# Malleus paper v4 run-11 source-grounded review record

Template. The row counts are substituted at freeze, from the frozen cell's own
query result, at the same time as `paper-v4/evaluation-v4/review-task-v3.template.md`.
No placeholder may survive instantiation.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

Fill one `rows` entry per returned row, in order, zero-based: 60 for
CQ-01, 123 for CQ-02, 145 for CQ-03, 129 for
CQ-04, 457 in all. Cite reading block ids only. Write the reasons in
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
    "review_input_manifest_sha256": "sha256:bff60ce546c84ae9a320e9762df836cb9f10875ffc85f8cc01044a89b9e13342"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-preliminary-run-11",
    "completed_at": "2026-09-05T10:30:35Z"
  },
  "questions": [
    {
      "question_id": "CQ-01",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "The rows name the acquiring campaign and the seafloor seismometer network, carry the deployed instrument count with an explicit scope on the campaign record, tie the network to the campaign through a relation row, and describe the acquisition itself through the detection and location methods and the resulting data resources. Every part the question asks for is therefore addressed. The remaining rows are software packages, funding bodies and author affiliations that the type-only binding drew in and that bear on nothing the question asks; they are noise rather than a competing answer. The deployed count and the count of instruments that yielded usable data are separately scoped on separate records, so the two numbers do not conflict.",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002",
        "page:2:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Both cited blocks name the cruise and state the same number of seafloor seismometers forming the deployed network, which is precisely the scope the row's count carries."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:008"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The data-availability block names the raw seismic recordings and cruise reports as an obtainable resource and gives the same access address the row projects."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The methods block names the rock-sample database and its web address exactly as the row projects them."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:008",
            "page:8:block:009"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The repository is named in the first cited block and its digital object identifier runs across the block boundary into the second, so the two blocks together carry the projected identifier."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The results block introduces the seafloor seismometer network under the abbreviation the row uses as its name, and the figure caption block uses the same abbreviation for the deployed instruments."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The code-availability block lists this mapping package among the software used for structural analysis, and the name is the whole of the row's projection."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010",
            "page:8:block:011"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The code-availability block names the plotting toolbox with its major version, which is the projected name."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The focal-mechanism block and the code-availability block both name this package, matching the row's only projected field."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The relocation block and the code-availability block both name this program, which is all the row projects."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004",
            "page:7:block:007",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The location and station-correction blocks and the code-availability block all name this program, matching the projected name."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002",
            "page:8:block:002",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Detection, magnitude and code-availability blocks all name this analysis package, which is the row's only claim."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The velocity-model block and the code-availability block both name this inversion program, matching the projection."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The magnitude block and the code-availability block both name this catalogue-analysis software, which is the whole projection."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The discussion block names the carbon-dioxide solubility model it applies to the melt, which is the projected method name."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:7:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The results block and the relocation block both describe relocating events by the differencing method the row names."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The focal-mechanism block describes determining mechanisms from first-motion polarities of the compressional phase, which is the projected method name."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The magnitude block names the local magnitude scale used, matching the projection."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:7:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The results block names a non-linear location algorithm for the hypocentres and the methods block describes the same non-linear search, so the projected name holds."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Both cited blocks describe automatic arrival detection with the short-term over long-term average trigger the row names."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The title block's byline carries this author's name, and the byline is a list of people, which supports the projected agent type."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:044"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The acknowledgements block names this regional body among the funders, which supports both the name and the organisation type."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The byline carries this author's name among the people credited, supporting the name and the person type."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The affiliation block names this institute in full as an author affiliation, which supports the name and the organisation type."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The byline carries this author's name; the text layer spaces the letters out, but read as prose it is the same name, and the byline supports the person type."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:044"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The acknowledgements block names this funding council, supporting the name and the organisation type."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:044"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The acknowledgements block credits the national government among the funders under the name the row projects."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The affiliation block names this research unit with its identifier as an author affiliation, supporting name and organisation type."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006",
            "page:10:block:044"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The affiliation block gives this institute's full name and the acknowledgements block refers to it again by initials, supporting the projected name and type."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:044"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The acknowledgements block names this graduate-school project as a funder, supporting the projected name and type."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The byline lists this author fourth, with an affiliation marker attached, so the name and the person type both hold on that block."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The byline lists this author among the last three names, carrying an affiliation marker, which supports the name and the person type."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The byline opens its second line with this author's name and affiliation marker, supporting the name and the person type."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:044"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The acknowledgements block names this national funding body with its grant numbers, supporting name and organisation type."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:11:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The byline carries this author's name and the correspondence block repeats it, supporting name and person type."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The affiliation block names this institute as an author affiliation, supporting name and organisation type."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:044"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The acknowledgements block credits this national fleet infrastructure with funding the ship time, supporting name and organisation type."
        },
        {
          "row_index": 36,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The affiliation block does place an Italian university among the author affiliations, so the organisation type holds, but the block names it with its city and the row's name field keeps only the generic first word, cut where the affiliation list breaks across a line. The identifying part of the name is not what the reading gives."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The affiliation block names this university as an author affiliation, supporting name and organisation type."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:044"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The acknowledgements block names this provincial funding body with its grant number, supporting name and organisation type."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:11:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The byline carries the first author's name and the correspondence block repeats it, supporting name and person type."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The code-availability block names this mapping package and gives the same download address the row projects; no version is claimed."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010",
            "page:8:block:011"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The code-availability block names the toolbox with its major version, and its download address runs across the block boundary into the following block, so the two blocks carry the whole projected address."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The code-availability block gives this package's name, its version in parentheses and the address the row projects."
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The code-availability block gives this program's version and address and the relocation block names it in use, covering every projected field."
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The code-availability block names this location program and gives the address the row projects; no version is claimed."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The code-availability block names this phase-picking package and gives the projected address."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The code-availability block names this inversion program and gives the projected address."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The code-availability block names this catalogue-analysis software and gives the projected address."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DERIVATION_LOCAL The relation and both endpoints are formalised from the same results block, which states that the microseismicity was acquired by the seismometer network during that cruise, so the network belongs to the campaign on the reading."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:046",
            "page:1:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The contributions block credits this author, by initials, with taking part in data collection during the cruise, and the byline block ties those initials to a single author, so the contribution link holds."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:046",
            "page:1:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The contributions block credits this author's initials with participation in the cruise data collection, and the byline block resolves those initials to the named author, so the link holds on the reading."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:046",
            "page:10:block:045"
          ],
          "rationale": "DERIVATION_LOCAL The sentence crediting the design of the project runs across a block boundary: the block the derivation reaches carries the predicate and the campaign, while the two sets of initials that are its subject sit at the end of the preceding block. Read together the two blocks support this author designing the campaign."
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:046",
            "page:1:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The contributions block lists this author's initials among those who took part in data collection during the cruise, and the byline resolves the initials."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:046",
            "page:1:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The contributions block lists this author's initials among the cruise data collectors, and the byline resolves the initials to one author."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:046",
            "page:10:block:045"
          ],
          "rationale": "DERIVATION_LOCAL As with the other design credit, the crediting sentence is split: the initials naming this author close the preceding block and the predicate about designing the project opens the block the derivation reaches. The pair supports the link."
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:044"
          ],
          "rationale": "DERIVATION_LOCAL The acknowledgements block states that the ship time for the cruise was funded through this fleet infrastructure, which supports a funding link from that body to the campaign; the reading limits the funding to ship time and the row projects no narrower scope."
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block gives the network's instrument spacing with the approximation marker the row keeps, in kilometres, so the value, unit and qualification hold. The token is non-local because the instrument record is formalised only from two page-two blocks, not from this one. The subject's short name appears in this block."
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block states the minimum number of seismometers an event had to be seen on during manual checking, which matches the row's open lower bound and its stated scope. The instrument record is formalised elsewhere, hence non-local, and the subject's short name occurs here."
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The relocation block states that every relocated event was detected on more than six instruments, which is the row's open lower bound and scope. The subject record is formalised from page-two blocks, so the pointer is non-local, and the subject's short name appears in this block."
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The results block gives the number of usable instruments used for automatic detection as an exact count, and the methods block repeats the same number; the subject record is also formalised from the first of these blocks, and the subject's short name appears there."
        }
      ]
    },
    {
      "question_id": "CQ-02",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "The named ridge subsection carrying the deep events is present both as a record of its own, with its feature kind, and as the subject of the observations that place the events under its axis at mantle depths, so the named region, the earthquake population and the position of the events relative to the axis are all addressed by rows rather than left to inference. Two limits belong on the record without changing the label. The relation rows come back with an empty projection, so the geologic relations carry no spatial qualifier of their own, and none of them links an earthquake population to a ridge axis; the spatial part of the answer is therefore read from the observations' quantity descriptions and their subject links. The claim rows carry no statement text either, reaching their words only through the assertion locator and digest into the retained capture, which the task directs the reviewer to open. Neighbouring segments, discontinuities and other ridges also appear, but nothing in the rows places deep microseismicity anywhere but under the one subsection, so there is no competing answer.",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:004",
        "page:2:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The second cited block observes a cluster on the western side of the axial valley and so names the feature; the first block, from which the record also draws, describes the same valley in the segment where it lies."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The introduction block defines the brittle-ductile boundary and gives it the abbreviation the row uses as a name; calling it a boundary is what that definition does."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The study-area block names this transform fault as one of the two bounding the ridge segment, in the abbreviated form the row projects."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Both cited blocks refer to the crust as a distinct layer, the first in defining the boundary above it and the second in giving its thickness, which supports the bare name the row projects."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The study-area block describes a westward dipping detachment fault bounding the intersection segment, supporting both the name and the feature kind."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The study-area block places the study in this ocean region under exactly the name the row projects."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The discussion block names this ultraslow-spreading ridge as one of the places where deep mantle earthquakes have been seen."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The figure caption block reports an inactive hydrothermal mound inferred from submersible dive observations, which is both the name and the description the row projects."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The discussion block reports an extinct hydrothermal vent field on the eastern flank of the first discontinuity, supporting the name and the feature kind including its extinct qualifier."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001",
            "page:3:block:003"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block the derivation reaches describes the high-angle inward dipping faults with the orientation the description gives; the clause naming the ten-kilometre-wide axial valley they bound closes the preceding block, so the two together carry the whole description."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The discussion block spells out the lithosphere-asthenosphere boundary and introduces the abbreviation the row uses as a name; treating it as a boundary is the reading's own framing."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Both cited blocks refer to the lithosphere as a layer, the first in the brittle-ductile definition and the second in the cold-edge argument, supporting the bare name."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Both cited blocks locate processes in the mantle, one placing the earthquakes there and the other giving its temperature, which supports the projected name."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The study-area block names the ridge in full and defines its abbreviation, and the figure caption block repeats the expansion, so the projected full name holds."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The schematic caption block refers to the expected crust-mantle interface by this name, supporting the name and the feature kind."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The tectonics block describes an oriented neo-volcanic ridge in the segment's median valley, which is the projected name."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The tectonics block describes the core complex surface as heavily cut by normal faults with the two strike directions the description gives, supporting name and description."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The study-area block names the first non-transform discontinuity with the label the row projects and identifies it as such a discontinuity."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The study-area block names the second non-transform discontinuity with the label the row projects and identifies it as such a discontinuity."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The study-area block names the oceanic core complex in full with the abbreviation the row uses, supporting name and feature kind."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The methods block on maximum earthquake depth names this massif and places it at a non-transform discontinuity, supporting the projected name."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The study-area block names the intersection segment with this label and calls it a segment, which is the projected feature kind."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The study-area block introduces this label for a short ridge segment, supporting both the name and the feature kind."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The study-area block names the ridge segment south of the second discontinuity with this label, supporting name and feature kind."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The study-area block names this transform fault in the plural abbreviation it shares with its neighbour, and the figure caption block refers to the same transform and to major transform faults, so the projected name and feature kind hold; the reading uses the abbreviation rather than the exact string the row carries."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The study-area block names the ridge-transform intersection in full and gives the abbreviation the row projects as a name."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The study-area block opens by locating the study area, which is the generic name the row projects; the text layer spaces the words out but reads as that phrase."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:5:block:009"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The first cited block names the Southwest Indian Ridge in full with the abbreviation the row projects, and the second uses the abbreviation again."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DERIVATION_LOCAL The relation and both endpoints come from the same introduction block, which places the cooled brittle lithosphere above the partially molten crust, so the pairing and its vertical sense hold on the reading."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The block states that the core complex surface is cut by the normal faults that are the other endpoint, so the pairing holds; the fault record is formalised from this same block."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL The figure caption block places the oceanic core complex on the outside corner of the ridge, which supports the pairing; the ridge record is also formalised from this block."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The block states that the intersection segment is bounded to the east by a detachment fault, and both endpoints are formalised from that same block."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_NON_LOCAL The block the relation derives from places the segment immediately south of the first discontinuity, which supports the adjacency. The token is non-local because both endpoints are formalised only from the study-area block on page one, which the relation's own pointer does not reach."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The block states that the segment is bounded by the high-angle inward dipping faults that are the other endpoint, and the fault record is formalised from the same block."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The block names the ridge segment lying south of the second discontinuity, which is the pairing; both endpoints are formalised from it."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The block places the study area within the ridge segment between the two transforms, supporting a part-whole pairing; both endpoints are formalised from it."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DERIVATION_LOCAL The block places the extinct vent field on the eastern flank of the first discontinuity, which is the pairing; the vent-field record is formalised from this block."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:005",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence records that the authors analysed the samples of this segment and of its southern neighbour, which is a plain statement and matches the projected modality. The subject label appears in the block. The claim covers two segments while the row attaches it to one, which is a narrowing, not a conflict. The pointer is non-local because the segment record is formalised from the study-area block only."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence characterises the axial valley floor as bathymetric highs cut by ridge-parallel faults with basaltic constructions, stated flatly, so the modality holds and the subject is named in the block. The subject record is formalised from two page-two blocks, hence the non-local token."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence explicitly suggests that the ridge axis is relocating from the core complex termination towards the faulted dome, which supports both the hypothesised modality and the suggestion kind; the core complex is named in the block. Its record is formalised from the study-area block, hence non-local."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence says the boundary is expected to shallow southward, an expectation rather than an observation, which matches the hypothesised modality; the abbreviation is in the block. The boundary record is formalised from the introduction block, hence non-local."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The abstract sentence is an explicit suggestion that the deep mantle earthquakes result from carbon-dioxide degassing, supporting both the hypothesised modality and the suggestion kind, and it names the mantle. The mantle record is formalised from later blocks, hence non-local."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:002",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence presents this as the fourth possibility and marks it as the authors' preferred one, which supports the projected name, the possibility kind, the preferred disposition and the hypothesised modality; the segment label is in the block. The segment record is formalised from the study-area block, hence non-local."
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence projects continued degassing producing earthquakes in the mantle as the melt rises, phrased conditionally, which fits the hypothesised modality and an interpretive reading; the mantle is named in the block. Non-local because the mantle record is formalised elsewhere."
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The opening sentence states flatly how oceanic crust forms, matching the stated modality, and names the crust. The crust record is formalised from other blocks, hence the non-local token."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:012",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_NOT_IN_BLOCK The schematic caption block interprets the deep events beneath the ridge axis as a consequence of volume change from degassing, which supports the hypothesised modality and the interpretation kind. The block uses only the ridge's abbreviation, not the full name the row's subject projection carries, so the subject is not literally in it; the second cited block is where the reading expands that abbreviation."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence reports the measured alignment of the deep events beneath the segment axis along a single direction, which fits the measured modality and names the segment. The segment record is formalised from the study-area block, hence non-local."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:001",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence states that the deep events beneath the ridge axis are well constrained and not artifacts, a flat statement matching the modality, with the segment label in parentheses in the block. Non-local for the same reason as the other segment-subject rows."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence states the mechanism, that degassing causes volume change which under extension triggers deep mantle earthquakes, in declarative form, which matches the stated modality; the mantle is named in the block. Non-local because the mantle record is formalised from other blocks."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The located sentence denies that the maximum earthquake depth here follows the usual depth against spreading-rate relationship, which supports the negated modality; the block also carries the expansion of the ridge abbreviation, so the subject occurs in it. The sentence continues into the following block, which is cited for completeness."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_NOT_IN_BLOCK The located sentence infers from a shallow off-axis cluster that the unexpected depths beneath the ridge axis are not a location artifact, an inference marked as such, which fits the hypothesised modality and the suggestion kind. The block names the ridge only by its abbreviation, so the subject's full name is not in it; the second cited block is where the reading expands that abbreviation."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence infers from missing deep seismicity near the termination that the detachment fault is inactive, explicitly a suggestion, and it names the fault. The fault record is formalised from the study-area block, hence the non-local token."
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The located sentence places most of these earthquakes in the mantle below ten kilometres as an inference from crustal thickness, matching the hypothesised modality; the mantle is named in the block, and the mantle record is itself formalised from this block."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence states that seafloor peridotites indicate exhumed mantle, a flat statement naming the mantle. The mantle record is formalised from other blocks, hence non-local."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_NOT_IN_BLOCK The located sentence rules the fastest velocity model out for locating events beneath the ridge axis, which supports the negated modality. The block uses only the ridge abbreviation, so the projected full name is absent from it; the second cited block carries the expansion."
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The schematic caption states plainly that three segments are drawn southward from this transform, which is a stated claim naming the transform. Its record is formalised from earlier blocks, hence non-local."
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002",
            "page:5:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The first cited block introduces this as the third possibility, associating the deep mantle earthquakes with magmatic-tectonic activity, and the second concludes that the melt-movement mechanism does not apply here, which is what the not-supported disposition records. The mantle is named in the first block; the mantle record is formalised elsewhere, hence non-local."
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence states that magmatism dominates crustal accretion at this segment and that the events occur in hot mantle, a flat conclusion naming the segment. Non-local because the segment record is formalised from the study-area block."
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The located sentence derives the mantle temperature at these depths from thermal modelling, which is what the calculated modality records, and names the mantle; the mantle record is also formalised from this block."
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_NOT_IN_BLOCK The abstract sentence projects that a large carbon-dioxide concentration in the primitive melt will influence the presence of melt beneath the lithosphere-asthenosphere boundary, forward-looking and so hypothesised. The block spells the boundary out but never uses the abbreviation the subject projection carries, which is why the subject token is negative; the second cited block is where the reading introduces that abbreviation."
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001",
            "page:5:block:010"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence suggests that melt at the boundary could be due to combined carbon dioxide and water, a conditional claim matching the hypothesised modality, and it uses the abbreviation the subject carries. The boundary record is formalised from the earlier block, hence non-local."
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001",
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence proposes that melt could freeze at the base of the lithosphere, conditional and so hypothesised, and names the lithosphere. Its record is formalised from other blocks, hence non-local."
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence infers from the observed depth range that ascending melt resides, fractionates and evolves in the mantle, explicitly a suggestion, and names the mantle. Non-local because the mantle record is formalised elsewhere."
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:003",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The introduction sentence denies any clear understanding of how melts migrate through the upper mantle, which is the negated modality, and names the mantle. Non-local for the same reason as the other mantle rows."
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods sentence lists the one-dimensional velocity models built for the flanks and valley of this transform, a flat statement naming it. Its record is formalised from earlier blocks, hence non-local."
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block introduces this as another hypothesis, localised high strain in mantle shear zones, and in the same block states that the observations do not support it, which carries the projected name, hypothesis kind and not-supported disposition. The mantle is named there; its record is formalised elsewhere, hence non-local."
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence denies any observation of active vents on this segment's axis, which is the negated modality, and names the segment. Non-local because the segment record is formalised from the study-area block."
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence denies evidence of a current eruption in the axial valley, matching the negated modality, and names the valley. The valley record is formalised from page-two blocks, hence non-local."
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence attributes the shallow events beneath the dome to likely ruptures on high-angle faults, a hedged inference matching the hypothesised modality, and names the core complex. Non-local because that record is formalised from the study-area block."
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence states that the volcanic morphology indicates this segment is of magmatic origin, a flat statement naming the segment. Non-local for the usual reason."
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence says a localised high-strain shear zone in the deep mantle can be expected during detachment development, an expectation and so hypothesised, and names the mantle. Non-local because the mantle record is formalised elsewhere."
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence is an explicit suggestion that the small pressure rise from degassing induces the events beneath this segment's axis, matching the hypothesised modality and the suggestion kind, and it names the segment. Non-local for the usual reason."
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_NOT_IN_BLOCK The located sentence states plainly that the record is a brief snapshot in time along this supersegment, which matches the stated modality. The block uses only the ridge abbreviation, so the projected full name is absent from it; the second cited block carries the expansion."
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:003",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence reports that tomography also indicates normal velocity ratios in this segment, a flat statement naming it. Non-local for the usual reason."
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The located sentence attributes to earlier work the suggestion that volatiles flush melt towards the boundary, which is hypothesised, and it is the same sentence that introduces the abbreviation, so the subject is in the block and the pointer is local."
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The abstract reports the deep earthquakes at the depth range and unit the row carries, in the mantle along the ridge axis, and names the ridge in full; the plain range with no approximation marker matches the exact qualification. The ridge record is formalised from later blocks, hence non-local."
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the boundary depth that the cold-and-thick-lithosphere explanation would require, with an approximation marker, which matches the value, unit, qualification and hypothesised modality; the abbreviation is in the block. Non-local because the boundary record is formalised from the introduction block."
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the boundary depth revealed beneath the second discontinuity with an approximation marker, matching the value, unit and qualification; the abbreviation is in the block. Non-local for the same reason."
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence states that the boundary stays shallower than the projected upper bound off-axis, which is exactly an open upper bound in the same unit; the abbreviation is in the block. Non-local for the same reason."
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block gives this barium-based pre-eruptive estimate for the segment with the same bounds and unit, and the same block establishes that these are pre-eruptive melt estimates from a fixed ratio, which matches the calculated modality and the estimated determination. Non-local because the segment record is formalised from the study-area block."
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same methods block gives the barium-based pre-eruptive estimate for the southern segment with the bounds and unit the row carries, and the estimation is described in that block. Non-local for the usual reason."
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block gives the barium-based primary-melt estimate for this segment with the same bounds and unit, and describes it as an estimate for melts in equilibrium with the mantle source, matching the modality and determination. Non-local for the usual reason."
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same sentence gives the barium-based primary-melt estimate for the southern segment with the bounds the row carries; the projected name is the shorthand the block uses for the corrected barium concentration. Non-local for the usual reason."
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The results block gives the calculated volatile content of melts generated along this segment with the same bounds and unit and marks it as calculated, matching the modality and the estimated determination; the segment is named there. Non-local for the usual reason."
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same sentence gives the calculated content for the southern segment with the bounds and unit the row carries and names that segment. Non-local for the usual reason."
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence concludes that the primary-melt concentration along this segment is at least the projected value, which is an open lower bound in the same unit, reached by calculation. Non-local for the usual reason."
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block gives the rubidium-based pre-eruptive estimate for this segment with the same bounds and unit, in the sentence that describes the estimation. Non-local for the usual reason."
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same block gives the rubidium-based pre-eruptive estimate for the southern segment with the bounds the row carries. Non-local for the usual reason."
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the rubidium-based primary-melt estimate for this segment with the same bounds and unit. Non-local for the usual reason."
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same sentence gives the rubidium-based primary-melt estimate for the southern segment with the bounds the row carries. Non-local for the usual reason."
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block gives the age of the crust of the western flank as an exact figure in the unit the row carries, and it is the block from which the crust record is also formalised, so the pointer is local and the subject is named there."
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The first cited block gives the crustal thickness of the western flank with its stated uncertainty in the unit the row carries, from refraction work, which matches the measured modality; the schematic caption repeats the same figure. The crust record is formalised from the first block, so the pointer is local."
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The key-observations sentence places the deep microseismicity at the approximate depth range the row carries, beneath the ridge axis of this segment, and names the segment. Non-local because the segment record is formalised from the study-area block. This is one of the two rows that answer the question directly."
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The discussion sentence reports the average concentration previously estimated at several segments in this ocean region, with the approximation marker and unit the row carries, from ratio-based estimation, which matches the calculated modality. Non-local because the region record is formalised from the study-area block."
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The study-area block gives the half-spreading rate with the value and unit the row carries and names the ridge in full in the preceding sentence, and the ridge record is also formalised from this block, so the pointer is local."
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:012",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_NOT_IN_BLOCK The schematic caption gives the depth range of the deep earthquakes below the sea floor beneath the ridge axis, matching the bounds, unit and measured modality. The block uses only the ridge abbreviation, so the projected full name is absent from it; the second cited block carries the expansion."
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011",
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The cited block states that the boundary drawn from the maximum earthquake depth corresponds to the isotherm at the temperature the row carries, in the same unit. Worth recording: the located sentence in the capture stops just before that clause, so the number is supported by the block rather than by the located fragment alone. The abbreviation is in the block; the boundary record is formalised from the introduction block, hence non-local."
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block gives the age of the cold lithosphere responsible for the edge effect as the value and unit the row carries, and the lithosphere record is also formalised from this block, so the pointer is local."
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK Both the results block and the methods block give the same exact number of located earthquakes, the first placing them in the vicinity of the intersection region, which is the row's subject and is named there. The intersection record is formalised from the study-area block, hence non-local."
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence states that the earthquakes occur in hot mantle above the temperature the row carries, which is an open lower bound in the same unit, and it names the mantle. Non-local because the mantle record is formalised from other blocks."
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_NOT_IN_BLOCK The acquisition sentence gives the length of ridge axis the network covered, with the value and unit the row carries. The block uses only the ridge abbreviation, so the projected full name is absent from it; the second cited block is where the reading expands it."
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007",
            "page:3:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The relocation block gives the number of events located along the ridge as an exact count, and the figure caption block repeats the same total and spells the ridge name out, which is why the subject occurs in a block the derivation reaches. The ridge record itself is formalised from other blocks, hence non-local."
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_NOT_IN_BLOCK The tectonics block gives the width of the segment's median valley with the value and unit the row carries, so the quantity holds. The subject token is negative because that block calls the feature a median valley and the row's subject projection names it the axial valley; the second cited block is where the reading uses the axial-valley wording for the same feature. The pointer is local, since the subject record is also formalised from the first block."
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001",
            "page:5:block:010"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence reports the melt fraction earlier work proposed at the base of the boundary, with the approximation marker and unit the row carries, as a modelled requirement, matching the hypothesised modality and modelled determination; the abbreviation is in the block. Non-local because the boundary record is formalised from the earlier block."
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence denies any earthquakes deeper than the projected bound beneath this segment's axis, which is a negated claim with an open lower bound in the same unit, and it names the segment. Non-local because the segment record is formalised from the study-area block."
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The key-observations sentence gives the depth range of the normal-depth events beneath the southern discontinuity with the bounds and unit the row carries, and names it. Non-local for the usual reason."
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The tectonics block gives the length of the first discontinuity with the approximation marker and unit the row carries, and names it. Non-local because its record is formalised from the study-area block."
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence records that the expected shallow depth range is observed beneath this discontinuity under the projected bound, which is an open upper bound in the same unit, and names it. Non-local for the usual reason."
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the maximum depth of events beneath this discontinuity with the approximation marker and unit the row carries, and names it. Non-local for the usual reason."
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The tectonics block gives the ridge offset of this discontinuity with the approximation marker and unit the row carries, and names it. Non-local for the usual reason."
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same sentence that bounds the discontinuity's depths bounds those beneath the core complex under the projected value, an open upper bound in the same unit, and names the complex. Non-local because that record is formalised from the study-area block."
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports an off-axis cluster on the western side of the axial valley with the shallow focal-depth range the row carries, marked as approximate, and it is the block from which the valley record is also formalised, so the pointer is local and the subject is named there."
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the estimated pre-eruptive concentration range for this segment with the bounds and unit the row carries, arrived at by accounting for fractional crystallisation, which matches the calculated modality and estimated determination. Non-local for the usual reason."
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence gives the barium enrichment of all samples in this segment above the projected value, an open lower bound in the same unit, and names the segment. Non-local for the usual reason."
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The located sentence reports the observed depths of the deep earthquakes beneath this segment's axis with the bounds and unit the row carries, which matches the measured modality, and names the segment. Non-local because the segment record is formalised from the study-area block. With the shallower depth row this is what answers the question's second half."
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The tectonics block gives this segment's length with the approximation marker and unit the row carries, and names it. Non-local for the usual reason."
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same enrichment sentence gives the rubidium concentration of the segment's samples above the projected value, an open lower bound in the same unit. Non-local for the usual reason."
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The tectonics block gives the southern segment's length as an exact figure in the unit the row carries and names it. Non-local for the usual reason."
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The acquisition sentence gives the length of the transform covered by the network, with the value and unit the row carries, and names the transform in the abbreviated form the subject projection uses. Non-local because the transform record is formalised from other blocks."
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007",
            "page:3:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The relocation block gives the number of events located along the transform as an exact count and names it; the figure panel block the derivation also reaches carries the same total. Non-local because the transform record is formalised from other blocks."
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The key-observations sentence gives the depth range of the shallow events on the outside corner of the intersection with the bounds and unit the row carries, and names the intersection. Non-local for the usual reason."
        },
        {
          "row_index": 121,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:6:block:001",
            "page:5:block:010"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The quantity holds: the located sentence gives the sub-solidus temperature at which melt is present for anhydrous peridotite at the boundary, with the approximation marker and unit the row carries, and the abbreviation the subject projection uses is in the block. What is not supported is the projected name, which is the first half of a word split across a line in the text layer and is not a term the reading offers. Non-local because the boundary record is formalised from the earlier block."
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports the highest melt concentration previously reported at this ridge as the value and unit the row carries, and names it; the record is also formalised from this block, so the pointer is local. Worth recording: the located sentence in the capture ends just before the figure in parentheses, so the number rests on the block rather than on the located fragment alone."
        }
      ]
    },
    {
      "question_id": "CQ-03",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "Every part the question asks for is present in the rows and correctly bound to a subject. The earthquake-depth range for the segment the paper treats as central appears as an approximate 10 to 20 km observation and as an exact 16 to 19 km observation, each with the kilometre unit and a measured modality; the calculated primary-melt CO2 range appears as 0.4 to 3.0 wt% from barium and 0.5 to 2.8 wt% from rubidium, each with the weight-per-cent unit, a calculated modality and an estimated determination, and there is a separate open lower bound at 0.4 wt%. The residual is dilution rather than absence: the binding is type-only, so the same set also carries the adjacent segment's ranges, the pre-eruptive rather than primary values, and many quantities with no bearing on the question, and the rows do not themselves mark which pairing the question calls central. Each candidate is nonetheless separable by its subject reference and its quantity kind without leaving the row set.",
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
            "page:8:block:008"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The data-availability block names the cruise reports together with the unprocessed seismic recordings, and carries the repository address the row projects."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The methods block names the database and gives the address the row projects."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:008",
            "page:8:block:009"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The data-availability block names the repository and begins the deposit identifier, which the following block completes; both are cited."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:2:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block that supplies the name uses it for the structure west of which the off-axis cluster sits; the projection carries nothing else to check."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The introduction block defines the brittle-ductile boundary and abbreviates it, which gives both the name and the boundary kind the row projects."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names this transform alongside the Romanche as the bound of the ridge segment studied."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Both cited blocks use the noun, one contrasting it with the lithosphere above and one dating and measuring the western flank."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the westward-dipping detachment bounding the intersection segment, which is the feature kind the row projects."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block places the study in this ocean region by name."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names this ridge alongside the Southwest Indian Ridge as an ultraslow case with deep mantle events."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The figure-caption block describes the inactive mound and the dive observations behind it, which is what the row's description asserts."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports the extinct vent field on the eastern flank of the northern discontinuity, giving both the name and the kind."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block describes the high-angle inward-dipping faults and their orientation, which is what the row's description asserts."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block spells out the lithosphere-asthenosphere boundary and abbreviates it, giving the name and the boundary kind."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Both cited blocks use the noun, one for the brittle lithosphere above the melt and one for the cold 45 Ma lithosphere."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Both cited blocks use the noun for the layer the deep events are placed in."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the ridge in full and gives its abbreviation; the caption block repeats the expansion."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The caption block names the expected Moho interface, which is the kind the row projects."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the neo-volcanic ridge in the segment's median valley and gives its orientation."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block describes the normal faults cutting the core complex surface with the strikes the row's description carries."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block introduces the first non-transform discontinuity and names it, giving the name and the kind."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The same block introduces the second non-transform discontinuity and names it."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the oceanic core complex and abbreviates it, giving the name and the kind."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The methods block names this massif and places it at a non-transform discontinuity."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the intersection segment, which is the segment kind the row projects."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the short ridge segment between the two discontinuities, which is the kind the row projects."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The same block names the ridge segment south of the second discontinuity."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the transform; the caption block that supplies the row's feature kind calls the major structures of the region transform faults."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the eastern ridge-transform intersection and abbreviates it."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block uses the phrase for the region it then locates and measures."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:5:block:009"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW One cited block spells out the Southwest Indian Ridge with its abbreviation, the other uses the abbreviation."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the solubility model used to place the saturation pressure and depth."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:7:block:006",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW All three cited blocks name the double-difference relocation, in the results, in the methods and in the code list."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The methods block names the first-motion polarity approach used for the focal mechanisms."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The methods block names the local magnitude scale used for the magnitudes."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:7:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Both cited blocks name the non-linear location algorithm used for the initial hypocentres."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Both cited blocks name the short-term over long-term average trigger used for detection."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:8:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Both cited blocks give the ratio as 81.3 with an uncertainty of 23 and identify the two elements, which is what the row projects."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:8:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Both cited blocks give the ratio as 991 with an uncertainty of 129 and identify the two elements."
        },
        {
          "row_index": 39,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block gives the ratio as approximately 1.7 from Wadati diagrams; the row carries 1.7 flat, with no uncertainty and no approximation marker, so the source's hedge is dropped where the projection had a slot for imprecision."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records basalts observed on the seafloor of the segment, which gives the name and the material."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The figure-caption block names melt inclusions as one of the sample groups plotted."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:6:block:005",
            "page:8:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited blocks name the compiled mid-ocean-ridge basalt samples and the network bounds they were drawn within."
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006",
            "page:7:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records peridotites observed on the seafloor of the intersection segment."
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The figure-caption block names popping rocks as one of the plotted sample groups."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records basalts observed on the seafloor; this projection carries the name alone."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The figure-caption block names melt inclusions among the plotted groups; this projection carries the name alone."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:6:block:005",
            "page:8:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited blocks name the compiled mid-ocean-ridge basalt samples; this projection carries the name alone."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006",
            "page:7:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records peridotites observed on the seafloor; this projection carries the name alone."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The figure-caption block names popping rocks among the plotted groups; this projection carries the name alone."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ],
          "rationale": "DERIVATION_LOCAL The block separates the cooled brittle layer from the partly molten material beneath it, which is the overlying relation and the qualifier the row carries; that same block formalises both endpoints."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The block says the core complex surface is cut by those normal faults; the relation's block is where the fault endpoint is formalised."
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL The caption block places the core complex on the outside corner of the ridge, giving the relation and the qualifier; that block also formalises the ridge endpoint."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The block bounds the intersection segment to the east by the detachment; the relation and both endpoints are formalised in that one block."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL The block places the segment south of the northern discontinuity, so the pairing holds on the reading; the relation's block is not among the blocks that formalise either endpoint, both of which are introduced a block earlier."
        },
        {
          "row_index": 55,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:4:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The block says the inward-dipping faults bound the segment's axial valley rather than the segment itself, and the graph carries that valley as a feature of its own, so the endpoint the row names is a step removed from what the prose bounds; the relation's block does formalise the fault endpoint."
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The block names the ridge segment lying south of the second discontinuity; the relation and both endpoints are formalised there."
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL The block places the study area in the northern part of the ridge segment; the relation and both endpoints are formalised there."
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:002"
          ],
          "rationale": "DERIVATION_LOCAL The block puts the extinct vent field on the eastern flank of the northern discontinuity; that block also formalises the vent-field endpoint."
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports the authors analysing samples from this segment and its southern neighbour, in the plain indicative the row's stated modality records, and names the segment."
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:2:block:006",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block describes the valley floor's bathymetric highs, faulting and basaltic constructions as observed fact, which matches the stated modality, and names the valley."
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block draws a suggestion that the ridge axis is shifting east beneath the core complex dome, which is the hedge the hypothesised modality and the suggestion kind record; the complex is named there."
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block frames the southward shallowing of the boundary as an expectation rather than a finding, which is what the hypothesised modality carries; the boundary is named by abbreviation."
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:2:block:006",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The abstract block carries the authors' own suggestion that deep mantle earthquakes follow from CO2 degassing; the hedge is explicit and the mantle is named."
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block sets out the fourth listed possibility as the one the authors prefer and ties the deep microseismicity beneath this segment to degassing from ascending melt; the preferred disposition, the possibility kind and the segment all come off that one sentence."
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:001",
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block projects continued degassing as the melt rises and places the resulting earthquakes in the mantle between 10 and 20 km, in the conditional the hypothesised modality records."
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:1:block:004",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block's opening states plainly how oceanic crust forms from mantle-derived melt at spreading centres; the subject noun is present."
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007",
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure-caption block reads the deep events under the axis of the ridge as a consequence of degassing-driven volume change, an interpretation rather than a measurement; the ridge appears there under its abbreviation, not its full name."
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports the deep events aligned along a N150E trend parallel to the axial normal faults, and names the segment."
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block concludes from the resolution tests that the deep events are real and not artifacts, and names the segment in parentheses."
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:001",
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block states the chain from degassing through volume change and extensional stress to deep mantle earthquakes in the indicative, which is what the stated modality records; the hypothesis framing for this mechanism sits in the block before it, not in this one."
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block denies that the maximum earthquake depth here follows the usual boundary-depth against spreading-rate relation; the sentence runs on into the next block but the denial is complete in this one."
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:006",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports the off-axis shallow cluster and concludes that the unexpected depths are not a location artifact; the located fragment stops at a line break that the same block completes, and the ridge appears abbreviated."
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block infers from absent deep microseismicity that this fault is inactive, a suggestion rather than a measurement, and names the fault."
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block places most of the deep events in the mantle below 10 km with scattered crustal events, hedged as a suggestion."
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:2:block:006",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block's opening fragment reads the seafloor peridotites as evidence of exhumed mantle; the sentence begins in the previous block but the assertion and the subject noun are both here."
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007",
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block rules the fastest velocity model out for locating events beneath the ridge axis, which is the negation the row records; the ridge appears abbreviated."
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007",
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure-caption block states that three segments are drawn southward from the transform, and names it."
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:001",
            "page:4:block:002",
            "page:5:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The first cited block sets out the magmatic-tectonic possibility and the second records the authors rejecting it for these events, which is what the not-supported disposition asserts; the mantle is named in the first."
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block concludes that magmatism dominates crustal accretion at this segment and that the events sit in mantle above 1100 C; both parts are stated outright and the segment is named."
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block derives the 1100 to 1200 C range at 10 to 20 km from thermal modelling and concludes the mantle beneath the segment axis is hot, which is the calculated basis the row records."
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The abstract block projects the effect of high primary-melt CO2 on melt beneath the lithosphere-asthenosphere boundary; the boundary appears spelled out there rather than under the abbreviation the row's subject carries."
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010",
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block suggests the melt at the boundary could come from CO2 and water together, leaning on the authors' analysis and earlier work; the abbreviation is used in that block."
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006",
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block offers freezing at the lithosphere base as a possibility producing sub-horizontal reflections, which matches the conditional the modality records."
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:001",
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reads the 10 to 20 km microseismicity as showing ascending melt residing, fractionating and evolving in the mantle, hedged as a suggestion."
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:003",
            "page:2:block:006",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block states the absence of a clear understanding of how the melts migrate in the upper mantle, which is the negation the row carries."
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007",
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block lists the five velocity models by their position relative to the transform, plainly and without hedging."
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:001",
            "page:3:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block raises the mylonite shear-zone hypothesis and, in the same block, records that the observations do not support it, which is what the not-supported disposition asserts."
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block states there are no observed active vents on this segment's axis, the negation the row records, and names the segment."
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:2:block:006",
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block denies evidence of a current eruption in the valley, resting it on low crustal microseismicity and seafloor morphology."
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block attributes the shallow events beneath the dome to ruptures on high-angle normal faults with a likelihood hedge, which the modality records."
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reads the hummocky morphology, the cones and the neo-volcanic ridge as showing this segment is magmatic, stated outright."
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:001",
            "page:3:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block says a strain-localised shear zone in the deep mantle can be expected during detachment development; the retained fragment opens with the previous sentence's reference marker but the assertion is intact."
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block carries the authors' suggestion that a small degassing-driven pressure rise induces the events beneath this ridge axis, and names the segment."
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block records the limitation plainly, that the microseismicity is a brief snapshot and activity may vary over years; the ridge appears abbreviated."
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:7:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports normal velocity ratios from tomography in this segment, stated without hedge."
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block attributes to earlier work the idea that volatiles flush melt away from the axis toward the boundary, which matches the hypothesised modality and names the boundary."
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The abstract block reports the deep events at 10 to 20 km in the mantle along the ridge axis; the bounds, the unit and the measured basis all come off that sentence and the ridge is named in full."
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block places the 20 km boundary depth inside an explanation the authors then set aside, so the approximate qualifier and the hypothesised modality both match; the boundary is named by abbreviation."
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the boundary as about 10 km beneath the southern discontinuity on the strength of the microseismicity, which matches the approximate bound and the measured basis."
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block bounds the boundary above at 10 km off-axis west of the segment, which is the open upper bound the row carries."
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block gives the barium-based pre-eruptive estimate for this segment as 0.7 to 4.6 wt% and says in the same block that the estimate is for pre-eruptive melts, so the quantity kind and the estimated status both hold."
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same block gives the barium-based pre-eruptive estimate for the southern segment as 0.06 to 0.8 wt%, with that segment named."
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the primary-melt barium estimate for this segment as 0.4 to 3.0 wt%, calculated from the equilibrium concentrations; bounds, unit, subject and estimated status all come off it."
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same sentence gives the southern segment's primary-melt barium estimate as 0.04 to 0.5 wt%; the row's short label is a fragment of the block's own symbol, which leaves value, unit and subject exact."
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The results block gives the calculated volatile content of melts generated along this segment as 0.4 to 3.0 wt%; the label the row carries is the sentence's opening noun rather than the symbol, which changes nothing that is claimed."
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same sentence gives 0.04 to 0.7 wt% for the southern segment, named there for contrast."
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block puts the primary-melt concentration no lower than 0.4 wt% for this segment, which is the open lower bound the row carries."
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block gives the rubidium-based pre-eruptive estimate for this segment as 0.9 to 4.3 wt%."
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same block gives 0.07 to 1.0 wt% for the southern segment."
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the primary-melt rubidium estimate for this segment as 0.5 to 2.8 wt%."
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same sentence gives 0.05 to 0.7 wt% for the southern segment."
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block dates the western-flank crust at 8 Ma; the retained fragment is short but value, unit and subject are all in that block."
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006",
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block gives the western-flank crust as 5.4 km thick with a 0.3 km uncertainty from refraction work, and the caption block repeats it for the segment."
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The results block lists the deep microseismicity beneath this segment's axis at about 10 to 20 km, which is the approximate bounded quantity the row carries, with the segment named."
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports an average near 2800 ppm for segments in this ocean region from earlier ratio-based estimates; the row carries the average and not the maximum the same sentence also gives."
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block gives the half-spreading rate as 16 mm/yr and names the ridge in the same block."
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007",
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure-caption block gives those events as 10 to 19 km below the sea floor under the axis of the ridge; the ridge appears there under its abbreviation."
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The caption block ties the boundary to the 750 C isotherm; the located fragment stops just before the number, which sits in the same block."
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block gives the cold lithosphere as 45 Ma inside the cold-edge argument."
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:003",
            "page:6:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports 514 located events around the intersection region and the methods block repeats the count; the intersection is named in the first."
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:001",
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block puts these earthquakes in mantle hotter than 1100 C, which is the open lower bound the row carries."
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:002",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives 120 km of ridge axis as covered by the network; the ridge appears abbreviated there."
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007",
            "page:3:block:004",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block gives 317 events located along the ridge and the figure-caption block carries the same total."
        },
        {
          "row_index": 124,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:001",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_NOT_IN_BLOCK The block gives a 10 km width for the segment's median valley, so value, unit and segment hold, but it calls the structure the median valley and never the axial valley the row's subject is named for; the identification is made nowhere in this block."
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010",
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports about 1.1 per cent melt required at the boundary base as a modelled proposal from earlier work, which matches the hypothesised modality and the modelled determination."
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block denies any events below 20 km beneath this segment's axis, which is the negated open bound the row carries."
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same key-observations sentence gives 4 to 10 km for the events beneath the southern discontinuity, which is named there."
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the northern discontinuity as about 35 km long and names it."
        },
        {
          "row_index": 129,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block bounds the events beneath the southern discontinuity above at 10 km."
        },
        {
          "row_index": 130,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the maximum depth there as about 10 km, which it treats as expected for a slow-slipping discontinuity."
        },
        {
          "row_index": 131,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the southern discontinuity a ridge offset of about 33 km."
        },
        {
          "row_index": 132,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same sentence bounds the events beneath the core complex above at 6 km."
        },
        {
          "row_index": 133,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block gives the off-axis cluster focal depths as about 2 to 6 km on the western side of the valley, which is named."
        },
        {
          "row_index": 134,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives pre-eruptive concentrations of 0.7 to 4.6 wt% for this segment after fractional crystallisation, an estimate rather than a measurement."
        },
        {
          "row_index": 135,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives barium above 89 ppm for this segment's samples, an open lower bound taken from measurement."
        },
        {
          "row_index": 136,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the deep events beneath this segment's axis as 16 to 19 km, observed."
        },
        {
          "row_index": 137,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives this segment as about 22 km long."
        },
        {
          "row_index": 138,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same sentence gives rubidium above 8 ppm for this segment's samples."
        },
        {
          "row_index": 139,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the southern segment as 50 km long."
        },
        {
          "row_index": 140,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:002",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives 140 km of the transform's eastern part as covered by the network and names it."
        },
        {
          "row_index": 141,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007",
            "page:3:block:003",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block gives 197 events along the transform and the figure-caption block carries the same total."
        },
        {
          "row_index": 142,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same key-observations sentence gives 0 to 6 km for the shallow events at the intersection, which is named there."
        },
        {
          "row_index": 143,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010",
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives about 1250 C as the sub-solidus temperature at which melt is present at the boundary; the row's label is a hyphen-broken fragment of the block's own noun and does not change the quantity."
        },
        {
          "row_index": 144,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports the highest previously published melt CO2 at that ridge; the located fragment stops before the 1.9 wt% figure, which sits in the same block."
        }
      ]
    },
    {
      "question_id": "CQ-04",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The preferred mechanism is in the rows and so is its epistemic marking: a claim row states the fourth listed possibility as the authors' preferred one, ties the deep microseismicity to CO2 degassing from ascending melt, and carries both a hypothesised modality and a preferred disposition, while the rival mechanisms it displaces carry an explicit not-supported disposition. The ambiguity is in the rest of the chain. Volume change, extensional stress and the triggering of the earthquakes are carried by a claim row whose modality is stated rather than hypothesised, because the sentence it was drawn from is written in the indicative and the hypothesis framing sits in the neighbouring block. Nothing in the row set links that row to the preferred-hypothesis row, so a consumer meets the requirement that the mechanism be represented explicitly as a hypothesis only by reading several rows together and joining them on their shared subjects. Ascending melt, degassing, pressure change and triggering are each present on at least one hypothesised row, so the shortfall is in how the parts are bound, not in coverage.",
      "source_locators": [
        "page:1:block:001",
        "page:3:block:003",
        "page:5:block:001",
        "page:5:block:002",
        "page:5:block:003",
        "page:7:block:012"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:2:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block that supplies the name uses it for the structure west of which the off-axis cluster sits; the projection carries nothing else to check."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The introduction block defines the brittle-ductile boundary and abbreviates it, which gives both the name and the boundary kind the row projects."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names this transform alongside the Romanche as the bound of the ridge segment studied."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Both cited blocks use the noun, one contrasting it with the lithosphere above and one dating and measuring the western flank."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the westward-dipping detachment bounding the intersection segment, which is the feature kind the row projects."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block places the study in this ocean region by name."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names this ridge alongside the Southwest Indian Ridge as an ultraslow case with deep mantle events."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The figure-caption block describes the inactive mound and the dive observations behind it, which is what the row's description asserts."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports the extinct vent field on the eastern flank of the northern discontinuity, giving both the name and the kind."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block describes the high-angle inward-dipping faults and their orientation, which is what the row's description asserts."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block spells out the lithosphere-asthenosphere boundary and abbreviates it, giving the name and the boundary kind."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Both cited blocks use the noun, one for the brittle lithosphere above the melt and one for the cold 45 Ma lithosphere."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Both cited blocks use the noun for the layer the deep events are placed in."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the ridge in full and gives its abbreviation; the caption block repeats the expansion."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The caption block names the expected Moho interface, which is the kind the row projects."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the neo-volcanic ridge in the segment's median valley and gives its orientation."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block describes the normal faults cutting the core complex surface with the strikes the row's description carries."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block introduces the first non-transform discontinuity and names it, giving the name and the kind."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The same block introduces the second non-transform discontinuity and names it."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the oceanic core complex and abbreviates it, giving the name and the kind."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The methods block names this massif and places it at a non-transform discontinuity."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the intersection segment, which is the segment kind the row projects."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the short ridge segment between the two discontinuities, which is the kind the row projects."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The same block names the ridge segment south of the second discontinuity."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the transform; the caption block that supplies the row's feature kind calls the major structures of the region transform faults."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the eastern ridge-transform intersection and abbreviates it."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block uses the phrase for the region it then locates and measures."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:5:block:009"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW One cited block spells out the Southwest Indian Ridge with its abbreviation, the other uses the abbreviation."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block names the solubility model used to place the saturation pressure and depth."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:7:block:006",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW All three cited blocks name the double-difference relocation, in the results, in the methods and in the code list."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The methods block names the first-motion polarity approach used for the focal mechanisms."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The methods block names the local magnitude scale used for the magnitudes."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:7:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Both cited blocks name the non-linear location algorithm used for the initial hypocentres."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Both cited blocks name the short-term over long-term average trigger used for detection."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ],
          "rationale": "DERIVATION_LOCAL The block separates the cooled brittle layer from the partly molten material beneath it, which is the overlying relation and the qualifier the row carries; that same block formalises both endpoints."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The block says the core complex surface is cut by those normal faults; the relation's block is where the fault endpoint is formalised."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL The caption block places the core complex on the outside corner of the ridge, giving the relation and the qualifier; that block also formalises the ridge endpoint."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The block bounds the intersection segment to the east by the detachment; the relation and both endpoints are formalised in that one block."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL The block places the segment south of the northern discontinuity, so the pairing holds on the reading; the relation's block is not among the blocks that formalise either endpoint, both of which are introduced a block earlier."
        },
        {
          "row_index": 39,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:4:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The block says the inward-dipping faults bound the segment's axial valley rather than the segment itself, and the graph carries that valley as a feature of its own, so the endpoint the row names is a step removed from what the prose bounds; the relation's block does formalise the fault endpoint."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The block names the ridge segment lying south of the second discontinuity; the relation and both endpoints are formalised there."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL The block places the study area in the northern part of the ridge segment; the relation and both endpoints are formalised there."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:002"
          ],
          "rationale": "DERIVATION_LOCAL The block puts the extinct vent field on the eastern flank of the northern discontinuity; that block also formalises the vent-field endpoint."
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports the authors analysing samples from this segment and its southern neighbour, in the plain indicative the row's stated modality records, and names the segment."
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:2:block:006",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block describes the valley floor's bathymetric highs, faulting and basaltic constructions as observed fact, which matches the stated modality, and names the valley."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block draws a suggestion that the ridge axis is shifting east beneath the core complex dome, which is the hedge the hypothesised modality and the suggestion kind record; the complex is named there."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block frames the southward shallowing of the boundary as an expectation rather than a finding, which is what the hypothesised modality carries; the boundary is named by abbreviation."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:2:block:006",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The abstract block carries the authors' own suggestion that deep mantle earthquakes follow from CO2 degassing; the hedge is explicit and the mantle is named."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block sets out the fourth listed possibility as the one the authors prefer and ties the deep microseismicity beneath this segment to degassing from ascending melt; the preferred disposition, the possibility kind and the segment all come off that one sentence."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:001",
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block projects continued degassing as the melt rises and places the resulting earthquakes in the mantle between 10 and 20 km, in the conditional the hypothesised modality records."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:1:block:004",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block's opening states plainly how oceanic crust forms from mantle-derived melt at spreading centres; the subject noun is present."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007",
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure-caption block reads the deep events under the axis of the ridge as a consequence of degassing-driven volume change, an interpretation rather than a measurement; the ridge appears there under its abbreviation, not its full name."
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports the deep events aligned along a N150E trend parallel to the axial normal faults, and names the segment."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block concludes from the resolution tests that the deep events are real and not artifacts, and names the segment in parentheses."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:001",
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block states the chain from degassing through volume change and extensional stress to deep mantle earthquakes in the indicative, which is what the stated modality records; the hypothesis framing for this mechanism sits in the block before it, not in this one."
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block denies that the maximum earthquake depth here follows the usual boundary-depth against spreading-rate relation; the sentence runs on into the next block but the denial is complete in this one."
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:006",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports the off-axis shallow cluster and concludes that the unexpected depths are not a location artifact; the located fragment stops at a line break that the same block completes, and the ridge appears abbreviated."
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block infers from absent deep microseismicity that this fault is inactive, a suggestion rather than a measurement, and names the fault."
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block places most of the deep events in the mantle below 10 km with scattered crustal events, hedged as a suggestion."
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:2:block:006",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block's opening fragment reads the seafloor peridotites as evidence of exhumed mantle; the sentence begins in the previous block but the assertion and the subject noun are both here."
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007",
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block rules the fastest velocity model out for locating events beneath the ridge axis, which is the negation the row records; the ridge appears abbreviated."
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007",
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure-caption block states that three segments are drawn southward from the transform, and names it."
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:001",
            "page:4:block:002",
            "page:5:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The first cited block sets out the magmatic-tectonic possibility and the second records the authors rejecting it for these events, which is what the not-supported disposition asserts; the mantle is named in the first."
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block concludes that magmatism dominates crustal accretion at this segment and that the events sit in mantle above 1100 C; both parts are stated outright and the segment is named."
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block derives the 1100 to 1200 C range at 10 to 20 km from thermal modelling and concludes the mantle beneath the segment axis is hot, which is the calculated basis the row records."
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The abstract block projects the effect of high primary-melt CO2 on melt beneath the lithosphere-asthenosphere boundary; the boundary appears spelled out there rather than under the abbreviation the row's subject carries."
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010",
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block suggests the melt at the boundary could come from CO2 and water together, leaning on the authors' analysis and earlier work; the abbreviation is used in that block."
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006",
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block offers freezing at the lithosphere base as a possibility producing sub-horizontal reflections, which matches the conditional the modality records."
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:001",
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reads the 10 to 20 km microseismicity as showing ascending melt residing, fractionating and evolving in the mantle, hedged as a suggestion."
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:003",
            "page:2:block:006",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block states the absence of a clear understanding of how the melts migrate in the upper mantle, which is the negation the row carries."
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007",
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block lists the five velocity models by their position relative to the transform, plainly and without hedging."
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:001",
            "page:3:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block raises the mylonite shear-zone hypothesis and, in the same block, records that the observations do not support it, which is what the not-supported disposition asserts."
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block states there are no observed active vents on this segment's axis, the negation the row records, and names the segment."
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:2:block:006",
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block denies evidence of a current eruption in the valley, resting it on low crustal microseismicity and seafloor morphology."
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block attributes the shallow events beneath the dome to ruptures on high-angle normal faults with a likelihood hedge, which the modality records."
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reads the hummocky morphology, the cones and the neo-volcanic ridge as showing this segment is magmatic, stated outright."
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:001",
            "page:3:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block says a strain-localised shear zone in the deep mantle can be expected during detachment development; the retained fragment opens with the previous sentence's reference marker but the assertion is intact."
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block carries the authors' suggestion that a small degassing-driven pressure rise induces the events beneath this ridge axis, and names the segment."
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block records the limitation plainly, that the microseismicity is a brief snapshot and activity may vary over years; the ridge appears abbreviated."
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:7:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports normal velocity ratios from tomography in this segment, stated without hedge."
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block attributes to earlier work the idea that volatiles flush melt away from the axis toward the boundary, which matches the hypothesised modality and names the boundary."
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The abstract block reports the deep events at 10 to 20 km in the mantle along the ridge axis; the bounds, the unit and the measured basis all come off that sentence and the ridge is named in full."
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block places the 20 km boundary depth inside an explanation the authors then set aside, so the approximate qualifier and the hypothesised modality both match; the boundary is named by abbreviation."
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the boundary as about 10 km beneath the southern discontinuity on the strength of the microseismicity, which matches the approximate bound and the measured basis."
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block bounds the boundary above at 10 km off-axis west of the segment, which is the open upper bound the row carries."
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block gives the barium-based pre-eruptive estimate for this segment as 0.7 to 4.6 wt% and says in the same block that the estimate is for pre-eruptive melts, so the quantity kind and the estimated status both hold."
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same block gives the barium-based pre-eruptive estimate for the southern segment as 0.06 to 0.8 wt%, with that segment named."
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the primary-melt barium estimate for this segment as 0.4 to 3.0 wt%, calculated from the equilibrium concentrations; bounds, unit, subject and estimated status all come off it."
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same sentence gives the southern segment's primary-melt barium estimate as 0.04 to 0.5 wt%; the row's short label is a fragment of the block's own symbol, which leaves value, unit and subject exact."
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The results block gives the calculated volatile content of melts generated along this segment as 0.4 to 3.0 wt%; the label the row carries is the sentence's opening noun rather than the symbol, which changes nothing that is claimed."
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same sentence gives 0.04 to 0.7 wt% for the southern segment, named there for contrast."
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block puts the primary-melt concentration no lower than 0.4 wt% for this segment, which is the open lower bound the row carries."
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block gives the rubidium-based pre-eruptive estimate for this segment as 0.9 to 4.3 wt%."
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same block gives 0.07 to 1.0 wt% for the southern segment."
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the primary-melt rubidium estimate for this segment as 0.5 to 2.8 wt%."
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same sentence gives 0.05 to 0.7 wt% for the southern segment."
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block dates the western-flank crust at 8 Ma; the retained fragment is short but value, unit and subject are all in that block."
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006",
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block gives the western-flank crust as 5.4 km thick with a 0.3 km uncertainty from refraction work, and the caption block repeats it for the segment."
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The results block lists the deep microseismicity beneath this segment's axis at about 10 to 20 km, which is the approximate bounded quantity the row carries, with the segment named."
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports an average near 2800 ppm for segments in this ocean region from earlier ratio-based estimates; the row carries the average and not the maximum the same sentence also gives."
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block gives the half-spreading rate as 16 mm/yr and names the ridge in the same block."
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007",
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The figure-caption block gives those events as 10 to 19 km below the sea floor under the axis of the ridge; the ridge appears there under its abbreviation."
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The caption block ties the boundary to the 750 C isotherm; the located fragment stops just before the number, which sits in the same block."
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block gives the cold lithosphere as 45 Ma inside the cold-edge argument."
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:003",
            "page:6:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports 514 located events around the intersection region and the methods block repeats the count; the intersection is named in the first."
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:001",
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block puts these earthquakes in mantle hotter than 1100 C, which is the open lower bound the row carries."
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:002",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives 120 km of ridge axis as covered by the network; the ridge appears abbreviated there."
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007",
            "page:3:block:004",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block gives 317 events located along the ridge and the figure-caption block carries the same total."
        },
        {
          "row_index": 108,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:001",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_NOT_IN_BLOCK The block gives a 10 km width for the segment's median valley, so value, unit and segment hold, but it calls the structure the median valley and never the axial valley the row's subject is named for; the identification is made nowhere in this block."
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010",
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block reports about 1.1 per cent melt required at the boundary base as a modelled proposal from earlier work, which matches the hypothesised modality and the modelled determination."
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block denies any events below 20 km beneath this segment's axis, which is the negated open bound the row carries."
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same key-observations sentence gives 4 to 10 km for the events beneath the southern discontinuity, which is named there."
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the northern discontinuity as about 35 km long and names it."
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block bounds the events beneath the southern discontinuity above at 10 km."
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the maximum depth there as about 10 km, which it treats as expected for a slow-slipping discontinuity."
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the southern discontinuity a ridge offset of about 33 km."
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same sentence bounds the events beneath the core complex above at 6 km."
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block gives the off-axis cluster focal depths as about 2 to 6 km on the western side of the valley, which is named."
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives pre-eruptive concentrations of 0.7 to 4.6 wt% for this segment after fractional crystallisation, an estimate rather than a measurement."
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives barium above 89 ppm for this segment's samples, an open lower bound taken from measurement."
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the deep events beneath this segment's axis as 16 to 19 km, observed."
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives this segment as about 22 km long."
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same sentence gives rubidium above 8 ppm for this segment's samples."
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives the southern segment as 50 km long."
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:002",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives 140 km of the transform's eastern part as covered by the network and names it."
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007",
            "page:3:block:003",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The methods block gives 197 events along the transform and the figure-caption block carries the same total."
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The same key-observations sentence gives 0 to 6 km for the shallow events at the intersection, which is named there."
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010",
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_NON_LOCAL SUBJECT_IN_BLOCK The block gives about 1250 C as the sub-solidus temperature at which melt is present at the boundary; the row's label is a hyphen-broken fragment of the block's own noun and does not change the quantity."
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports the highest previously published melt CO2 at that ridge; the located fragment stops before the 1.9 wt% figure, which sits in the same block."
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
