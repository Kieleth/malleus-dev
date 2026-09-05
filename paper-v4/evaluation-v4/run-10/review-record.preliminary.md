# Malleus paper v4 run-10 source-grounded review record

Template. The row counts are substituted at freeze, from the frozen cell's own
query result, at the same time as `paper-v4/evaluation-v4/review-task-v3.template.md`.
No placeholder may survive instantiation.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

Fill one `rows` entry per returned row, in order, zero-based: 51 for
CQ-01, 164 for CQ-02, 165 for CQ-03, 172 for
CQ-04, 552 in all. Cite reading block ids only. Write the reasons in
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
    "review_input_manifest_sha256": "sha256:50ce795d7e929e34501b46b1d58fa55e5c1f463f64fed80c49f99402057ca634"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-preliminary-run-10",
    "completed_at": "2026-09-05T08:56:38Z"
  },
  "questions": [
    {
      "question_id": "CQ-01",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The rows answer the campaign part of the question outright: the cruise is returned as a campaign record with the months it ran, and the instrument record for the ocean-bottom seismometers is returned with a description that carries the network wording. The instrument count the question asks for is not answered. The rows reach the usable-instrument count, the instrument that produced no data and the minimum number an event had to be seen on, but no row carries the number of instruments deployed; the record holding that count is present in the population trace, is not among the witnesses these rows use, carries no subject reference in its formalization and belongs to a type this question's binding gives no entity case, so no row can reach it. Nothing in the row set ties the network or the campaign to the acquisition of the microseismicity data either: the one relation returned here is a funding tie between the cruise and a fleet body, and the datasets come back as free-standing records. What is answered is answered from the reading, so this is partial rather than unresponsive.",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The results block names the SMARTIES cruise as the campaign that acquired the microseismicity data, and the methods block dates it to the two summer months the row's interval spans at the month precision the row declares."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:008"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The data-availability block names the raw seismic data and the cruise reports and gives the fleet address the row carries as its resource url."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The geochemistry methods block names PetDB as the compilation source and gives the address the row repeats."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The same methods block names Supplementary Data 1; the row projects nothing about it beyond the name."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:008",
            "page:8:block:009"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The data-availability block names the earthquake catalogue with its picked arrivals, the repository it was deposited in and the deposit identifier, whose final digits fall into the following block, so both are cited."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The results block describes a network of ocean-bottom seismometers that acquired the microseismicity, which is what the row's name and description restate; the block does not use the word passive, but recording natural microseismicity with a seismometer network is what that word names here."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The code-availability block names Global Mapper; under this case the row projects only the name."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010",
            "page:8:block:011"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The code-availability block names the GMT toolbox in the version the row carries."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The focal-mechanism block names the HASH package; the row projects only the name."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The relocation block names the hypoDD program."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The earthquake-location block names the NonLinLoc program."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The seismic-data block names the SEISAN package."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The velocity-model block names the VELEST program."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The magnitude block names the ZMAP software."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The results block names the double-difference relocation method the hypocentres were passed through."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The magnitude block names the local magnitude scale the row carries."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The results block names the non-linear location algorithm used to obtain the hypocentres."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The earthquake-location block names the non-linear oct-tree search algorithm."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The results block names the trigger algorithm used for automatic arrival detection."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The velocity-model block identifies the average model as the best fitting of the five one-dimensional models and says it was kept for locating earthquakes and computing focal mechanisms, which is what the row's description states."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The degassing block names the solubility model used for the saturation calculation."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The geochemistry methods block names the solubility model of Iacono-Marziano and colleagues."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The discussion block names the thermal modelling whose temperatures it reports."
        },
        {
          "row_index": 23,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block supports a one-dimensional velocity model found from an active-source profile and used to compute travel times when locating earthquakes, but it does not say the model is a P-wave model, and that qualifier is part of the description the row carries."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:044"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The acknowledgement block names the Regional Council of Brittany among the funders."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:044"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The acknowledgement block names the European Research Council among the funders."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The affiliation footnote block gives this laboratory with the town and country the row carries as its location."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The affiliation footnote block gives this institute with the city and country the row carries."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The affiliation footnote block gives this institute with the city and country the row carries."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:044"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The acknowledgement block names the ISblue project as a funder."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The affiliation footnote block gives this university department with the city and country the row carries."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:044"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The acknowledgement block names the national science foundation of China among the funders."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The affiliation footnote block gives this key laboratory with the city and country the row carries."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:11:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The publisher's note block names Springer Nature."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:044"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The acknowledgement block names the French oceanographic fleet body as having funded the cruise's shipping time."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:044"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The acknowledgement block names the Zhejiang provincial foundation among the funders."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The code-availability block names Global Mapper and gives the address the row carries."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010",
            "page:8:block:011"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The code-availability block names the GMT toolbox and gives its address, which runs on into the following block, so both are cited."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The focal-mechanism block names HASH and the code-availability block gives its version and address, both of which the row carries."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The relocation block names hypoDD and the code-availability block gives its version and address."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The location block names NonLinLoc and the code-availability block gives its address."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The seismic-data block names SEISAN and the code-availability block gives its address."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The velocity-model block names VELEST and the code-availability block gives its address."
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The magnitude block names ZMAP and the code-availability block gives its address."
        },
        {
          "row_index": 44,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:10:block:044"
          ],
          "rationale": "DERIVATION_LOCAL The acknowledgement block ties the cruise to the fleet body, but only for the cruise's shipping time, while the row states an unqualified funding relation between the campaign and the organisation; that scope qualifier is absent from the row."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block sets a minimum number of instruments an event had to be detected on before it was kept, which is the quantity this projection names; the projection carries no count and everything it does state is in that block, while the instrument record itself is formalized in the results block, hence the non-local reading."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure caption block identifies the deployed instrument that produced no seismic data, which is the quantity this projection names; the count is not projected under this case."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The results block reports the instruments that yielded usable data for automatic arrival detection, which is the quantity named here, and presents it as a fact of the deployment rather than a calculation, consistent with the measured framing; the count itself is not projected under this case."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block requires each retained event to have been detected on at least five instruments, matching both the count and the scope this projection carries."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure caption block marks a single deployed instrument as having produced no seismic data, matching the count and the scope the row carries."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The results block gives the number of usable instruments from which arrivals were detected automatically, matching the count and the scope the row carries."
        }
      ]
    },
    {
      "question_id": "CQ-02",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "The rows name the subsections of the studied ridge portion and single out the short segment as the one the deep microseismicity sits under. A typed relation places the deep-microseismicity observation beneath that segment, and the observations attached to the segment give the depth band and say in their own names that the events lie under its ridge axis, with a separate record for the deeper events. The second half of the question is answered as well: the rows put the shallow off-axis cluster west of that same axis, the shallow events at the intersection outside corner and the normal-depth events beneath the southern discontinuity, so the position of the deep events relative to the axis is read off the rows rather than inferred. The same observations come back more than once because a record is returned under each observation type case it satisfies, which repeats the answer without changing it. Two qualifications worth recording, neither of which withholds the answer: a few of the supporting rows rest on figure caption or figure label blocks, and the ridge axis appears only inside the observations' own naming rather than as a record the relation points at.",
      "source_locators": [
        "page:2:block:004",
        "page:1:block:005",
        "page:2:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The introduction block names the Chain transform as one of the two transforms the ridge segment runs between; under this case the row projects only that name."
        },
        {
          "row_index": 1,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The introduction block gives the fault and its westward dipping character, but the inactive status the row states flat is offered in the later block as something the absence of deep microseismicity suggests, so the row carries the conclusion without the hedge the reading puts on it."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The subsection block gives the fault set of the first discontinuity with the two strikes the row carries."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The subsection block gives the normal faults affecting the second discontinuity with the two strikes the row carries."
        },
        {
          "row_index": 4,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The subsection block gives the strikes of the normal faults cutting the core complex surface, but it presents recent tectonic activity as what those faults are suggestive of, while the row states an active status outright."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The discussion block gives the high-angle inward dipping faults with the orientation the row carries."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The introduction block names the Romanche transform; under this case the row projects only the name."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The introduction block places the study in the equatorial Atlantic Ocean, which is the region the row names."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block comparing magmatic-tectonic settings names Iceland."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block comparing magmatic-tectonic settings names Mayotte, offshore in the western Indian Ocean."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The introduction block introduces the brittle-ductile boundary under the abbreviation the row carries as its name."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block on volatiles and melt introduces the lithosphere-asthenosphere boundary under the abbreviation the row carries."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The figure block for the schematic section names the expected Moho interface."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The discussion block names the axial valley whose floor it describes."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:007"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The figure block listing the shaded units names the hummocky seafloor."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The subsection block gives the median valley of the short segment."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The figure block lists the corrugated surface of the core complex among the tectonic elements it marks."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The observations block names the faulted dome of the core complex."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The discussion block names the core complex termination."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The introduction block names the oceanic core complex east of the ridge axis under the abbreviation the row carries."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The introduction block names the first non-transform discontinuity."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The introduction block names the second non-transform discontinuity."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The introduction block names the intersection subsection."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The introduction block names the short ridge segment between the two discontinuities."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The introduction block names the segment lying south of the second discontinuity."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The introduction block names the eastern ridge-transform intersection under the abbreviation the row carries."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block on ultraslow ridges names the Gakkel Ridge."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The compilation block names the Knipovich Ridge."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The introduction block names the Mid-Atlantic Ridge under the abbreviation the row carries."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The discussion block names the Southwest Indian Ridge under the abbreviation the row carries."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The introduction block names the Chain transform, and this case returns it as a transform fault."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The introduction block names the Romanche transform, and this case returns it as a transform fault."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The subsection block states that the core complex surface is cut by those striking normal faults, which is the relation the row carries between the two records."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:006"
          ],
          "rationale": "DERIVATION_LOCAL The figure block presents the corrugated surface as one of the core complex's own marked features, which supports the part-of relation."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DERIVATION_LOCAL The observations block places the deep microseismicity beneath the ridge axis of the short segment and gives the approximate depth band the source projection carries."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_NON_LOCAL The figure caption block places the core complex on the outside corner of the ridge, which is the relation the row carries; both endpoint records are formalized in the introduction block, hence the non-local reading."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The introduction block says the intersection subsection is bounded to the east by the detachment fault, which supports the bounding relation between the two records."
        },
        {
          "row_index": 37,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:4:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The block bounds the axial valley of the short segment by those inward dipping faults, while the row makes the segment itself the bounded record, which shifts what the reading says is bounded."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL The subsection block places the short segment immediately south of the first discontinuity, which is what the adjacency relation states; both endpoints are formalized in the introduction block."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The introduction block places the southern segment immediately south of the second discontinuity, which is what the adjacency relation states."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DERIVATION_LOCAL The same pairing as the earlier relation row, returned again under the seismological observation case; the observations block states both the depth band and the position beneath the segment's ridge axis."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The retained statement is the block's own sentence, the fault it is about is named there, and the interpretation label matches a conclusion the reading presents as suggested by an absence of deep events rather than established."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The statement matches the block, which attributes the enriched-source reading to earlier geochemical work, so the prior-interpretation label holds; the transform is named in that block while its own record is formalized in the introduction block."
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block attributes the shallow events beneath the dome to ruptures on the high-angle normal faults and hedges the attribution, which the interpretation label carries; the subject faults are named in the block."
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block states the southward shallowing of the boundary as an expectation, which is what the hypothesised modality and the expectation label carry; the boundary is named in the block."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block presents the combined carbon dioxide and water explanation for melt at the boundary as something the authors' analysis and earlier work suggest, matching the interpretation label."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block attributes the focusing and flushing of melt to an earlier study, matching the prior-interpretation label, and names the boundary the claim is about."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block describes the valley floor as the retained statement does and presents it as an observation rather than an inference, which matches the label."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block presents the eastward relocation of the axis as something the earthquake distribution and the tectonic observations suggest, which the interpretation label carries; the dome is named in the block."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block records that no evidence of a current eruption is seen in the valley, which matches the negated modality and the observation label."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block concludes from the resolution tests that the deep events beneath the segment axis are well constrained and required by the data, which is the claim the row carries."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block offers higher temperature at greater depth as a possible reason no earthquakes are seen deeper, which is what this claim names; the record carries no located statement and no digest, so there is nothing to recompute."
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block draws the conclusion that magmatism dominates crustal accretion at the segment, matching the retained statement and its interpretation label."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block records that no active vents have been observed on the segment axis, matching the negated modality and the observation label."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block states that the segment shows no evidence of detachment faulting, matching the negated modality; the retained statement is the block's opening sentence."
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block infers a magmatic origin for the segment from its axial morphology, matching the retained statement and the interpretation label."
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block states which two segments the samples were analysed for, matching the retained statement and the method label."
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block proposes the small pressure rise from degassing of the ascending melt as what induces the events beneath the segment axis, which is what this claim names; the record carries no located statement and no digest."
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block reports normal velocity ratios for the segment from earlier tomography, matching the retained statement and the prior-observation label."
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure caption block fixes the zero of the depth profiles at the intersection, matching the retained statement and the figure label."
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block opens the discussion with the departure from the relationship between boundary depth and spreading rate; the retained sentence breaks at the page boundary and completes in the following block, which is cited with it."
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block concludes from the shallow cluster on the western side of the valley that the unexpected event depths are not a location artefact, which is what this claim names; the record carries no located statement and no digest."
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same claim as the earlier row, returned again under the transform-fault subject case; the block carries the statement and names the transform."
        },
        {
          "row_index": 63,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the temperature figure for anhydrous peridotite at the boundary, but it places melt at sub-solidus temperatures, that is below that figure, whereas the row frames the quantity as the temperature at which melt is present and gives it as a single point."
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the boundary depth that the cold and thick lithosphere explanation would imply and presents it as one explanation among others, which the hypothesised modality carries."
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the isotherm range that such a boundary depth would correspond to; the record carries no located statement and no digest."
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The introduction block gives the isotherm, with the tolerance the row carries as its uncertainty, that the maximum earthquake depth is taken to mark."
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block states that the boundary stays shallow up to a young crustal age near the ridge, which is the open upper bound the row carries."
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure block gives the isotherm the plotted boundary is drawn to correspond to."
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports the melt fraction an earlier study proposed as required at the base of the boundary, which the modelled framing matches."
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same block gives the water content proposed alongside that melt fraction, as the upper bound the row carries."
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reads the boundary depth beneath the second discontinuity off the microseismicity that reaches that depth, which matches the value and the derived framing."
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003",
            "page:4:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the width of the axial valley; the sentence breaks at the page boundary and names the segment in the following block, which is cited with it. The negated modality belongs to that sentence, which is rejecting a hypothesis, and not to the width itself, which the reading asserts."
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL SUBJECT_IN_BLOCK The subsection block gives the width of the median valley of the short segment."
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The subsection block gives the length of the first discontinuity."
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The subsection block gives the bearing of the first discontinuity."
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The subsection block gives the ridge offset at the second discontinuity."
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The subsection block gives the bearing of the second discontinuity."
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The subsection block gives the length of the short segment."
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The subsection block gives the length of the southern segment."
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The subsection block gives the bearing of the southern segment."
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the temperature expected below twenty kilometres as a lower bound, which is how the row carries it, and presents it as coming from a thermal model."
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The introduction block gives the half-spreading rate of the ridge in the study area."
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The introduction block gives the length of the ridge segment between the two transforms."
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The results block gives the length of the eastern part of the transform that the network covered."
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block reports events located along the transform, which is the quantity this projection names; under this case no count is projected and everything the row does state is in the block."
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the average concentration earlier studies report for several segments of the region."
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same block gives the upper figure of that reported range."
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DERIVATION_LOCAL SUBJECT_IN_BLOCK The block gives the depth floor of the magmatic-tectonic seismicity offshore the island, which is the open lower bound the row carries."
        },
        {
          "row_index": 89,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same observation as the earlier row, returned again under the generic observation case; the block gives the figure for anhydrous peridotite but places melt below it, not at it, so the quantity's framing and its single point value overreach the prose."
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the boundary depth implied by the cold-lithosphere explanation and marks it as one explanation, which the hypothesised modality carries."
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the isotherm range that such a boundary depth would correspond to; the record carries no located statement and no digest."
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The introduction block gives the isotherm, with its tolerance, that the maximum earthquake depth is taken to mark."
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block states that the boundary stays shallow near the ridge up to a young crustal age, which is the bound the row carries."
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure block gives the isotherm the plotted boundary corresponds to."
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports the melt fraction an earlier study proposed as required at the base of the boundary."
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the water content proposed with it as an upper bound."
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reads the boundary depth beneath the second discontinuity off the microseismicity reaching that depth."
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003",
            "page:4:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the width of the axial valley and the sentence completes in the following block, which names the segment and is cited with it; the negated modality belongs to the hypothesis the sentence rejects, not to the width."
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL SUBJECT_IN_BLOCK The subsection block gives the width of the median valley of the short segment."
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports a cluster on the western side of the valley with the shallow focal depths the row carries."
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the depth limit of the events observed beneath the core complex, as the open upper bound the row carries."
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The subsection block gives the length of the first discontinuity."
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The subsection block gives its bearing."
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block states how deep the events beneath the second discontinuity reach, which is the approximate upper limit the row carries."
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the depth limit of the events beneath the second discontinuity as the open upper bound the row carries."
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The observations block gives the depth band of the normal-depth events beneath the southern discontinuity."
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The subsection block gives the ridge offset at the second discontinuity."
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The subsection block gives its bearing."
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the bearing along which the deep events beneath the segment axis are aligned."
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block records that no events are seen deeper than twenty kilometres beneath the segment axis, which matches the negated modality and the open lower bound."
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the depth limit of the shallow off-axis microseismicity west of the segment axis."
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the barium enrichment of the segment samples as the lower bound the row carries."
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block gives the pre-eruptive concentration range estimated from barium for this segment."
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block gives the primary-melt range estimated from the barium-based proxy for this segment."
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the calculated volatile content of melts generated along this segment as the range the row carries."
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block gives the pre-eruptive concentration range estimated from rubidium for this segment."
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block gives the primary-melt range estimated from the rubidium-based proxy for this segment."
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the depths of the deep earthquakes observed beneath the segment axis as the band the row carries."
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The observations block gives the approximate depth band of the deep microseismicity beneath the segment's ridge axis."
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The subsection block gives the length of the segment."
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the estimated pre-eruptive concentration range for the segment, which matches the value and the estimated framing."
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block states the floor of the primary-melt concentration along the segment, which is the open lower bound the row carries."
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the rubidium enrichment of the segment samples as the lower bound the row carries."
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block gives the pre-eruptive range estimated from barium for the southern segment."
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block gives the primary-melt range estimated from the barium-based proxy for the southern segment."
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the calculated volatile content for the southern segment as the range the row carries."
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block gives the pre-eruptive range estimated from rubidium for the southern segment."
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block gives the primary-melt range estimated from the rubidium-based proxy for the southern segment."
        },
        {
          "row_index": 129,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The subsection block gives the length of the southern segment."
        },
        {
          "row_index": 130,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The subsection block gives the bearing of the southern segment."
        },
        {
          "row_index": 131,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the temperature expected below twenty kilometres as a lower bound and presents it as model-derived."
        },
        {
          "row_index": 132,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The results block reports the earthquakes located in the vicinity of the intersection region, which is the quantity this projection names; the count itself is not projected under this case."
        },
        {
          "row_index": 133,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The observations block gives the depth band of the majority of shallow earthquakes on the outside corner of the intersection."
        },
        {
          "row_index": 134,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure block gives the depth band below the sea floor of the deep earthquakes beneath the ridge axis."
        },
        {
          "row_index": 135,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The introduction block gives the half-spreading rate of the ridge in the study area."
        },
        {
          "row_index": 136,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The results block gives the length of the ridge axis the network covered."
        },
        {
          "row_index": 137,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:004",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block is the figure's own histogram labelling and carries the ridge total as text; the same total is stated in prose in the relocation block, which is cited with it. The count itself is not projected under this case."
        },
        {
          "row_index": 138,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The relocation block states how many events were located along the ridge; the count is not projected under this case."
        },
        {
          "row_index": 139,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The introduction block gives the length of the ridge segment between the two transforms."
        },
        {
          "row_index": 140,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports the highest melt concentration previously reported at that ridge, which is the value and the prior framing the row carries."
        },
        {
          "row_index": 141,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same coverage observation, returned again under the transform-fault subject case; the results block gives the covered length of the eastern part of the transform."
        },
        {
          "row_index": 142,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The relocation block reports events located along the transform; no count is projected under this case."
        },
        {
          "row_index": 143,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same coverage observation again under the seismological case; the results block gives the covered length."
        },
        {
          "row_index": 144,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The relocation block gives the number of events located along the transform, matching the count and the scope the row carries."
        },
        {
          "row_index": 145,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DERIVATION_LOCAL SUBJECT_IN_BLOCK The block gives the depth floor of the seismicity offshore the island, which the record and its subject are both formalized from."
        },
        {
          "row_index": 146,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports the shallow focal depths of the cluster on the western side of the valley."
        },
        {
          "row_index": 147,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the depth limit of the events beneath the core complex."
        },
        {
          "row_index": 148,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block states how deep the events beneath the second discontinuity reach."
        },
        {
          "row_index": 149,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives their depth limit as an open upper bound."
        },
        {
          "row_index": 150,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The observations block gives the depth band of the normal-depth events beneath the southern discontinuity."
        },
        {
          "row_index": 151,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the bearing along which the deep events beneath the segment axis are aligned."
        },
        {
          "row_index": 152,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block records that no events are seen deeper than twenty kilometres beneath the segment axis."
        },
        {
          "row_index": 153,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the depth limit of the shallow off-axis microseismicity west of the segment axis."
        },
        {
          "row_index": 154,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the depths of the deep earthquakes observed beneath the segment axis."
        },
        {
          "row_index": 155,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The observations block gives the approximate depth band of the deep microseismicity beneath the segment's ridge axis."
        },
        {
          "row_index": 156,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The results block gives the number of earthquakes located in the vicinity of the intersection region, matching the count and the scope the row carries."
        },
        {
          "row_index": 157,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The observations block gives the depth band of the majority of shallow earthquakes at the outside corner of the intersection."
        },
        {
          "row_index": 158,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure block gives the depth band below the sea floor of the deep earthquakes beneath the ridge axis."
        },
        {
          "row_index": 159,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The results block gives the length of the ridge axis covered by the network."
        },
        {
          "row_index": 160,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:004",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The count comes from the figure's histogram labelling in that block, and the same total is stated in prose in the relocation block, which is cited with it; both match the count and its scope."
        },
        {
          "row_index": 161,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The relocation block gives the number of events located along the ridge, matching the count and the scope the row carries."
        },
        {
          "row_index": 162,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The results block gives the covered length of the eastern part of the transform."
        },
        {
          "row_index": 163,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The relocation block gives the number of events located along the transform, matching the count and its scope."
        }
      ]
    },
    {
      "question_id": "CQ-03",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "The rows carry both quantities the question asks for. The depth of the deep microseismicity beneath the segment's ridge axis is returned with its bounds, its kilometre unit, a measured determination and the segment as its subject, and the narrower reading taken from the discussion sits beside it. The calculated primary-melt carbon dioxide range comes back in the same shape, in weight per cent, marked derived or estimated, with the primary melt or the segment as its subject, and the barium and rubidium routes to it are returned separately rather than merged. Units and estimate status sit on the rows themselves and do not have to be inferred. The southern segment's values are returned too, but every row names the segment it belongs to, so which association a value attaches to is never ambiguous. The type-only binding also returns a great deal the question did not ask for; that is noise around a complete answer rather than a gap in it.",
      "source_locators": [
        "page:1:block:001",
        "page:2:block:004",
        "page:2:block:006",
        "page:5:block:005",
        "page:8:block:006",
        "page:8:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names barium among the trace elements whose ratio to carbon dioxide the authors rely on, which is all this row's single name projection asserts.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names carbon dioxide throughout as the volatile under study, which carries the row's bare name projection.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block lists water beside carbon dioxide among the volatiles, in the same spaced form the row projects, so the name holds.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the forsterite-90 olivine composition that the equilibrium melt concentrations are referred to, which matches the row's name.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names rubidium as one of the two trace elements the ratio proxy uses, which is what the row's name asserts.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the raw seismic data and the cruise reports and gives the campaign address the row projects, so both fields are carried.",
          "source_locators": [
            "page:8:block:008"
          ]
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the sample database and gives the same web address the row projects.",
          "source_locators": [
            "page:8:block:005"
          ]
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block refers to the supplementary data item under the name the row carries.",
          "source_locators": [
            "page:8:block:005"
          ]
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The two cited blocks together name the deposited catalogue, the repository and the identifier, whose digits fall across the block boundary; both are cited, so every projected field is covered.",
          "source_locators": [
            "page:8:block:008",
            "page:8:block:009"
          ]
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block introduces the brittle-ductile boundary and the abbreviation the row projects as its name.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block introduces the lithosphere-asthenosphere boundary and the abbreviation the row carries.",
          "source_locators": [
            "page:5:block:010"
          ]
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The figure-caption block names the Moho interface drawn in the schematic, which matches the row's name.",
          "source_locators": [
            "page:7:block:011"
          ]
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block opens on the oceanic crust and how it forms, so the row's bare name is carried.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block describes the brittle, cooled lithosphere that sits over partly molten material, which supports the row's name.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the mantle as the source of the melt, which is all the row asserts.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the ascending melt as what the degassing comes from, matching the row's name.",
          "source_locators": [
            "page:5:block:002"
          ]
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block speaks of these melts and of the pre-eruptive concentrations estimated for them, which carries both the row's name and its material kind.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports the carbon dioxide quantity in the primary melts, so the row's name is carried.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the double-difference relocation method the row projects.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the local magnitude scale used for the event sizes, matching the row's name.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the non-linear location algorithm used for the hypocentres, as the row does.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the oct-tree search algorithm the location program uses, which matches the row's name.",
          "source_locators": [
            "page:7:block:004"
          ]
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the short-term over long-term average trigger used for automatic detection, as the row's name states.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block identifies the average velocity model as the fifth and best fitting of five one-dimensional models and says it was kept for the subsequent location and focal mechanism work, which covers the row's name and its description.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the carbon dioxide solubility model used to place saturation, matching the row's name.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the solubility model of Iacono-Marziano as the basis of the calculation, matching the row's name.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block attributes the temperature range at depth to thermal modelling, which is the row's name.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 27,
          "source_support": "PARTIAL",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block supports a one-dimensional velocity model chosen so that travel times could be computed for the locations, but it never restricts that model to compressional velocities; the description's P-wave qualifier is absent from the cited block, so only part of the projection is supported.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block identifies the average velocity model as the fifth and best fitting of five one-dimensional models and says it was kept for the subsequent location and focal mechanism work, which covers the row's name and its description.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the carbon dioxide solubility model used to place saturation, matching the row's name.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the solubility model of Iacono-Marziano as the basis of the calculation, matching the row's name.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block attributes the temperature range at depth to thermal modelling, which is the row's name.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 32,
          "source_support": "PARTIAL",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block supports a one-dimensional velocity model chosen so that travel times could be computed for the locations, but it never restricts that model to compressional velocities; the description's P-wave qualifier is absent from the cited block, so only part of the projection is supported.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block gives the carbon dioxide to barium ratio with its uncertainty and describes such ratios as global trends, which covers every field the row projects.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block gives the carbon dioxide to rubidium ratio with its uncertainty and describes such ratios as global trends, matching the row.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports the compressional to shear velocity ratio obtained from the arrival-time analysis at the value the row carries; the source's approximation mark has no slot on this projection.",
          "source_locators": [
            "page:7:block:002"
          ]
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the ridge-transform intersection segment by the label the row projects.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the short ridge segment by the label the row projects.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the segment south of the second discontinuity by the label the row projects.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Both cited blocks describe the compiled mid-ocean ridge basalt samples the row names, one at the compilation step and one in the methods.",
          "source_locators": [
            "page:5:block:004",
            "page:8:block:005"
          ]
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports basalts seen on the sea floor, which matches the row's name.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports peridotites seen on the sea floor, which matches the row's name.",
          "source_locators": [
            "page:1:block:006"
          ]
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Both cited blocks describe the compiled mid-ocean ridge basalt samples the row names, one at the compilation step and one in the methods.",
          "source_locators": [
            "page:5:block:004",
            "page:8:block:005"
          ]
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL The block states that the deep microseismicity sits under the segment's ridge axis, which is the relation the row asserts; the same block carries the depth range, the unit and the measured character of the source observation, and the segment endpoint is named there as well as in its own block.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ]
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL The block states that the deep microseismicity sits under the segment's ridge axis, which is the relation the row asserts; the same block carries the depth range, the unit and the measured character of the source observation, and the segment endpoint is named there as well as in its own block.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ]
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence sits in the cited block and says carbon dioxide behaves at depth like the most incompatible trace elements, which is what the row's name and background-statement kind assert.",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:004"
          ]
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The abstract block carries the located sentence proposing that degassing-driven volume change causes the deep mantle earthquakes, and the discussion block cited beside it is where the authors name this possibility as the one they prefer, so the name, the proposed-mechanism kind and the preferred disposition all hold.",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002"
          ]
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence is the caption line in the cited block describing carbon dioxide content plotted against rubidium and against barium, which matches the row's name and its figure-statement kind.",
          "source_locators": [
            "page:1:block:001",
            "page:6:block:005"
          ]
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The located sentence closes the abstract block with a forward-looking statement about melt below the boundary, which fits the row's projected-consequence kind and its hypothesised modality.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence in the methods block calls the two ratios a good stand-in for the concentration, which is the row's name and its background-statement kind.",
          "source_locators": [
            "page:1:block:001",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence states the expectation that the boundary shallows away from the intersection, which matches the row's expectation kind and hypothesised modality.",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ]
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence puts melt at the boundary down to the two volatiles together, hedged as a suggestion, which is what the row's name and interpretation kind carry.",
          "source_locators": [
            "page:5:block:010",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The located sentence reports an earlier study's proposal that volatiles both focus melt under the axis and drive it aside towards the boundary, which matches the row's prior-interpretation kind.",
          "source_locators": [
            "page:5:block:010"
          ]
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block raises the cold thick lithosphere as one explanation and then argues against it from the segment's volcanic morphology, so both the candidate-explanation kind and the not-supported disposition are carried; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block places the deep events in the mantle below ten kilometres, which is the row's interpretation; the source qualifies this as where most of them sit, with a few scattered in the crust, and the row's name does not restate that qualification.",
          "source_locators": [
            "page:1:block:002",
            "page:2:block:006"
          ]
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence states the hydrothermal cooling hypothesis and the rest of the block withdraws it for want of active venting near the segment, which supports both the candidate-explanation kind and the not-supported disposition.",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:002"
          ]
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence states the shear-zone strain hypothesis and the block then says the observations do not bear it out, which matches the row's kind and its disposition.",
          "source_locators": [
            "page:1:block:002",
            "page:3:block:003"
          ]
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence in the first cited block states the magmatic-tectonic hypothesis, and the second cited block is where the authors set the melt-movement mechanism aside for these events, so the not-supported disposition holds.",
          "source_locators": [
            "page:1:block:002",
            "page:4:block:002",
            "page:5:block:001"
          ]
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence offers melt freezing where the lithosphere bottoms out as a possible outcome, which fits the row's projected-consequence kind and hypothesised modality.",
          "source_locators": [
            "page:1:block:004",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reads the off-axis shallow swarm as probably tied to magmatism in the crust away from the axis, which is the row's interpretation; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:002",
            "page:5:block:001"
          ]
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block concludes that the mantle under the segment axis is hot, which is what the row's name and interpretation kind assert.",
          "source_locators": [
            "page:1:block:002",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence is the caption line describing the plotted primary-melt carbon dioxide contours, which matches the row's figure-statement kind.",
          "source_locators": [
            "page:1:block:001",
            "page:6:block:005"
          ]
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure-caption block reads the deep earthquakes as volume change from degassing of the ascending melts in hot ductile mantle, which is the row's interpretation; this projection has no statement digest.",
          "source_locators": [
            "page:5:block:002",
            "page:7:block:012"
          ]
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence infers from the depth of the microseismicity that ascending melt sits, fractionates and evolves at those depths, which is the row's interpretation.",
          "source_locators": [
            "page:5:block:002",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence separates primary melts in equilibrium with their source from the pre-eruptive melts that have crystallised on the way up, which matches the row's background-statement kind.",
          "source_locators": [
            "page:1:block:001",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence concludes from the resolution tests that the deep events are demanded by the observations rather than produced by the location procedure, which is the row's interpretation.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:001"
          ]
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block explains the lack of events below twenty kilometres by temperatures too high for rupture to nucleate, offered as a possibility, which fits the row's interpretation kind; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:007"
          ]
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence concludes that magmatism governs crustal accretion at the segment, which is the row's interpretation.",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:002"
          ]
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence records that no active venting has been seen on the segment axis, which matches the row's negated modality and observation kind.",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:002"
          ]
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence records that the segment shows nothing indicating detachment faulting, which matches the row's negated modality.",
          "source_locators": [
            "page:1:block:005",
            "page:4:block:001"
          ]
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence reads the volcanic morphology of the axial valley as showing the segment is magmatic in origin, which is the row's interpretation.",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence in the methods block states that the samples of the studied segment and its southern neighbour were analysed, which matches the row's method-statement kind.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:005"
          ]
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block ends by suggesting that the small pressure rise from degassing of the ascending melt brings on the earthquakes under the segment axis, which is the row's proposed mechanism; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:003"
          ]
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence reports that earlier tomography found ordinary velocity ratios at the segment, which matches the row's prior-observation kind.",
          "source_locators": [
            "page:1:block:005",
            "page:7:block:003"
          ]
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence reports that the concentrations measured in the samples of both segments sit close to the solubility computed for the sampling pressure, which is the row's observation and its measured modality.",
          "source_locators": [
            "page:5:block:004",
            "page:5:block:006",
            "page:8:block:005"
          ]
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence concludes from the closeness of the computed solubility and the measured contents that the samples have lost their volatiles, which matches the row's interpretation and calculated modality.",
          "source_locators": [
            "page:5:block:004",
            "page:8:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence states that basalts recovered from the sea floor have for the most part already lost their volatiles, which is the row's interpretation.",
          "source_locators": [
            "page:2:block:001",
            "page:5:block:006"
          ]
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence reports that the concentrations measured in the samples of both segments sit close to the solubility computed for the sampling pressure, which is the row's observation and its measured modality.",
          "source_locators": [
            "page:5:block:004",
            "page:5:block:006",
            "page:8:block:005"
          ]
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence concludes from the closeness of the computed solubility and the measured contents that the samples have lost their volatiles, which matches the row's interpretation and calculated modality.",
          "source_locators": [
            "page:5:block:004",
            "page:8:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block projects continued degassing during ascent producing earthquakes across the depth interval the row bounds, in the unit it carries, and the hypothesised modality matches the conditional wording.",
          "source_locators": [
            "page:1:block:002",
            "page:5:block:009"
          ]
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The abstract block reports the carbon dioxide quantity of the primary melts over the bounds and in the unit the row carries and marks it approximate as the row does; the calculated modality matches its derivation from sample geochemistry.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports the barium enrichment of the segment's samples as a floor in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:004"
          ]
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the barium-derived pre-eruptive estimate for the segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the barium-derived primary-melt estimate for the segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the calculated carbon dioxide content of melts generated along the segment over the bounds and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:005"
          ]
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the rubidium-derived pre-eruptive estimate for the segment at the bounds and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the rubidium-derived primary-melt estimate for the segment at the bounds and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the estimated pre-eruptive concentrations for the segment over the bounds and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:006"
          ]
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence states a floor on the primary-melt concentration along the segment, which the row records as an open lower bound in the same unit.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence reports the rubidium enrichment of the segment's samples as a floor in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:004"
          ]
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the barium-derived pre-eruptive estimate for the southern segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the barium-derived primary-melt estimate for the southern segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the calculated carbon dioxide content of melts from the southern segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:005"
          ]
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the rubidium-derived pre-eruptive estimate for the southern segment at the bounds and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the rubidium-derived primary-melt estimate for the southern segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the sub-solidus temperature for dry peridotite at the boundary as the approximate value the row carries.",
          "source_locators": [
            "page:5:block:010",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the boundary depth the cold-lithosphere explanation would imply, approximate and in the unit the row carries, and the hypothesised modality matches its conditional framing.",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block ties that same boundary depth to the temperature range the row bounds; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The located sentence in the same block ties the maximum earthquake depth to the isotherm and the tolerance the row carries.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the depth under which the boundary stays shallow away from the axis, which the row records as an open upper bound; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure-caption block ties the drawn boundary to the isotherm value the row carries.",
          "source_locators": [
            "page:1:block:004",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the melt fraction the earlier work needs at the base of the boundary, approximate and in the unit the row carries.",
          "source_locators": [
            "page:5:block:010",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the water content proposed there as a ceiling, which the row records as an open upper bound; this projection has no statement digest.",
          "source_locators": [
            "page:5:block:010",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence puts the boundary under the southern discontinuity at the approximate depth the row carries.",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the age of the crust on the western flank that the row records; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:002",
            "page:2:block:006"
          ]
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the crustal age up to which the boundary stays shallow, approximate and in the unit the row carries; the block names the crust only in adjectival form, which is how the subject occurs there.",
          "source_locators": [
            "page:1:block:002",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the thickness of that western flank crust with the tolerance the row carries.",
          "source_locators": [
            "page:1:block:002",
            "page:2:block:006"
          ]
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure-caption block gives the crustal thickness under the segment with the same tolerance, marked approximate as the row marks it.",
          "source_locators": [
            "page:1:block:002",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the age of the cold lithosphere behind the edge effect, in the unit the row carries.",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ]
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the modelled temperature range across that depth interval, which the row bounds and marks modelled.",
          "source_locators": [
            "page:1:block:002",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block concludes that the earthquakes occur in mantle hotter than the floor the row records as an open lower bound; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:002",
            "page:3:block:002"
          ]
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the age below which accreted crust is treated as young, which the row records as an open upper bound; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:002",
            "page:7:block:009"
          ]
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the length of the segment, approximate and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ]
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the length of the southern segment in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ]
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the southern segment's bearing, which the row records as an approximate angle east of north; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ]
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the temperature floor inferred below twenty kilometres under the segment axis, which the row records as an open lower bound; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:007"
          ]
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the sub-solidus temperature for dry peridotite at the boundary as the approximate value the row carries.",
          "source_locators": [
            "page:5:block:010",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the boundary depth the cold-lithosphere explanation would imply, approximate and in the unit the row carries, and the hypothesised modality matches its conditional framing.",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block ties that same boundary depth to the temperature range the row bounds; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The located sentence in the same block ties the maximum earthquake depth to the isotherm and the tolerance the row carries.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the depth under which the boundary stays shallow away from the axis, which the row records as an open upper bound; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure-caption block ties the drawn boundary to the isotherm value the row carries.",
          "source_locators": [
            "page:1:block:004",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the melt fraction the earlier work needs at the base of the boundary, approximate and in the unit the row carries.",
          "source_locators": [
            "page:5:block:010",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the water content proposed there as a ceiling, which the row records as an open upper bound; this projection has no statement digest.",
          "source_locators": [
            "page:5:block:010",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence puts the boundary under the southern discontinuity at the approximate depth the row carries.",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The abstract block reports the deep earthquakes across the depth interval the row bounds, in the unit it carries, and the measured modality matches the observational framing.",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:002"
          ]
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block projects continued degassing during ascent producing earthquakes across the depth interval the row bounds, in the unit it carries, and the hypothesised modality matches the conditional wording.",
          "source_locators": [
            "page:1:block:002",
            "page:5:block:009"
          ]
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the age of the crust on the western flank that the row records; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:002",
            "page:2:block:006"
          ]
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the crustal age up to which the boundary stays shallow, approximate and in the unit the row carries; the block names the crust only in adjectival form, which is how the subject occurs there.",
          "source_locators": [
            "page:1:block:002",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 129,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the thickness of that western flank crust with the tolerance the row carries.",
          "source_locators": [
            "page:1:block:002",
            "page:2:block:006"
          ]
        },
        {
          "row_index": 130,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure-caption block gives the crustal thickness under the segment with the same tolerance, marked approximate as the row marks it.",
          "source_locators": [
            "page:1:block:002",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 131,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the age of the cold lithosphere behind the edge effect, in the unit the row carries.",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ]
        },
        {
          "row_index": 132,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the modelled temperature range across that depth interval, which the row bounds and marks modelled.",
          "source_locators": [
            "page:1:block:002",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 133,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block concludes that the earthquakes occur in mantle hotter than the floor the row records as an open lower bound; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:002",
            "page:3:block:002"
          ]
        },
        {
          "row_index": 134,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the age below which accreted crust is treated as young, which the row records as an open upper bound; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:002",
            "page:7:block:009"
          ]
        },
        {
          "row_index": 135,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The abstract block reports the carbon dioxide quantity of the primary melts over the bounds and in the unit the row carries and marks it approximate as the row does; the calculated modality matches its derivation from sample geochemistry.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 136,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the bearing along which the deep events under the segment axis line up, approximate as the row records it.",
          "source_locators": [
            "page:1:block:005",
            "page:4:block:003"
          ]
        },
        {
          "row_index": 137,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence records that nothing is seen below that depth under the segment's ridge axis, which matches the row's negated modality and its open lower bound.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:007"
          ]
        },
        {
          "row_index": 138,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the depth the off-axis shallow microseismicity reaches west of the segment axis, which the row records as an open upper bound.",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 139,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports the barium enrichment of the segment's samples as a floor in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:004"
          ]
        },
        {
          "row_index": 140,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the barium-derived pre-eruptive estimate for the segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 141,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the barium-derived primary-melt estimate for the segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 142,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the calculated carbon dioxide content of melts generated along the segment over the bounds and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:005"
          ]
        },
        {
          "row_index": 143,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the rubidium-derived pre-eruptive estimate for the segment at the bounds and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 144,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the rubidium-derived primary-melt estimate for the segment at the bounds and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 145,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the depth range of the deep earthquakes observed under the segment axis that the row bounds, in the unit it carries.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:006"
          ]
        },
        {
          "row_index": 146,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the approximate depth range over which the deep microseismicity sits under the segment's own ridge axis, in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ]
        },
        {
          "row_index": 147,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the length of the segment, approximate and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ]
        },
        {
          "row_index": 148,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the estimated pre-eruptive concentrations for the segment over the bounds and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:006"
          ]
        },
        {
          "row_index": 149,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence states a floor on the primary-melt concentration along the segment, which the row records as an open lower bound in the same unit.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 150,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence reports the rubidium enrichment of the segment's samples as a floor in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:004"
          ]
        },
        {
          "row_index": 151,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the barium-derived pre-eruptive estimate for the southern segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 152,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the barium-derived primary-melt estimate for the southern segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 153,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the calculated carbon dioxide content of melts from the southern segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:005"
          ]
        },
        {
          "row_index": 154,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the rubidium-derived pre-eruptive estimate for the southern segment at the bounds and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 155,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the rubidium-derived primary-melt estimate for the southern segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 156,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the length of the southern segment in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ]
        },
        {
          "row_index": 157,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the southern segment's bearing, which the row records as an approximate angle east of north; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ]
        },
        {
          "row_index": 158,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the temperature floor inferred below twenty kilometres under the segment axis, which the row records as an open lower bound; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:007"
          ]
        },
        {
          "row_index": 159,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The abstract block reports the deep earthquakes across the depth interval the row bounds, in the unit it carries, and the measured modality matches the observational framing.",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:002"
          ]
        },
        {
          "row_index": 160,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the bearing along which the deep events under the segment axis line up, approximate as the row records it.",
          "source_locators": [
            "page:1:block:005",
            "page:4:block:003"
          ]
        },
        {
          "row_index": 161,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence records that nothing is seen below that depth under the segment's ridge axis, which matches the row's negated modality and its open lower bound.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:007"
          ]
        },
        {
          "row_index": 162,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the depth the off-axis shallow microseismicity reaches west of the segment axis, which the row records as an open upper bound.",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 163,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the depth range of the deep earthquakes observed under the segment axis that the row bounds, in the unit it carries.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:006"
          ]
        },
        {
          "row_index": 164,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the approximate depth range over which the deep microseismicity sits under the segment's own ridge axis, in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ]
        }
      ]
    },
    {
      "question_id": "CQ-04",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The preferred mechanism is present and is marked as a hypothesis rather than as fact: one row carries the authors' suggestion that degassing-driven volume change causes the deep mantle earthquakes, with a preferred disposition and a proposed-mechanism kind, and it reaches both the abstract block and the discussion block where that possibility is named as the authors' own. Ascending melt, the degassing, the volume change, the pressure rise and the triggering of the earthquakes are all present across the rows, and the three rejected explanations come back carrying not-supported dispositions, which is the contrast the question asks for. One required element is missing. The extensional stress the volume change is said to act against appears in the reading, but the record formalising that sentence is a claim with no subject, so it falls outside every case this type-only binding expands and reaches no row. The rows therefore answer most of the question and leave one part of the mechanism unrepresented.",
      "source_locators": [
        "page:1:block:001",
        "page:3:block:003",
        "page:5:block:002",
        "page:5:block:003",
        "page:7:block:012"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names barium among the trace elements whose ratio to carbon dioxide the authors rely on, which is all this row's single name projection asserts.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names carbon dioxide throughout as the volatile under study, which carries the row's bare name projection.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block lists water beside carbon dioxide among the volatiles, in the same spaced form the row projects, so the name holds.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the forsterite-90 olivine composition that the equilibrium melt concentrations are referred to, which matches the row's name.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names rubidium as one of the two trace elements the ratio proxy uses, which is what the row's name asserts.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the Chain transform as one of the two bounding the studied ridge stretch.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The first cited block gives the fault's westward dipping detachment character and the second gives the authors' reading that it is no longer active, so all three projected fields are covered; the source hedges the inactivity as a suggestion and the row states it flat.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ]
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block describes the first discontinuity as marked by faults on the two strikes the row's fault kind carries.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block describes the second discontinuity as affected by normal faults on the two strikes the row projects.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block describes the core complex surface as cut by normal faults on the strikes the row carries and reads the deformation there as recent and active; the row's active status states that reading without the source's hedge.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block describes the faults bounding the segment with the dip and orientation the row's fault kind carries.",
          "source_locators": [
            "page:4:block:001"
          ]
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the Romanche transform, which is the row's whole content.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports an extinct vent field on the flank of the first discontinuity, which supports both the name and the inactive status.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The figure-caption block marks an inactive hydrothermal mound inferred from the dive observations, covering the row's name and status.",
          "source_locators": [
            "page:2:block:007"
          ]
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block introduces the brittle-ductile boundary and the abbreviation the row projects as its name.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block introduces the lithosphere-asthenosphere boundary and the abbreviation the row carries.",
          "source_locators": [
            "page:5:block:010"
          ]
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The figure-caption block names the Moho interface drawn in the schematic, which matches the row's name.",
          "source_locators": [
            "page:7:block:011"
          ]
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block opens on the oceanic crust and how it forms, so the row's bare name is carried.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block describes the brittle, cooled lithosphere that sits over partly molten material, which supports the row's name.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the mantle as the source of the melt, which is all the row asserts.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the ascending melt as what the degassing comes from, matching the row's name.",
          "source_locators": [
            "page:5:block:002"
          ]
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block speaks of these melts and of the pre-eruptive concentrations estimated for them, which carries both the row's name and its material kind.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports the carbon dioxide quantity in the primary melts, so the row's name is carried.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block identifies the average velocity model as the fifth and best fitting of five one-dimensional models and says it was kept for the subsequent location and focal mechanism work, which covers the row's name and its description.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the carbon dioxide solubility model used to place saturation, matching the row's name.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the solubility model of Iacono-Marziano as the basis of the calculation, matching the row's name.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block attributes the temperature range at depth to thermal modelling, which is the row's name.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 27,
          "source_support": "PARTIAL",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block supports a one-dimensional velocity model chosen so that travel times could be computed for the locations, but it never restricts that model to compressional velocities; the description's P-wave qualifier is absent from the cited block, so only part of the projection is supported.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the ridge-transform intersection segment by the label the row projects.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the short ridge segment by the label the row projects.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the segment south of the second discontinuity by the label the row projects.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the Chain transform as one of the two bounding the studied ridge stretch.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the Romanche transform, which is the row's whole content.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the Icelandic volcano among the comparison cases, matching the row.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the Icelandic peninsula among the comparison cases, matching the row.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The methods block names the seamount whose depth datum was updated in the compilation, matching the row.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block describes the neo-volcanic ridge in the median valley of the segment, which matches the row's name.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The methods block names the massif included in the compilation for reference, matching the row.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The figure-caption block names the volcanic cones shaded on the map, matching the row's name.",
          "source_locators": [
            "page:4:block:007"
          ]
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL The block states that the deep microseismicity sits under the segment's ridge axis, which is the relation the row asserts; the same block carries the depth range, the unit and the measured character of the source observation, and the segment endpoint is named there as well as in its own block.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ]
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The block says the intersection segment is bounded on its eastern side by the westward dipping detachment fault, which gives the relation and both endpoints; the fault's inactive status comes from the second cited block.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ]
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The block says the segment is bounded by the high-angle inward dipping faults the row's target projects, which is exactly the relation asserted.",
          "source_locators": [
            "page:1:block:005",
            "page:4:block:001"
          ]
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL The block states that the deep microseismicity sits under the segment's ridge axis, which is the relation the row asserts; the same block carries the depth range, the unit and the measured character of the source observation, and the segment endpoint is named there as well as in its own block.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ]
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence sits in the cited block and says carbon dioxide behaves at depth like the most incompatible trace elements, which is what the row's name and background-statement kind assert.",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:004"
          ]
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The abstract block carries the located sentence proposing that degassing-driven volume change causes the deep mantle earthquakes, and the discussion block cited beside it is where the authors name this possibility as the one they prefer, so the name, the proposed-mechanism kind and the preferred disposition all hold.",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002"
          ]
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence is the caption line in the cited block describing carbon dioxide content plotted against rubidium and against barium, which matches the row's name and its figure-statement kind.",
          "source_locators": [
            "page:1:block:001",
            "page:6:block:005"
          ]
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The located sentence closes the abstract block with a forward-looking statement about melt below the boundary, which fits the row's projected-consequence kind and its hypothesised modality.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence in the methods block calls the two ratios a good stand-in for the concentration, which is the row's name and its background-statement kind.",
          "source_locators": [
            "page:1:block:001",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The located sentence reads the absence of deep microseismicity near the termination as showing the detachment is no longer active, which is the row's interpretation.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ]
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence attributes the enriched basalts and their high volatile contents, as earlier studies read them, to limited melting of an already enriched source near the transform, which matches the row's prior-interpretation kind.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:005"
          ]
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence reads the shallow events under the dome as breaks on the steep normal faults cutting its surface, which is the row's interpretation.",
          "source_locators": [
            "page:2:block:001",
            "page:2:block:005"
          ]
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence states the expectation that the boundary shallows away from the intersection, which matches the row's expectation kind and hypothesised modality.",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ]
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence puts melt at the boundary down to the two volatiles together, hedged as a suggestion, which is what the row's name and interpretation kind carry.",
          "source_locators": [
            "page:5:block:010",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The located sentence reports an earlier study's proposal that volatiles both focus melt under the axis and drive it aside towards the boundary, which matches the row's prior-interpretation kind.",
          "source_locators": [
            "page:5:block:010"
          ]
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block raises the cold thick lithosphere as one explanation and then argues against it from the segment's volcanic morphology, so both the candidate-explanation kind and the not-supported disposition are carried; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block places the deep events in the mantle below ten kilometres, which is the row's interpretation; the source qualifies this as where most of them sit, with a few scattered in the crust, and the row's name does not restate that qualification.",
          "source_locators": [
            "page:1:block:002",
            "page:2:block:006"
          ]
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence states the hydrothermal cooling hypothesis and the rest of the block withdraws it for want of active venting near the segment, which supports both the candidate-explanation kind and the not-supported disposition.",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:002"
          ]
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence states the shear-zone strain hypothesis and the block then says the observations do not bear it out, which matches the row's kind and its disposition.",
          "source_locators": [
            "page:1:block:002",
            "page:3:block:003"
          ]
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence in the first cited block states the magmatic-tectonic hypothesis, and the second cited block is where the authors set the melt-movement mechanism aside for these events, so the not-supported disposition holds.",
          "source_locators": [
            "page:1:block:002",
            "page:4:block:002",
            "page:5:block:001"
          ]
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence offers melt freezing where the lithosphere bottoms out as a possible outcome, which fits the row's projected-consequence kind and hypothesised modality.",
          "source_locators": [
            "page:1:block:004",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reads the off-axis shallow swarm as probably tied to magmatism in the crust away from the axis, which is the row's interpretation; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:002",
            "page:5:block:001"
          ]
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block concludes that the mantle under the segment axis is hot, which is what the row's name and interpretation kind assert.",
          "source_locators": [
            "page:1:block:002",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence is the caption line describing the plotted primary-melt carbon dioxide contours, which matches the row's figure-statement kind.",
          "source_locators": [
            "page:1:block:001",
            "page:6:block:005"
          ]
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure-caption block reads the deep earthquakes as volume change from degassing of the ascending melts in hot ductile mantle, which is the row's interpretation; this projection has no statement digest.",
          "source_locators": [
            "page:5:block:002",
            "page:7:block:012"
          ]
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence infers from the depth of the microseismicity that ascending melt sits, fractionates and evolves at those depths, which is the row's interpretation.",
          "source_locators": [
            "page:5:block:002",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence separates primary melts in equilibrium with their source from the pre-eruptive melts that have crystallised on the way up, which matches the row's background-statement kind.",
          "source_locators": [
            "page:1:block:001",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence concludes from the resolution tests that the deep events are demanded by the observations rather than produced by the location procedure, which is the row's interpretation.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:001"
          ]
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block explains the lack of events below twenty kilometres by temperatures too high for rupture to nucleate, offered as a possibility, which fits the row's interpretation kind; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:007"
          ]
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence concludes that magmatism governs crustal accretion at the segment, which is the row's interpretation.",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:002"
          ]
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence records that no active venting has been seen on the segment axis, which matches the row's negated modality and observation kind.",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:002"
          ]
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence records that the segment shows nothing indicating detachment faulting, which matches the row's negated modality.",
          "source_locators": [
            "page:1:block:005",
            "page:4:block:001"
          ]
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence reads the volcanic morphology of the axial valley as showing the segment is magmatic in origin, which is the row's interpretation.",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence in the methods block states that the samples of the studied segment and its southern neighbour were analysed, which matches the row's method-statement kind.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:005"
          ]
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block ends by suggesting that the small pressure rise from degassing of the ascending melt brings on the earthquakes under the segment axis, which is the row's proposed mechanism; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:003"
          ]
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence reports that earlier tomography found ordinary velocity ratios at the segment, which matches the row's prior-observation kind.",
          "source_locators": [
            "page:1:block:005",
            "page:7:block:003"
          ]
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence attributes the enriched basalts and their high volatile contents, as earlier studies read them, to limited melting of an already enriched source near the transform, which matches the row's prior-interpretation kind.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:005"
          ]
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block projects continued degassing during ascent producing earthquakes across the depth interval the row bounds, in the unit it carries, and the hypothesised modality matches the conditional wording.",
          "source_locators": [
            "page:1:block:002",
            "page:5:block:009"
          ]
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The abstract block reports the carbon dioxide quantity of the primary melts over the bounds and in the unit the row carries and marks it approximate as the row does; the calculated modality matches its derivation from sample geochemistry.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports the barium enrichment of the segment's samples as a floor in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:004"
          ]
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the barium-derived pre-eruptive estimate for the segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the barium-derived primary-melt estimate for the segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the calculated carbon dioxide content of melts generated along the segment over the bounds and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:005"
          ]
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the rubidium-derived pre-eruptive estimate for the segment at the bounds and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the rubidium-derived primary-melt estimate for the segment at the bounds and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the estimated pre-eruptive concentrations for the segment over the bounds and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:006"
          ]
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence states a floor on the primary-melt concentration along the segment, which the row records as an open lower bound in the same unit.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence reports the rubidium enrichment of the segment's samples as a floor in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:004"
          ]
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the barium-derived pre-eruptive estimate for the southern segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the barium-derived primary-melt estimate for the southern segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the calculated carbon dioxide content of melts from the southern segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:005"
          ]
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the rubidium-derived pre-eruptive estimate for the southern segment at the bounds and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the rubidium-derived primary-melt estimate for the southern segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the sub-solidus temperature for dry peridotite at the boundary as the approximate value the row carries.",
          "source_locators": [
            "page:5:block:010",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the boundary depth the cold-lithosphere explanation would imply, approximate and in the unit the row carries, and the hypothesised modality matches its conditional framing.",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block ties that same boundary depth to the temperature range the row bounds; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The located sentence in the same block ties the maximum earthquake depth to the isotherm and the tolerance the row carries.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the depth under which the boundary stays shallow away from the axis, which the row records as an open upper bound; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure-caption block ties the drawn boundary to the isotherm value the row carries.",
          "source_locators": [
            "page:1:block:004",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the melt fraction the earlier work needs at the base of the boundary, approximate and in the unit the row carries.",
          "source_locators": [
            "page:5:block:010",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the water content proposed there as a ceiling, which the row records as an open upper bound; this projection has no statement digest.",
          "source_locators": [
            "page:5:block:010",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence puts the boundary under the southern discontinuity at the approximate depth the row carries.",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the age of the crust on the western flank that the row records; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:002",
            "page:2:block:006"
          ]
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the crustal age up to which the boundary stays shallow, approximate and in the unit the row carries; the block names the crust only in adjectival form, which is how the subject occurs there.",
          "source_locators": [
            "page:1:block:002",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the thickness of that western flank crust with the tolerance the row carries.",
          "source_locators": [
            "page:1:block:002",
            "page:2:block:006"
          ]
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure-caption block gives the crustal thickness under the segment with the same tolerance, marked approximate as the row marks it.",
          "source_locators": [
            "page:1:block:002",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the age of the cold lithosphere behind the edge effect, in the unit the row carries.",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ]
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the modelled temperature range across that depth interval, which the row bounds and marks modelled.",
          "source_locators": [
            "page:1:block:002",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block concludes that the earthquakes occur in mantle hotter than the floor the row records as an open lower bound; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:002",
            "page:3:block:002"
          ]
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the age below which accreted crust is treated as young, which the row records as an open upper bound; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:002",
            "page:7:block:009"
          ]
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the length of the segment, approximate and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ]
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the length of the southern segment in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ]
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the southern segment's bearing, which the row records as an approximate angle east of north; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ]
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the temperature floor inferred below twenty kilometres under the segment axis, which the row records as an open lower bound; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:007"
          ]
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL SUBJECT_IN_BLOCK The block gives the bearing of the neo-volcanic ridge in the median valley, which the row records as an angle east of north; this projection has no statement digest.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the length of the eastern part of the transform the network covered, in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:002"
          ]
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the number of events located along the transform, so the quantity the row names and its measured character are supported; this projection carries no count, so the row itself states no value.",
          "source_locators": [
            "page:1:block:005",
            "page:7:block:007"
          ]
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the sub-solidus temperature for dry peridotite at the boundary as the approximate value the row carries.",
          "source_locators": [
            "page:5:block:010",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the boundary depth the cold-lithosphere explanation would imply, approximate and in the unit the row carries, and the hypothesised modality matches its conditional framing.",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block ties that same boundary depth to the temperature range the row bounds; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The located sentence in the same block ties the maximum earthquake depth to the isotherm and the tolerance the row carries.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the depth under which the boundary stays shallow away from the axis, which the row records as an open upper bound; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure-caption block ties the drawn boundary to the isotherm value the row carries.",
          "source_locators": [
            "page:1:block:004",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the melt fraction the earlier work needs at the base of the boundary, approximate and in the unit the row carries.",
          "source_locators": [
            "page:5:block:010",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the water content proposed there as a ceiling, which the row records as an open upper bound; this projection has no statement digest.",
          "source_locators": [
            "page:5:block:010",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence puts the boundary under the southern discontinuity at the approximate depth the row carries.",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The abstract block reports the deep earthquakes across the depth interval the row bounds, in the unit it carries, and the measured modality matches the observational framing.",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:002"
          ]
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block projects continued degassing during ascent producing earthquakes across the depth interval the row bounds, in the unit it carries, and the hypothesised modality matches the conditional wording.",
          "source_locators": [
            "page:1:block:002",
            "page:5:block:009"
          ]
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the age of the crust on the western flank that the row records; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:002",
            "page:2:block:006"
          ]
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the crustal age up to which the boundary stays shallow, approximate and in the unit the row carries; the block names the crust only in adjectival form, which is how the subject occurs there.",
          "source_locators": [
            "page:1:block:002",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 129,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the thickness of that western flank crust with the tolerance the row carries.",
          "source_locators": [
            "page:1:block:002",
            "page:2:block:006"
          ]
        },
        {
          "row_index": 130,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure-caption block gives the crustal thickness under the segment with the same tolerance, marked approximate as the row marks it.",
          "source_locators": [
            "page:1:block:002",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 131,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the age of the cold lithosphere behind the edge effect, in the unit the row carries.",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ]
        },
        {
          "row_index": 132,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the modelled temperature range across that depth interval, which the row bounds and marks modelled.",
          "source_locators": [
            "page:1:block:002",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 133,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block concludes that the earthquakes occur in mantle hotter than the floor the row records as an open lower bound; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:002",
            "page:3:block:002"
          ]
        },
        {
          "row_index": 134,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the age below which accreted crust is treated as young, which the row records as an open upper bound; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:002",
            "page:7:block:009"
          ]
        },
        {
          "row_index": 135,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The abstract block reports the carbon dioxide quantity of the primary melts over the bounds and in the unit the row carries and marks it approximate as the row does; the calculated modality matches its derivation from sample geochemistry.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 136,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the bearing along which the deep events under the segment axis line up, approximate as the row records it.",
          "source_locators": [
            "page:1:block:005",
            "page:4:block:003"
          ]
        },
        {
          "row_index": 137,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence records that nothing is seen below that depth under the segment's ridge axis, which matches the row's negated modality and its open lower bound.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:007"
          ]
        },
        {
          "row_index": 138,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the depth the off-axis shallow microseismicity reaches west of the segment axis, which the row records as an open upper bound.",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 139,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports the barium enrichment of the segment's samples as a floor in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:004"
          ]
        },
        {
          "row_index": 140,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the barium-derived pre-eruptive estimate for the segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 141,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the barium-derived primary-melt estimate for the segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 142,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the calculated carbon dioxide content of melts generated along the segment over the bounds and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:005"
          ]
        },
        {
          "row_index": 143,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the rubidium-derived pre-eruptive estimate for the segment at the bounds and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 144,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the rubidium-derived primary-melt estimate for the segment at the bounds and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 145,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the depth range of the deep earthquakes observed under the segment axis that the row bounds, in the unit it carries.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:006"
          ]
        },
        {
          "row_index": 146,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the approximate depth range over which the deep microseismicity sits under the segment's own ridge axis, in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ]
        },
        {
          "row_index": 147,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the length of the segment, approximate and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ]
        },
        {
          "row_index": 148,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the estimated pre-eruptive concentrations for the segment over the bounds and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:006"
          ]
        },
        {
          "row_index": 149,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence states a floor on the primary-melt concentration along the segment, which the row records as an open lower bound in the same unit.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 150,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence reports the rubidium enrichment of the segment's samples as a floor in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:004"
          ]
        },
        {
          "row_index": 151,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the barium-derived pre-eruptive estimate for the southern segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 152,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the barium-derived primary-melt estimate for the southern segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 153,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the calculated carbon dioxide content of melts from the southern segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:005"
          ]
        },
        {
          "row_index": 154,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the rubidium-derived pre-eruptive estimate for the southern segment at the bounds and in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 155,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the rubidium-derived primary-melt estimate for the southern segment over the bounds and in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 156,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the length of the southern segment in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ]
        },
        {
          "row_index": 157,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the southern segment's bearing, which the row records as an approximate angle east of north; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ]
        },
        {
          "row_index": 158,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the temperature floor inferred below twenty kilometres under the segment axis, which the row records as an open lower bound; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:007"
          ]
        },
        {
          "row_index": 159,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the length of the eastern part of the transform the network covered, in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:002"
          ]
        },
        {
          "row_index": 160,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the number of events located along the transform, so the quantity the row names and its measured character are supported; this projection carries no count, so the row itself states no value.",
          "source_locators": [
            "page:1:block:005",
            "page:7:block:007"
          ]
        },
        {
          "row_index": 161,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL SUBJECT_IN_BLOCK The block gives the bearing of the neo-volcanic ridge in the median valley, which the row records as an angle east of north; this projection has no statement digest.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 162,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the length of the eastern part of the transform the network covered, in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:002"
          ]
        },
        {
          "row_index": 163,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the number of events located along the transform, which is the count and the scope the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:7:block:007"
          ]
        },
        {
          "row_index": 164,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The abstract block reports the deep earthquakes across the depth interval the row bounds, in the unit it carries, and the measured modality matches the observational framing.",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:002"
          ]
        },
        {
          "row_index": 165,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the bearing along which the deep events under the segment axis line up, approximate as the row records it.",
          "source_locators": [
            "page:1:block:005",
            "page:4:block:003"
          ]
        },
        {
          "row_index": 166,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence records that nothing is seen below that depth under the segment's ridge axis, which matches the row's negated modality and its open lower bound.",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:007"
          ]
        },
        {
          "row_index": 167,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the depth the off-axis shallow microseismicity reaches west of the segment axis, which the row records as an open upper bound.",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 168,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the depth range of the deep earthquakes observed under the segment axis that the row bounds, in the unit it carries.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:006"
          ]
        },
        {
          "row_index": 169,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the approximate depth range over which the deep microseismicity sits under the segment's own ridge axis, in the unit the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ]
        },
        {
          "row_index": 170,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the length of the eastern part of the transform the network covered, in the unit the row carries; this projection has no statement digest.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:002"
          ]
        },
        {
          "row_index": 171,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the number of events located along the transform, which is the count and the scope the row carries.",
          "source_locators": [
            "page:1:block:005",
            "page:7:block:007"
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
