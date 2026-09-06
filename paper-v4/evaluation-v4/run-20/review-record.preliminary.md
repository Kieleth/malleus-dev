# Malleus paper v4 run-20 source-grounded review record

Template. The row counts are substituted at freeze, from the frozen cell's own
query result, at the same time as `paper-v4/evaluation-v4/review-task-v4.template.md`.
No placeholder may survive instantiation.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

Fill one `rows` entry per returned row, in order, zero-based: 34 for
CQ-01, 105 for CQ-02, 158 for CQ-03, 137 for
CQ-04, 434 in all. Cite reading block ids only. Write the reasons in
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
    "review_input_manifest_sha256": "sha256:fcb666332ebc5878643adb0f1b7cb3d61ce3443ec95bef74b9126da8cb3cd8b1"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-preliminary-run-20",
    "completed_at": "2026-09-06T07:17:08Z"
  },
  "questions": [
    {
      "question_id": "CQ-01",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "Every requested part is directly present in the rows: the instrument network that acquired the microseismicity data, the named cruise it was deployed during, a membership relation binding the two, and a count row giving the number of instruments in that network. A second pair of count rows gives the smaller number of instruments actually used for detection, but each carries its own scope, so the two figures do not compete. Most of the remaining rows are location methods, velocity and solubility models and processing software, which the type-only binding admits and which say nothing about the network or the campaign; that is noise around the answer rather than a gap in it.",
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
          "rationale": "NO_SUBJECT_IN_ROW The projection is a bare campaign name and both cited blocks name that cruise, one as the campaign during which the microseismicity data were acquired and the other as the campaign during which the passive experiment was conducted."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:008"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The data-availability block names the raw seismic data and cruise reports and gives the cruise-archive address the projection carries, so both projected fields rest on that block."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:005",
            "page:8:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One cited block names the geochemical database and the other names it again with the web address the projection carries, so name and locator both rest on cited prose."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:008"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the earthquake catalogue and the picked P- and S-arrivals as the deposited product, which is the whole of the projection; no locator is projected, and the capture records that the repository identifier is split across the block boundary."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the ocean-bottom seismometers as the network that acquired the microseismicity data, which is the whole of this projection."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the double-difference relocation method used after the initial hypocentre locations, matching the projected name."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The magnitude-estimation block names the local magnitude scale used to determine earthquake magnitudes, matching the projected name."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the non-linear earthquake location algorithm used to obtain hypocentres, matching the projected name."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The earthquake-location block names the non-linear oct-tree search algorithm used for the initial hypocentres, matching the projected name."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the active-source wide-angle seismic refraction profile used to find the one-dimensional velocity model, matching the projected name."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the short-term-average over long-term-average trigger algorithm used for automatic arrival detection, matching the projected name."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the Wadati diagrams used to obtain the velocity ratio, matching the projected name."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the average velocity model as the best-fitting model selected for subsequent location work, matching the projected name."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the carbon-dioxide solubility model used to derive the saturation pressure and depth, matching the projected name."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The depth-resolution block names the fastest of the five velocity models, by that description and by its model number, matching the projected name."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the published solubility model, by its first author, used to compute the theoretical solubility, matching the projected name."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names thermal modelling as the source of the temperature expectation at the deep-earthquake depths, matching the projected name."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the one-dimensional velocity model sought from the refraction profile, which carries the projected generic name."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block names the mapping tool used for structural analysis and gives the address the projection carries, so both projected fields rest on that block."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the graphing toolbox used, which is the whole of the projection; no locator is projected, and the capture records that this tool's address is split across the block boundary."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One cited block names the focal-mechanism package and the other gives its version and address, so name, version and locator all rest on cited prose."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One cited block names the relocation program and the other gives its version and address, so all three projected fields rest on cited prose."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One cited block names the location program and the other gives its address, so name and locator both rest on cited prose."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One cited block names the phase-picking package and the other gives its address, so name and locator both rest on cited prose."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One cited block names the program used to search for the minimum velocity model and the other gives its address, so name and locator both rest on cited prose."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One cited block names the catalogue-analysis software used for the b value and completeness and the other gives its address, so name and locator both rest on cited prose."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DERIVATION_LOCAL The assertion that formalizes this relation sits in the same block that formalizes both endpoints, and that sentence states that the instrument network acquired the data during the named cruise, which is exactly the campaign membership asserted here."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence carries the cruise name and states the instrument total for the network that acquired the data, so the count of nineteen and its scope both rest on that sentence and the record is genuinely a property of that campaign's deployment."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence sets the minimum number of instruments on which an event had to be detected and names the instrument type, which is the counted thing here, so the count of five and its scope both rest on it."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence gives the number of useful instruments from which initial arrivals were detected and names the instrument type, which is the counted thing, so the count of seventeen and its scope both rest on it."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence in the Methods gives the same number of useful instruments and states that their vertical components were analysed, which is exactly the projected scope, and it names the instrument type."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence attributes the weakness of the focal-mechanism solutions to the instrument spacing and gives that spacing, approximately, with the projected unit, so value, qualification and subject all rest on it."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the location program and states the confidence level of the three-dimensional error ellipsoid it estimates, so the value, the unit and the attribution to that program all rest on it."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the refraction profile, hyphen-broken across a line but plainly the same phrase, and gives the approximate depth below sea level down to which it constrains velocity, which is exactly the projected quantity."
        }
      ]
    },
    {
      "question_id": "CQ-02",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "Both requested parts are directly present. One row names the short ridge segment as a subsection of the studied ridge portion, and a group of rows attaches the deep microseismicity to it and places the events: beneath its ridge axis at roughly ten to twenty kilometres, more narrowly sixteen to nineteen kilometres in the results text, aligned along a direction parallel to the main axial faults, absent below twenty kilometres, and with the shallow off-axis activity kept separate to the west of the axis. The depth endpoints differ between the abstract, the results text and the figure caption, but each row carries its own scope and provenance and they do not conflict about where the events lie. Most of the remaining rows are other named features, other subsections and the melt geochemistry, which the type-only binding admits and which do not bear on this question.",
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
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names deep-rooted detachment faults as one of the structures deeper earthquakes have been associated with, which carries the projected name."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the normal faults that heavily cut the core complex surface, which carries the projected name."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the equatorial ocean basin in which the studied ridge lies, which is the whole of this projection."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002",
            "page:4:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One cited block names the island, hyphen-broken across a line but plainly the same word, as the setting of two volcanic systems, and the other names it again unbroken."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the offshore island in the western Indian Ocean whose deep seismicity is offered as a comparison, which carries the projected name."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block locates the study area within the ridge segment between the two transforms, so the projected generic name rests on that sentence."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block introduces the brittle-ductile boundary and gives the abbreviation the projection carries."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block introduces the lithosphere-asthenosphere boundary and gives the abbreviation the projection carries."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited figure-caption block names the expected crust-mantle interface drawn on the schematic, which carries the projected name."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the sea floor as the datum for the expected earthquake depths, which carries the projected name."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block introduces the oceanic core complex on the eastern side of the ridge axis and gives the abbreviation the projection carries."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block enumerates the four subsections and names the first non-transform discontinuity, which carries the projected name."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The same enumeration names the second non-transform discontinuity, which carries the projected name."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the eastern ridge-transform intersection and gives the abbreviation the projection carries."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The enumeration of subsections names the intersection segment by the label the projection carries."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The enumeration of subsections names the short ridge segment by the label the projection carries."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the ridge segment south of the second discontinuity by the label the projection carries."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the axial valley floor beneath which deep microseismicity is absent, which carries the projected name."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the bathymetric highs that characterise the axial valley floor, which carries the projected name."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:006",
            "page:4:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both cited figure-caption blocks name the corrugated surface as marked tectonic information, which carries the projected name."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the hummocky volcanic axial morphology, hyphen-broken across a line as the projection preserves it, as evidence of magmatic origin."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited figure-caption block names the hummocky seafloor shaded on the map, which carries the projected name."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the median valley of the short ridge segment, which carries the projected name."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the transform valley beneath which one of the velocity models was built, which carries the projected name."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names this ultraslow-spreading ridge as one of the places where deep mantle earthquakes have been observed, which carries the projected name."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names this ridge among the compiled maximum-depth sites whose data were updated, which carries the projected name."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the Mid-Atlantic Ridge and gives the abbreviation the projection carries."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the Southwest Indian Ridge and gives the abbreviation the projection carries."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names this transform as one of the two bounding the ridge segment; the projection carries only the bare name, which the block supplies, though it supplies it inside a joint reference to both transforms."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:002",
            "page:2:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW All three cited blocks name this transform, one of them with exactly the abbreviated form the projection carries."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The formalizing assertion sits in the block that also formalizes the target endpoint, and its sentence states that the core complex surface is heavily cut by those normal faults, which is exactly the cutting relation asserted here."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_NON_LOCAL The relation is formalized from a figure caption, while both endpoints are formalized in a body block on the previous page, so the relation's block is not one of theirs; the caption nonetheless states plainly that the core complex lies on the outside corner of the ridge, which supports the containment asserted."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The formalizing assertion sits in the block that also formalizes the source endpoint, and it states that the intersection segment is bounded to the east by a westward dipping detachment fault, which is the bounding relation asserted."
        },
        {
          "row_index": 33,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:4:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL The relation's block is neither endpoint's. Its sentence does support that this segment is bounded by faults, but it describes them only as high-angle inward-dipping faults with a given strike and never calls them normal faults, so the identity of the bounding structures with the normal-fault record the row points at is not carried by the cited prose."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL The relation is formalized in a discussion block while its endpoints are formalized in two earlier blocks, so the relation's block is neither of theirs; that block does state that the axial valley floor is cut by ridge-parallel normal faults, which is the cutting relation asserted."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:006"
          ],
          "rationale": "DERIVATION_LOCAL The formalizing assertion sits in a block that also formalizes the source endpoint, and it refers to the corrugated surface as belonging to the core complex, which supports the part-whole relation asserted."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The formalizing assertion sits in the block that formalizes both endpoints, and it places the named ridge in the named ocean basin, which is the containment asserted."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the detachment fault and states that it is inactive, inferred from the absence of deep microseismicity beneath the valley floor near the core complex termination, so the claim is a predication about the subject itself."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the boundary and states the expectation that it shallows southward with distance from the intersection, which is exactly what the claim records about that subject."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the boundary and proposes that melt present there could come from a combination of the two volatiles; the hypothesised modality matches the suggesting verb in the prose."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the core complex twice, as the origin and as the destination of the axis relocation, so the subject is an essential term of the claim and not a passing mention."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence attributes the shallow earthquakes beneath the core complex dome to ruptures on faults cutting its surface, so both the location and the cut surface belong to the subject."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the segment and gives the direction along which the deep earthquakes beneath its axis are aligned; the sentence runs past the end of the block, but the alignment claim is complete within it."
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the segment and states that the deep events beneath its ridge axis are well constrained and not artifacts, which is what the claim records."
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the segment, offers degassing from the ascending melt as an explanation of the deep microseismicity beneath it, and marks it as the authors' preferred possibility, which supports both the hypothesised modality and the preferred disposition."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the segment and states that magmatism dominates its crustal accretion, which is exactly the claim."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the segment axis and denies any observation of active hydrothermal vents on it, which supports both the claim and its negated modality."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the segment and denies evidence for detachment faults there, which supports both the claim and its negated modality."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the segment ridge axis and proposes the small degassing-driven pressure increase as the trigger of the earthquakes observed beneath it, matching the claim and its hypothesised modality."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the segment and reports normal velocity ratios there from tomography, which is what the claim records about that subject."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the axial valley and denies evidence of a current eruption in it, which supports the claim and its negated modality."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the ridge and denies that the maximum earthquake depth beneath this portion of it follows the depth-versus-spreading relationship; the sentence is cut by the page break in the text layer, but the negation and its subject are complete within the cited block."
        },
        {
          "row_index": 52,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence does support the interpretation the claim records, that the enriched basalts and high volatile contents come from low-degree melting of an enriched source. The transform fault the row makes the subject enters that sentence only as a proximity qualifier on the mantle source; the claim is about the basalts, and the cited prose does not make it a claim about the fault."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence gives the number of earthquakes located in the vicinity of the named intersection region, so the region scopes the count and the count is genuinely about it."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence gives the number of events located along the named ridge, which is exactly the projected count and scope."
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same located sentence gives the number of events located along the named transform, which is exactly the projected count and scope."
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the ocean basin and gives the average concentration reported across several of its segments, with the projected unit and approximation, and attributes it to ratio-based estimation, which matches the estimated determination."
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same located sentence gives the highest concentration reached at those segments, which the row records as an upper bound with no lower bound, and that is how the prose expresses it."
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the island and gives the depth floor for the magmatic-tectonic activity observed there. The sentence as a whole frames a hypothesis about the ridge earthquakes, but the depth is reported as observed fact, and the capture carries a stated sub-span over exactly that clause."
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same located sentence names the offshore island and gives the depth floor for the activity observed there, again as reported fact inside a comparative clause covered by a stated sub-span."
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the boundary and puts it at the projected depth beneath the southern discontinuity, with the projected unit and approximation."
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the boundary and gives the depth it would have under the cold and thick lithosphere explanation, which is why the row is hypothesised rather than measured."
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same located sentence gives the isotherm range that boundary depth corresponds to under that explanation, with the projected unit and endpoints."
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the boundary and gives the isotherm, with its stated tolerance, used to define it at slow- and ultraslow-spreading ridges, matching the projected value and uncertainty."
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located figure-caption sentence names the boundary drawn on the schematic and gives the isotherm it corresponds to, matching the projected value and unit."
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the boundary and states that it remains shallow, below the projected depth, off-axis west of the segment, which is exactly the bound the row records."
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the boundary and gives the melt proportion proposed as required at its base to explain the observed reflections, which is the projected value and its hypothesised standing."
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same located sentence gives the water content accompanying that proposal as an upper bound, matching the projected value and qualification."
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the core complex and gives the depth bound of the earthquakes observed beneath it, matching the projected upper bound and unit."
        },
        {
          "row_index": 69,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:4:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located figure caption does give the half-width within which earthquake depths are plotted on the two transects, so the value, unit and scope are carried. The core complex the row makes the subject is only what those transects run along and across; the quantity is a property of how the figure was drawn, and the cited caption does not make it a property of the feature."
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the southern discontinuity and gives the depth range of the normal-depth earthquakes beneath it, matching the projected endpoints and unit."
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the first discontinuity and gives its length, matching the projected value, unit and approximation."
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the second discontinuity and gives the depth down to which earthquakes beneath it extend, matching the projected value and approximation."
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the same discontinuity and gives the depth bound of the earthquakes observed beneath it, matching the projected upper bound and unit."
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the second discontinuity and gives its ridge offset, matching the projected value, unit and approximation."
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the intersection and gives the depth range of the majority of shallow earthquakes on its outside corner, so the region scopes the population and the range matches the projected endpoints."
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the segment and gives the calculated volatile content of the melts generated along it, matching the projected range and unit, and it is written as a calculated figure."
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same located sentence gives the corresponding calculated content for the southern segment, matching the projected range and unit for that subject."
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the studied segment and states that the primary-melt concentration there is at least the projected value, which is exactly the lower bound the row records."
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the segment and gives the barium-based pre-eruptive range, matching the projected endpoints and unit."
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the southern segment and gives its barium-based pre-eruptive range, matching the projected endpoints and unit."
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the segment and gives the barium-derived primary-melt range, matching the projected endpoints and unit."
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same located sentence gives the barium-derived primary-melt range for the southern segment, matching the projected endpoints and unit."
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the segment and gives the rubidium-based pre-eruptive range, matching the projected endpoints and unit."
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the southern segment and gives its rubidium-based pre-eruptive range, matching the projected endpoints and unit."
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the segment and gives the rubidium-derived primary-melt range, matching the projected endpoints and unit."
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same located sentence gives the rubidium-derived primary-melt range for the southern segment, matching the projected endpoints and unit."
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the segment and gives the depth range of the deep earthquakes observed beneath its axis, matching the projected endpoints and unit."
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence is the key observation for this question: it names the segment and places the deep microseismicity, at the projected approximate depth range, beneath its ridge axis."
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the segment ridge axis and denies earthquakes deeper than the projected value beneath it, which supports both the bound and the negated modality."
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the segment axis and gives the depth down to which the off-axis microseismicity west of it extends, matching the projected upper bound; the capture carries a measured sub-span over exactly that observation clause."
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the segment and gives the estimated pre-eruptive concentration range for it, matching the projected endpoints and unit."
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the segment and gives the barium abundance floor for all its samples, matching the projected lower bound and unit."
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the segment and gives its length, matching the projected value, unit and approximation."
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same located sentence gives the rubidium abundance floor for those samples, matching the projected lower bound and unit."
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the southern segment and gives its length without an approximation marker, matching the projected exact value and unit."
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the median valley and gives its width as a compound modifier, matching the projected value and unit, and the valley is the bearer of that width."
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the axial valley and gives the shallow focal depths of the cluster on its western side, so the valley scopes which cluster is meant and the range matches the projected endpoints."
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located abstract sentence names the ridge and reports deep earthquakes at the projected depth range in the mantle along its axis, matching the projected endpoints and unit."
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the ridge axis and gives the length of it covered by the instrument network, matching the projected value and unit."
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located figure-caption sentence names the ridge axis and gives the depth range of the deep earthquakes beneath it, below the sea floor. The sentence goes on to interpret their cause, but the capture carries a measured sub-span over the depth clause alone, which is what this row records."
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the ridge and gives its half-spreading rate here, matching the projected value and unit."
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the ridge segment between the two transforms and gives its approximate length, matching the projected value, unit and approximation."
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the ridge and gives the highest melt concentration previously reported there, matching the projected value and unit."
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence names the transform and gives the length of its eastern part covered by the network, matching the projected value and unit."
        }
      ]
    },
    {
      "question_id": "CQ-03",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "Every part the question asks for is reachable in the returned rows: bounded depth and concentration quantities, their units, the entity each is predicated of, and whether the value was observed or computed, carried on the modality and determination fields. What the rows do not do is single out one pair. Three different depth bands for the deep events are returned, one from the abstract, one from the results and one from a figure caption, and four different concentration ranges are returned, split between pre-eruptive and primary melts and between the two trace-element proxies, all with the same segment as subject and none marked as the answer. The binding is type-only, so the rows are every witness of the case types rather than a selection, and the reader has to choose. That is material ambiguity in the row representation, not a failure to address the question, so the rows fall short of directly answering it.",
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
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block introduces barium as one of the trace elements the authors work from, so the constituent this row names is in the reading."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The abstract block presents carbon dioxide as the volatile the whole study turns on, which is all this row projects."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names water next to carbon dioxide as a control on solubility, and the row projects nothing beyond that name."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Rubidium appears in the cited block as the second trace element used for the ratio work, matching the name shown."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:008"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The data-availability block names the raw seismic material and cruise reports and gives the same web location the row carries."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:005",
            "page:8:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks name the sample database, and the methods one gives the same address the row projects."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:008"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The data-availability block names the earthquake catalogue and the arrival picks; no address is projected, so nothing further is at stake."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The velocity-model block names the averaged model and its model number, which is what the row shows."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the solubility model used to place the saturation depth, matching the row."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The depth-resolution block names the fastest of the trial models and its number."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block attributes the solubility calculation to the named model."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names thermal modelling as the source of the temperature estimate, which is the name projected."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block names the one-dimensional velocity model the row identifies."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The introduction block defines the brittle-ductile boundary and gives the abbreviation the row carries."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block spells out the lithosphere-asthenosphere boundary together with its abbreviation."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The caption block names the expected Moho interface."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block measures depth below the sea floor, naming the surface the row projects."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks speak of the brittle lithosphere, the feature named here."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block opens on oceanic crust, which is the feature the row names."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The discussion block names the Juan de Fuca plate as a comparison setting."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block refers to the cold lithosphere near the intersection, naming the feature."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The abstract block places the reported earthquakes in the mantle, so the feature is named where the row points."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:4:block:002",
            "page:5:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW All three cited blocks speak of melt, the material this row names."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006",
            "page:8:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks name the pre-eruptive melts."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:8:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The abstract and the methods block each name the primary melts."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The abstract block names the primitive melt."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block names the double-difference relocation method."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The magnitude block names the local magnitude scale the row projects."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block names the non-linear location algorithm."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The location block names the oct-tree search algorithm."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block names the active-source wide-angle refraction profile."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block names the trigger algorithm used to detect arrivals."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the Wadati diagrams used to obtain the velocity ratio."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block names the mapping tool and gives the same address the row shows."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block names the plotting toolbox; no address is projected on this record."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One cited block names the focal-mechanism package, the other gives the version and the address the row carries."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One cited block names the relocation program, the other gives its version and address."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One cited block names the location program, the other gives its address."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One cited block names the picking package, the other gives its address."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One cited block names the inversion program, the other gives its address."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One cited block names the catalogue-analysis software, the other gives its address."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block names the forsteritic olivine composition the row identifies."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names olivine melt inclusions, so the material is in the prose."
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the global carbon-to-barium trend with its spread and says it was defined from rare undegassed basalts and olivine inclusions, which covers the numerator, the denominator, the value, the uncertainty and the derived status."
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the same barium ratio and spread as the constant used in the estimation, which matches the value, the uncertainty and the derived status."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the global carbon-to-rubidium trend with its spread and the same derivation from undegassed basalts and inclusions, covering every field the row projects."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the same rubidium ratio and spread as the constant used in the estimation, matching every projected field."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:002"
          ],
          "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block attributes the velocity ratio to the Wadati diagrams and states it as approximate, matching the value, the approximation flag and the calculated status."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The study-area block names this subsection and gives it the identifier the row shows."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The study-area block names the short ridge segment and gives it this identifier."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The study-area block names the segment south of the second discontinuity under this identifier."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks report basalts, the material named."
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names mid-ocean ridge basalts."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports peridotites on the sea floor."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names pillow basalts among the rocks observed."
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure-caption block names popping rocks among the sample types plotted."
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure-caption block names melt inclusions among the sample types plotted."
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the compiled basalt samples the analysis rests on."
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this ridge among the ultraslow settings compared."
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The compilation block names this ridge."
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The study-area block names the Mid-Atlantic Ridge and its abbreviation."
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the Southwest Indian Ridge and its abbreviation."
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:1:block:001",
            "page:4:block:002",
            "page:5:block:006"
          ],
          "rationale": "DERIVATION_LOCAL The block states that the crust is built from melt derived from the mantle at spreading centres, which is this pairing and its direction, and the same block formalizes the melt endpoint."
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:004",
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The block reports basaltic rocks seen on the sea floor, and it is also one of the blocks that formalize the basalt endpoint."
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:1:block:004",
            "page:3:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The block reports the extensive observation of basalts on the sea floor at that segment and formalizes the basalt endpoint as well."
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006",
            "page:1:block:004"
          ],
          "rationale": "DERIVATION_LOCAL The block reports peridotites on the sea floor and is the block that formalizes the peridotite endpoint."
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:1:block:004",
            "page:1:block:006"
          ],
          "rationale": "DERIVATION_NON_LOCAL The block reports both pillow basalts and peridotites on the sea floor at the discontinuity, so the pairing holds on the reading; the pointer, though, lands in a block that formalizes neither endpoint, since both were introduced on the first page."
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:1:block:004"
          ],
          "rationale": "DERIVATION_LOCAL The block reports pillow basalts on the sea floor and formalizes the pillow-basalt endpoint too."
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block sets out how the gas behaves during melting and crystallisation at depth and likens it to the highly incompatible trace elements, which is the claim, and the substance is the subject it is filed under."
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block ties solubility in silicate melts to pressure and to water content, so both the content of the claim and the substance it is about sit in the prose."
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block records that the trends have been used to compute primary-melt content for ridge segments worldwide, which is what the claim asserts about the gas."
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block compares the existing measurements on the two segments against the solubility computed at sample depth, the relation the claim names."
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:008"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block draws the comparison between the nucleation proposed here and the rapid degassing under active volcanoes, and the gas the row files it under is the degassing agent on both sides."
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block calls the two element ratios a good proxy for the concentration, which is the status the claim records."
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block spells out the assumption that the trace elements reflect the source and were not disturbed by later processes."
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports that earlier work reached pre-eruptive concentration through volatile to non-volatile element ratios, which is the approach named."
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block records the choice of the averaged model as best fitting and its use downstream, and that model is the subject."
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block compares the chosen model against the minimum model on residuals and on how many events each locates; both are one-dimensional velocity models, the entity the row files this under."
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the expected southward shallowing of the boundary and the cold-edge reason behind it, with the boundary as subject."
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block attributes the melt present at the boundary to a combination of the two volatiles and hedges it, which matches the hypothesised modality and the boundary as subject."
        },
        {
          "row_index": 80,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The caption block does carry the interpretation of the deep earthquakes as volume change from degassing in the hot ductile mantle, but nothing in the reading marks this block as the sixth figure caption, which the row asserts in its name."
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block runs the chain from degassing through volume change and extensional stress to triggered deep earthquakes and places them in the mantle, the subject."
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block infers the host of the events from the measured crustal thickness and puts them mostly below the crust, which is the claim and its subject."
        },
        {
          "row_index": 83,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block does carry the inference to a tectonic origin from exhumed mantle, but it never names the ridge-transform intersection the row attributes the inference to, and the record is about a subsection origin rather than about the mantle it is filed under."
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block raises freezing of melt at the base of the lithosphere as a possibility tied to observed reflections, matching the hedged modality and the subject."
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reads the depth of the microseismicity as melt residing, fractionating and evolving in the mantle, which is the claim about the subject."
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block proposes off-axis magmatism in the crust as the origin of the shallow swarm-like activity, so both the content and the crustal subject are present."
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block concludes from the modelled temperatures that the mantle beneath that segment axis is hot, which is the claim, with the mantle as subject."
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block sets out the expectation of a deep localized shear zone forming during detachment development and producing deep activity, and places it in the mantle."
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the earlier proposal that volatiles both focus melt beneath the axis and flush it away towards the boundary, so the melt is the subject and the content is there."
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states that melt is focused into a narrow zone beneath the axis as it rises, which is the claim about the material it is filed under."
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the gap in understanding of how these melts reach the surface, which is the claim, and the melt is the subject."
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block ties melt movement at depth to high strain rates and brittle failure lower down, matching the claim."
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block distinguishes primary melts in equilibrium with the source from pre-eruptive melts that have fractionated, which is the claim about the primary melt."
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the alignment of the deep events beneath that segment axis parallel to the axial faults and denies a cluster or swarm pattern; the bearing itself is recorded in the capture as not formalized."
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the tests concluding that the deep events beneath that ridge axis are required by the data and are not artifacts."
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block presents this as the fourth possibility and the one the authors prefer, which matches both the hypothesised modality and the preferred disposition, with the segment as subject."
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block concludes that magmatism dominates crustal accretion at that segment, which is the claim about the segment it is filed under."
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block records that no active vents have been seen on that segment axis, which matches the negated modality and the subject."
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block records that the segment shows no evidence of detachment faulting, matching the negated modality and the subject."
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block proposes the small pressure rise from degassing as the trigger of the events beneath that ridge axis and hedges it, matching the modality and the subject."
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports normal velocity ratios from tomography in that segment, which is the claim and its subject."
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states that sea-floor basalts are mostly degassed, which is the claim about the material it is filed under."
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block denies that the maximum earthquake depth beneath this stretch of the ridge follows the depth-to-spreading-rate relationship; the sentence runs on into the next block but the denial and both of its terms are legible here."
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The relocation block gives the number of events located along the ridge as a result of the procedure, which covers the count, its scope and its subject."
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the fraction lost to a nucleated gas phase by the time the melt reaches the sea floor, with the unit, and the gas is the subject."
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reads the activity beneath the discontinuity as putting the boundary at that approximate depth, which matches the value, the unit and the approximation flag."
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the depth the boundary would have under the cold-and-thick explanation and frames it as one explanation, matching the hypothesised modality."
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block pairs that hypothetical boundary depth with an isotherm band in degrees, under the same hedge."
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The introduction block gives the isotherm and its spread used to define the boundary at slow and ultraslow ridges."
        },
        {
          "row_index": 110,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The caption block does give the isotherm the boundary corresponds to, with its unit, but nothing in the reading marks the block as the sixth figure caption, which the row states in its name."
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reads the off-axis shallow activity as keeping the boundary above that depth, matching the open upper bound and the unit."
        },
        {
          "row_index": 112,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block carries the proposed melt proportion at the base of the boundary with its unit and its hedged status, but it presents the figure as a proposal made to explain observed reflections and never says it came from a model, which is what the row asserts as its determination."
        },
        {
          "row_index": 113,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the water-content ceiling inside the same proposal, with its unit, but as with the melt fraction it does not attribute the number to a model, so the modelled determination is unsupported."
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block concludes a ceiling on brittle thickness at the segment boundaries, which matches the bound, the unit and the subject."
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the age of the cold lithosphere behind the edge effect, with its unit."
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block attributes the thickness and its uncertainty to refraction work, so the value, the spread and the measured determination all hold."
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the depth band in the mantle over which continued degassing would produce earthquakes and hedges it, matching the modality and the subject."
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block ties the expected maximum earthquake depth to a ceiling on brittle thickness, matching the bound and the unit."
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the lower temperature bound for the mantle hosting these events, with the unit."
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block attributes the temperature band over that depth interval to thermal modelling, which covers the values, the unit and the modelled determination."
        },
        {
          "row_index": 121,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The caption block gives the crustal thickness beneath that segment with its uncertainty, but the reading nowhere identifies the block as the sixth figure caption, which the row claims in its name."
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the age of the western flank crust, with its unit."
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the age ceiling for a magmatically accreted young crust in the aside about the fastest velocity model."
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The abstract block gives the approximate range in the primary melts and attributes it to sample syntheses and geochemical analyses, which covers the bounds, the unit and the derived status."
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block makes the program the estimator of the error ellipsoid and gives the confidence level with its unit, so the quantity is predicated of the tool the row files it under."
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block attaches the depth to which velocity is constrained to the refraction profile itself, which is the subject, with the approximation and the unit."
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the calculated content for the melts of that segment, flagged as calculated, with the unit."
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the calculated content for the southern segment as the comparison, with the unit."
        },
        {
          "row_index": 129,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states the floor on primary-melt concentration along that segment, matching the open lower bound and the estimated determination."
        },
        {
          "row_index": 130,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the barium-based pre-eruptive estimate for that segment, with the unit and the estimate framing."
        },
        {
          "row_index": 131,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the barium-based pre-eruptive estimate for the southern segment, with the unit."
        },
        {
          "row_index": 132,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the barium-based primary-melt estimate for that segment, with the unit and the estimate framing."
        },
        {
          "row_index": 133,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the barium-based primary-melt estimate for the southern segment."
        },
        {
          "row_index": 134,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the rubidium-based pre-eruptive estimate for that segment, with the unit."
        },
        {
          "row_index": 135,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the rubidium-based pre-eruptive estimate for the southern segment, with the unit."
        },
        {
          "row_index": 136,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the rubidium-based primary-melt estimate for that segment, with the unit."
        },
        {
          "row_index": 137,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium-based primary-melt estimate for the southern segment."
        },
        {
          "row_index": 138,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the observed depth band of the deep events beneath that segment axis as a measurement, with the unit."
        },
        {
          "row_index": 139,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The results block lists the approximate depth band of the deep activity beneath that segment axis among the three key observations."
        },
        {
          "row_index": 140,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block records that nothing is seen below that depth beneath the ridge axis, which matches the negated modality and the open lower bound."
        },
        {
          "row_index": 141,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives how deep the off-axis shallow activity west of that segment axis reaches, matching the bound and the unit."
        },
        {
          "row_index": 142,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the estimated pre-eruptive range for that segment after fractional crystallisation, with the unit and the estimate framing."
        },
        {
          "row_index": 143,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the measured barium floor in that segment samples relative to the southern segment and normal basalts, with the unit."
        },
        {
          "row_index": 144,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the approximate length of that segment with its unit."
        },
        {
          "row_index": 145,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the measured rubidium floor in those samples, with the unit."
        },
        {
          "row_index": 146,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the length of the southern segment with its unit."
        },
        {
          "row_index": 147,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the sub-solidus temperature for anhydrous peridotites at the boundary, which is the value, the unit and the material the row files it under."
        },
        {
          "row_index": 148,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The abstract block reports the depth band of the deep earthquakes along the ridge axis as a finding of the study, with the unit."
        },
        {
          "row_index": 149,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The results block gives the length of ridge axis the network covered, with the unit."
        },
        {
          "row_index": 150,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The caption block gives the depth band of the deep earthquakes beneath the ridge axis below the sea floor, but the reading nowhere identifies the block as the sixth figure caption, which the row states in its name."
        },
        {
          "row_index": 151,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The study-area block gives the half-spreading rate with its unit."
        },
        {
          "row_index": 152,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the approximate length of the ridge segment between the two transforms, with the unit."
        },
        {
          "row_index": 153,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the highest previously reported amount in melt and attaches it to that ridge, which is the subject."
        },
        {
          "row_index": 154,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the global carbon-to-barium trend with its spread and says it was defined from rare undegassed basalts and olivine inclusions, which covers the numerator, the denominator, the value, the uncertainty and the derived status."
        },
        {
          "row_index": 155,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the same barium ratio and spread as the constant used in the estimation, which matches the value, the uncertainty and the derived status."
        },
        {
          "row_index": 156,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the global carbon-to-rubidium trend with its spread and the same derivation from undegassed basalts and inclusions, covering every field the row projects."
        },
        {
          "row_index": 157,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the same rubidium ratio and spread as the constant used in the estimation, matching every projected field."
        }
      ]
    },
    {
      "question_id": "CQ-04",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "One returned row carries the preferred mechanism itself, with the modality marking it as a hypothesis and a separate disposition field marking it as the authors' preference, and its statement names degassing from the ascending melt as the cause of the deep activity. Adjacent rows carry the rest of what the question asks for: the chain from degassing through volume change and extensional stress to triggered earthquakes in the mantle, the pressure rise put forward as the trigger, and the caption reading of the deep earthquakes as volume change from degassing in the ascending melts. Epistemic status is explicit rather than inferred, on the fields and in the prose the rows point at. The row set also contains many witnesses that bear on nothing in the question, which follows from a type-only binding, but every requested part is directly addressed.",
      "source_locators": [
        "page:5:block:002",
        "page:5:block:003",
        "page:7:block:012"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block introduces barium as one of the trace elements the authors work from, so the constituent this row names is in the reading."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The abstract block presents carbon dioxide as the volatile the whole study turns on, which is all this row projects."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names water next to carbon dioxide as a control on solubility, and the row projects nothing beyond that name."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Rubidium appears in the cited block as the second trace element used for the ratio work, matching the name shown."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The introduction block names deep-rooted detachment faults as one of the associations reported elsewhere."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports normal faults cutting the core-complex surface."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The velocity-model block names the averaged model and its model number, which is what the row shows."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the solubility model used to place the saturation depth, matching the row."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The depth-resolution block names the fastest of the trial models and its number."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block attributes the solubility calculation to the named model."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names thermal modelling as the source of the temperature estimate, which is the name projected."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block names the one-dimensional velocity model the row identifies."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports an extinct hydrothermal vent field on the eastern flank of the first discontinuity."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure-caption block marks an inactive hydrothermal mound."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The compilation block names this seamount among the updated entries."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The compilation block names this massif and places it at a non-transform discontinuity."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The introduction block defines the brittle-ductile boundary and gives the abbreviation the row carries."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block spells out the lithosphere-asthenosphere boundary together with its abbreviation."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The caption block names the expected Moho interface."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block measures depth below the sea floor, naming the surface the row projects."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks speak of the brittle lithosphere, the feature named here."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block opens on oceanic crust, which is the feature the row names."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The discussion block names the Juan de Fuca plate as a comparison setting."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block refers to the cold lithosphere near the intersection, naming the feature."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The abstract block places the reported earthquakes in the mantle, so the feature is named where the row points."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:4:block:002",
            "page:5:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW All three cited blocks speak of melt, the material this row names."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006",
            "page:8:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks name the pre-eruptive melts."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:8:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The abstract and the methods block each name the primary melts."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The abstract block names the primitive melt."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block names the double-difference relocation method."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The magnitude block names the local magnitude scale the row projects."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block names the non-linear location algorithm."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The location block names the oct-tree search algorithm."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block names the active-source wide-angle refraction profile."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block names the trigger algorithm used to detect arrivals."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the Wadati diagrams used to obtain the velocity ratio."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block names the mapping tool and gives the same address the row shows."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block names the plotting toolbox; no address is projected on this record."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One cited block names the focal-mechanism package, the other gives the version and the address the row carries."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One cited block names the relocation program, the other gives its version and address."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One cited block names the location program, the other gives its address."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One cited block names the picking package, the other gives its address."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One cited block names the inversion program, the other gives its address."
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One cited block names the catalogue-analysis software, the other gives its address."
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The study-area block names this subsection and gives it the identifier the row shows."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The study-area block names the short ridge segment and gives it this identifier."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The study-area block names the segment south of the second discontinuity under this identifier."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002",
            "page:4:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks name this Icelandic volcano among the magmatic-tectonic comparisons."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The introduction block names axial melt lenses as the usual separator at faster ridges."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this Icelandic peninsula among the comparison cases."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names a deep magma reservoir under the pre-existing fractures."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the neo-volcanic ridge in the median valley."
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names volcanic cones among the axial morphology."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:1:block:001",
            "page:4:block:002",
            "page:5:block:006"
          ],
          "rationale": "DERIVATION_LOCAL The block states that the crust is built from melt derived from the mantle at spreading centres, which is this pairing and its direction, and the same block formalizes the melt endpoint."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:1:block:004"
          ],
          "rationale": "DERIVATION_LOCAL The block names the intersection segment under the identifier the row shows and says it is bounded on its eastern side by a westward dipping detachment fault; the same block formalizes the segment endpoint."
        },
        {
          "row_index": 55,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:4:block:001",
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL The block does say the segment is bounded by high-angle inward-dipping faults, but it never calls them normal faults, and the fault record on the far end of this pairing was formalized from a different block about faults cutting the core-complex surface; the pointer also lands in a block that formalizes neither endpoint."
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block sets out how the gas behaves during melting and crystallisation at depth and likens it to the highly incompatible trace elements, which is the claim, and the substance is the subject it is filed under."
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block ties solubility in silicate melts to pressure and to water content, so both the content of the claim and the substance it is about sit in the prose."
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block records that the trends have been used to compute primary-melt content for ridge segments worldwide, which is what the claim asserts about the gas."
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block compares the existing measurements on the two segments against the solubility computed at sample depth, the relation the claim names."
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:008"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block draws the comparison between the nucleation proposed here and the rapid degassing under active volcanoes, and the gas the row files it under is the degassing agent on both sides."
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block calls the two element ratios a good proxy for the concentration, which is the status the claim records."
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block spells out the assumption that the trace elements reflect the source and were not disturbed by later processes."
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports that earlier work reached pre-eruptive concentration through volatile to non-volatile element ratios, which is the approach named."
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block infers from the missing deep activity near the termination that this fault is no longer active, and the fault is the subject."
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block records the choice of the averaged model as best fitting and its use downstream, and that model is the subject."
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block compares the chosen model against the minimum model on residuals and on how many events each locates; both are one-dimensional velocity models, the entity the row files this under."
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the expected southward shallowing of the boundary and the cold-edge reason behind it, with the boundary as subject."
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block attributes the melt present at the boundary to a combination of the two volatiles and hedges it, which matches the hypothesised modality and the boundary as subject."
        },
        {
          "row_index": 69,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The caption block does carry the interpretation of the deep earthquakes as volume change from degassing in the hot ductile mantle, but nothing in the reading marks this block as the sixth figure caption, which the row asserts in its name."
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block runs the chain from degassing through volume change and extensional stress to triggered deep earthquakes and places them in the mantle, the subject."
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block infers the host of the events from the measured crustal thickness and puts them mostly below the crust, which is the claim and its subject."
        },
        {
          "row_index": 72,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block does carry the inference to a tectonic origin from exhumed mantle, but it never names the ridge-transform intersection the row attributes the inference to, and the record is about a subsection origin rather than about the mantle it is filed under."
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block raises freezing of melt at the base of the lithosphere as a possibility tied to observed reflections, matching the hedged modality and the subject."
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reads the depth of the microseismicity as melt residing, fractionating and evolving in the mantle, which is the claim about the subject."
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block proposes off-axis magmatism in the crust as the origin of the shallow swarm-like activity, so both the content and the crustal subject are present."
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block concludes from the modelled temperatures that the mantle beneath that segment axis is hot, which is the claim, with the mantle as subject."
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block sets out the expectation of a deep localized shear zone forming during detachment development and producing deep activity, and places it in the mantle."
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the earlier proposal that volatiles both focus melt beneath the axis and flush it away towards the boundary, so the melt is the subject and the content is there."
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states that melt is focused into a narrow zone beneath the axis as it rises, which is the claim about the material it is filed under."
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the gap in understanding of how these melts reach the surface, which is the claim, and the melt is the subject."
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block ties melt movement at depth to high strain rates and brittle failure lower down, matching the claim."
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block distinguishes primary melts in equilibrium with the source from pre-eruptive melts that have fractionated, which is the claim about the primary melt."
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the alignment of the deep events beneath that segment axis parallel to the axial faults and denies a cluster or swarm pattern; the bearing itself is recorded in the capture as not formalized."
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the tests concluding that the deep events beneath that ridge axis are required by the data and are not artifacts."
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block presents this as the fourth possibility and the one the authors prefer, which matches both the hypothesised modality and the preferred disposition, with the segment as subject."
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block concludes that magmatism dominates crustal accretion at that segment, which is the claim about the segment it is filed under."
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block records that no active vents have been seen on that segment axis, which matches the negated modality and the subject."
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block records that the segment shows no evidence of detachment faulting, matching the negated modality and the subject."
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block proposes the small pressure rise from degassing as the trigger of the events beneath that ridge axis and hedges it, matching the modality and the subject."
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports normal velocity ratios from tomography in that segment, which is the claim and its subject."
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the fraction lost to a nucleated gas phase by the time the melt reaches the sea floor, with the unit, and the gas is the subject."
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reads the activity beneath the discontinuity as putting the boundary at that approximate depth, which matches the value, the unit and the approximation flag."
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the depth the boundary would have under the cold-and-thick explanation and frames it as one explanation, matching the hypothesised modality."
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block pairs that hypothetical boundary depth with an isotherm band in degrees, under the same hedge."
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The introduction block gives the isotherm and its spread used to define the boundary at slow and ultraslow ridges."
        },
        {
          "row_index": 96,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The caption block does give the isotherm the boundary corresponds to, with its unit, but nothing in the reading marks the block as the sixth figure caption, which the row states in its name."
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reads the off-axis shallow activity as keeping the boundary above that depth, matching the open upper bound and the unit."
        },
        {
          "row_index": 98,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block carries the proposed melt proportion at the base of the boundary with its unit and its hedged status, but it presents the figure as a proposal made to explain observed reflections and never says it came from a model, which is what the row asserts as its determination."
        },
        {
          "row_index": 99,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the water-content ceiling inside the same proposal, with its unit, but as with the melt fraction it does not attribute the number to a model, so the modelled determination is unsupported."
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block concludes a ceiling on brittle thickness at the segment boundaries, which matches the bound, the unit and the subject."
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the age of the cold lithosphere behind the edge effect, with its unit."
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block attributes the thickness and its uncertainty to refraction work, so the value, the spread and the measured determination all hold."
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the depth band in the mantle over which continued degassing would produce earthquakes and hedges it, matching the modality and the subject."
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block ties the expected maximum earthquake depth to a ceiling on brittle thickness, matching the bound and the unit."
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the lower temperature bound for the mantle hosting these events, with the unit."
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block attributes the temperature band over that depth interval to thermal modelling, which covers the values, the unit and the modelled determination."
        },
        {
          "row_index": 107,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The caption block gives the crustal thickness beneath that segment with its uncertainty, but the reading nowhere identifies the block as the sixth figure caption, which the row claims in its name."
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the age of the western flank crust, with its unit."
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the age ceiling for a magmatically accreted young crust in the aside about the fastest velocity model."
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The abstract block gives the approximate range in the primary melts and attributes it to sample syntheses and geochemical analyses, which covers the bounds, the unit and the derived status."
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block makes the program the estimator of the error ellipsoid and gives the confidence level with its unit, so the quantity is predicated of the tool the row files it under."
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block attaches the depth to which velocity is constrained to the refraction profile itself, which is the subject, with the approximation and the unit."
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the calculated content for the melts of that segment, flagged as calculated, with the unit."
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the calculated content for the southern segment as the comparison, with the unit."
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states the floor on primary-melt concentration along that segment, matching the open lower bound and the estimated determination."
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the barium-based pre-eruptive estimate for that segment, with the unit and the estimate framing."
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the barium-based pre-eruptive estimate for the southern segment, with the unit."
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the barium-based primary-melt estimate for that segment, with the unit and the estimate framing."
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the barium-based primary-melt estimate for the southern segment."
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the rubidium-based pre-eruptive estimate for that segment, with the unit."
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the rubidium-based pre-eruptive estimate for the southern segment, with the unit."
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the rubidium-based primary-melt estimate for that segment, with the unit."
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium-based primary-melt estimate for the southern segment."
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the observed depth band of the deep events beneath that segment axis as a measurement, with the unit."
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The results block lists the approximate depth band of the deep activity beneath that segment axis among the three key observations."
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block records that nothing is seen below that depth beneath the ridge axis, which matches the negated modality and the open lower bound."
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives how deep the off-axis shallow activity west of that segment axis reaches, matching the bound and the unit."
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the estimated pre-eruptive range for that segment after fractional crystallisation, with the unit and the estimate framing."
        },
        {
          "row_index": 129,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the measured barium floor in that segment samples relative to the southern segment and normal basalts, with the unit."
        },
        {
          "row_index": 130,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the approximate length of that segment with its unit."
        },
        {
          "row_index": 131,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the measured rubidium floor in those samples, with the unit."
        },
        {
          "row_index": 132,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the length of the southern segment with its unit."
        },
        {
          "row_index": 133,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the global carbon-to-barium trend with its spread and says it was defined from rare undegassed basalts and olivine inclusions, which covers the numerator, the denominator, the value, the uncertainty and the derived status."
        },
        {
          "row_index": 134,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the same barium ratio and spread as the constant used in the estimation, which matches the value, the uncertainty and the derived status."
        },
        {
          "row_index": 135,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the global carbon-to-rubidium trend with its spread and the same derivation from undegassed basalts and inclusions, covering every field the row projects."
        },
        {
          "row_index": 136,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the same rubidium ratio and spread as the constant used in the estimation, matching every projected field."
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
