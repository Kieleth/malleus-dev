# Malleus paper v4 run-15 source-grounded review record

Template. The row counts are substituted at freeze, from the frozen cell's own
query result, at the same time as `paper-v4/evaluation-v4/review-task-v4.template.md`.
No placeholder may survive instantiation.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

Fill one `rows` entry per returned row, in order, zero-based: 28 for
CQ-01, 104 for CQ-02, 154 for CQ-03, 147 for
CQ-04, 433 in all. Cite reading block ids only. Write the reasons in
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
    "review_input_manifest_sha256": "sha256:784f8e3761575b59d7e376dfc846d4376d8a9400eb2985bb4e393f0e9f684dcb"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-preliminary-run-15",
    "completed_at": "2026-09-05T18:47:17Z"
  },
  "questions": [
    {
      "question_id": "CQ-01",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The rows name one campaign and give nineteen deployed instruments with a scope that says they make up the network, so the campaign and the deployed instrument count are each answered by a single row. The observing network itself comes back only as an instrument record whose projection is a bare name; that it is a network is recoverable only from the scope text of a count row, and no returned row ties the campaign or the instruments to the microseismicity data, so the acquisition part of the question is left for the reader to join up. Further instrument counts arrive beside the deployed one, and most of the block is method and software records that answer nothing here.",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block the record's own derivation reaches names the cruise with the same name the row carries, and the row asserts nothing beyond that name."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block introduces the ocean-bottom seismometers under the plural abbreviation the row uses as the record name."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names a CO2 solubility model and uses it to obtain a saturation pressure and depth; the row carries only that name."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says the hypocentres were relocated with a double-difference location method, which is the name the row carries."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says first-motion polarities of the P phase were what the focal mechanisms were determined from."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the minimum 1-D velocity model that was searched for as a check on the chosen model."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says magnitudes were determined on the local magnitude scale the row names."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block identifies Model 1 as the fastest of the five velocity models tried."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block identifies Model 5 as the average velocity model selected as best fitting."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says a non-linear earthquake location algorithm produced the initial hypocentres."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says the velocity model used for travel times came from an active-source refraction experiment of the wide-angle kind the row names."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the short-term-average over long-term-average trigger used to detect arrivals automatically."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports what thermal modelling gives for the temperature at depth, so the modelling method the row names is present."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says Wadati diagrams yielded the velocity ratio used in the inversion."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block names this tool and gives the address the row records as its resource URL."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010",
            "page:8:block:011"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block names the toolbox and starts its address, which the text layer breaks across into the following block; the version the row records is carried by the numeral in the tool's own name rather than stated separately."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block gives this package's name, its version in parentheses and its address, matching all three projected fields."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block gives the program's name, its version in parentheses and its address, matching all three projected fields."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the location code and gives the address the row records."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the phase-picking software and gives the address the row records."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the velocity-inversion program and gives the address the row records."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the catalogue-analysis software and gives the address the row records."
        },
        {
          "row_index": 22,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement puts the detection threshold strictly above six instruments, while the row records six as a stated minimum, so the count and the inequality do not agree; the instrument subject and the relocated-event scope are supported."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block requires every retained event to have been seen on at least five instruments, which is the count, the scope and the modality the row records."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the deployed network held nineteen ocean-bottom seismometers, which is exactly the count and the scope the row records."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block says seventeen usable instruments supplied the automatically detected first arrivals, matching the count and the scope."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives an instrument spacing of about thirty kilometres, matching the value, the unit and the approximate qualification."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block attributes the weakness of the focal mechanism solutions to the wide instrument spacing of about thirty kilometres, which carries the value, the unit and the negated framing the row records."
        }
      ]
    },
    {
      "question_id": "CQ-02",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "The rows name the ridge subsection the deep microseismicity is associated with and place those events beneath its ridge axis with a depth band, both carried by rows whose own fields say so rather than left to inference: one observation gives the approximate band beneath that segment's ridge axis and another the narrower band observed beneath the same axis, each with the segment as its subject, and a third puts the shallow off-axis activity west of that axis. The segment is also returned as an entity in its own right and as a neighbour of the two discontinuities that bound it, which fixes which subsection is meant. Both requested parts are therefore answered directly. Much of the block is unrelated matter, comparison sites and melt chemistry among it, and the event population itself is not returned as its own record, but neither costs the reader the answer.",
      "source_locators": [
        "page:2:block:004",
        "page:2:block:006",
        "page:3:block:001",
        "page:1:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this volcano among the magmatic-tectonic comparisons, and the row carries nothing but that name."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block speaks of the axial valley floor near the detachment termination, so the feature the row names is present in the prose its derivation reaches."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block defines the brittle-ductile boundary and introduces the abbreviation, so both the name and the feature kind the row carries are supported."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this transform as one of the two bounding the ridge segment studied."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block opens on oceanic crust formed from mantle-derived melt, so the feature the row names is in the prose."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block describes the eastern boundary of the intersection segment as a westward dipping detachment fault, matching both the name and the feature kind."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block places the study in the equatorial Atlantic Ocean, which is the whole content of the row."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this peninsula among the Icelandic magmatic-tectonic comparisons."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this ridge as one of the ultraslow settings at which deep earthquakes in the mantle have already been reported."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports an extinct hydrothermal vent field on the eastern flank of the first discontinuity, supporting both the name and the feature kind."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says the seismicity of this country occurs in thickened crust, so the place name the row carries is in the prose unbroken."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure caption block reports an inactive hydrothermal mound inferred from the dive observations, which is the name the row carries."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block compares the sub-lithospheric reflections with those seen beneath this young plate, naming it as the row does."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block lists a seamount of this ridge among the sites whose maximum depths were updated."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block spells out the lithosphere-asthenosphere boundary and introduces the abbreviation, giving both the name and the feature kind the row carries."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block contrasts the cooled brittle layer with the partly molten material under it, so the feature the row names is in the prose."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The abstract block places the reported deep earthquakes in the mantle, so the feature the row names is in the prose its derivation reaches."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block gives the ridge's full name and the abbreviation the row carries as the record name."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this island offshore of which the deep magmatic-tectonic seismicity was observed."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure caption block calls this an expected interface drawn as a dashed line, giving both the name and the feature kind the row carries."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block describes a neo-volcanic ridge with the same strike the row records as the orientation."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:2:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first block has normal faults cutting the complex's surface and the second calls those faults high-angle, so the name and the feature kind are each supported in a block the record's derivations reach."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first block introduces the two non-transform discontinuities and names this one; the second gives its strike, which is the orientation the row records."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first block names the second discontinuity and its kind; the second gives the strike the row records as the orientation."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block introduces the oceanic core complex east of the axis and gives its abbreviation, supporting both the name and the feature kind."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says this massif sits at a non-transform discontinuity and was included for reference, so the name the row carries is in the prose."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this subsection when it divides the studied ridge into four parts."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this short segment when it divides the studied ridge into four parts."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first block names the segment south of the second discontinuity; the second gives its length and the strike the row records as the orientation."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:10:block:040"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first block names this transform as one of the two bounding the segment; the feature kind comes from the bibliographic block the record's own derivation reaches, which spells the name out as a transform fault."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block spells out the ridge-transform intersection and gives the abbreviation, supporting both the name and the feature kind."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block describes semi-brittle high-temperature mylonite shear zones in the mantle, which is both the name and the feature kind the row records."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block spells out the Southwest Indian Ridge and gives the abbreviation the row carries as the record name."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The block that formalizes the relation names both endpoints in one sentence, placing the ridge in that ocean, and the containment the row asserts is exactly what it says."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:2:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The relation's block says normal faults heavily cut the complex's surface and names both endpoints; the second block supplies the high-angle qualifier the target projection carries."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL The caption block that formalizes the relation puts the complex at the ridge's outside corner and names both endpoints."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The relation's block says the intersection segment is bounded to the east by that detachment and names both endpoints, including the segment's own label."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The relation's block places this segment immediately south of the first discontinuity, which supports the adjacency and names both endpoints."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The relation's block calls the southern segment the adjacent one to the studied segment, naming both endpoints in the same sentence."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The relation's block names the segment south of the second discontinuity, which supports the adjacency and carries both endpoints."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DERIVATION_LOCAL The relation's block puts the extinct vent field on the eastern flank of the first discontinuity and names both endpoints."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement has the axis moving eastward, away from the complex's termination and under its faulted dome, so the complex is the feature the claim is predicated around rather than an incidental mention, and the direction the row records is the one stated."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement offers a cold and thick lithosphere as one explanation for the deep events and the block then argues against it, which matches the hypothesised modality and the not-supported disposition the row records."
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement is about whether the unexpectedly deep events beneath this ridge's axis are a location artifact and concludes they are not, so the claim is predicated on events at the subject feature."
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement infers from the absence of deep events near the termination that this detachment is inactive, which is the subject and the question of present activity the row records."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement places most of these earthquakes in the mantle below ten kilometres, which is the subject and the placement the row records."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement offers vigorous hydrothermal circulation cooling the lithosphere as a hypothesis for the large depths, and the rest of the block withdraws it, matching the modality and disposition the row records."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement offers association with magmatic-tectonic activity as the third possibility for these mantle earthquakes and the argument that follows rejects it, matching the modality and disposition the row records."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement concludes that magmatism dominates crustal accretion at this segment, which is the subject and the content the row records."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement attributes the melt present at this boundary to a combination of the two volatiles, which is the subject and the hypothesised cause the row records."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement has the ascending melt residing in the mantle at the observed depths, which is the subject and the content the row records."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement offers localized high strain in mylonite shear zones as another hypothesis and the block then says the observations do not support it, matching the modality and disposition the row records."
        },
        {
          "row_index": 52,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement supports the content, that the microseismicity record is a brief snapshot which may not represent activity over years. What it does not support is that this is a record about the ridge: the thing the statement predicates the temporal reach of is the dataset, and the ridge is named only as what the dataset informs about."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the same total and indexes it to the vicinity of this intersection region, so the count is predicated on the subject rather than merely mentioning it."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives the same number of events located along this ridge, in the same sentence that names it, and the row carries no statement digest to check."
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives the same number of events located along this transform, in the same sentence that names it, and the row carries no statement digest to check."
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement puts the boundary at about ten kilometres beneath the second discontinuity, matching the value, the unit and the approximate qualification."
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement says the boundary would lie about twenty kilometres deep under the cold-lithosphere explanation, which is the value and the conditional framing the row records."
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the isotherm the maximum earthquake depth is taken to correspond to as a central value with a symmetric tolerance, which is the range and the uncertainty the row records."
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement says the boundary stays shallower than ten kilometres off axis, matching the upper bound and the open lower end the row records."
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement caps the brittle lithosphere at roughly ten kilometres at the segment boundaries, matching the bound; the subject occurs in the block with a hyphenated line break, which the row's own tag list carries."
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the average concentration reported across several segments of this region, matching the value, the unit and the approximate qualification."
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the primary-melt range from the barium proxy for this segment, and the row's bounds and unit are the ones stated."
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same located statement gives the barium-proxy primary-melt range for the southern segment, and the row's bounds and unit are the ones stated for it."
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the pre-eruptive range from the barium proxy for this segment, matching the row's bounds and unit."
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the pre-eruptive barium-proxy range for the southern segment, matching the row's bounds and unit."
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the calculated volatile content of the melts generated along this segment, matching the row's bounds and unit."
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same located statement gives the calculated content for the southern segment as the contrast, matching the row's bounds and unit."
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the highest concentration reached across those segments as a ceiling, which is the upper bound and the open lower end the row records."
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the primary-melt range from the rubidium proxy for this segment, matching the row's bounds and unit."
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same located statement gives the rubidium-proxy primary-melt range for the southern segment, matching the row's bounds and unit."
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the pre-eruptive range from the rubidium proxy for this segment, matching the row's bounds and unit."
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the pre-eruptive rubidium-proxy range for the southern segment, matching the row's bounds and unit."
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement dates the crust of the western flank in the same clause that gives its thickness, and the age and unit the row records are the ones stated."
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the thickness of that crust with a symmetric tolerance, matching the value and the uncertainty the row records; the figure caption block the record also reaches repeats it for this segment."
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located caption statement gives the depth band of the deep earthquakes beneath this ridge's axis below the sea floor, matching the row's bounds and unit."
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement has the migrating melt continuing to degas and producing earthquakes in the mantle across the band the row records, and the row's hypothesised modality matches the conditional wording."
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the half-spreading rate of this ridge in the study area, matching the value and the unit the row records."
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement places these earthquakes in hot mantle above the temperature the row records, which is the open lower bound it carries."
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the depths of the two comparison sites in this country as greater than the value the row records; the place name is split by a line break in the block and the row's tag list carries that broken form."
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement pairs the hypothetical boundary depth with the isotherm range the row records, matching its bounds and unit."
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement attributes the cold-edge effect near the intersection to lithosphere of the age the row records, so the value and the indexing to that setting are both stated."
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement reports the modelled temperature over the depth interval the row's name gives and concludes the mantle there is hot, matching the value range, the unit and the modelled determination."
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the length of this ridge's axis covered by the network, matching the value and the unit the row records."
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the approximate length of the ridge segment between the two transforms, matching the value, the unit and the approximate qualification."
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the depths offshore this island as greater than the value the row records, which is the open lower bound it carries."
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the width of the median valley of that segment, matching the value and the unit; the subject occurs in the block under the tag the row lists."
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement reports the melt fraction proposed at the base of this boundary, matching the value, the unit and the approximate qualification."
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the length of this discontinuity, matching the value, the unit and the approximate qualification."
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement says the earthquakes beneath this discontinuity reach down to about the depth the row records as its upper bound."
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement bounds the depths observed beneath this discontinuity below the value the row records, matching the open upper bound."
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the normal depth band of the earthquakes beneath this southern discontinuity, matching the row's bounds and unit."
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the ridge offset at this discontinuity, matching the value, the unit and the approximate qualification."
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same located statement bounds the depths observed beneath the complex below the value the row records, matching the open upper bound."
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives shallow focal depths for the cluster observed west of the axial valley, matching the row's bounds, unit and approximate qualification."
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement says the off-axis shallow microseismicity west of this segment's axis reaches down to the value the row records as its upper bound."
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the estimated pre-eruptive concentration range for this segment, matching the row's bounds, unit and estimated determination."
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the depth band of the deep earthquakes observed beneath this segment's axis, matching the row's bounds and unit."
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement puts the deep microseismicity at the approximate band the row records beneath this segment's ridge axis, matching the bounds, the unit and the approximation."
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the length of this segment, matching the value, the unit and the approximate qualification."
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the length of this segment, matching the value and the unit the row records."
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement gives the length of the eastern part of this transform covered by the network, matching the value and the unit."
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement reports the highest melt concentration previously reported at this ridge, matching the value and the unit the row records."
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located statement caps the water content proposed at the base of this boundary at the value the row records, matching the open upper bound and the unit."
        }
      ]
    },
    {
      "question_id": "CQ-03",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The rows do carry both halves the question asks for: the depth interval of the deep events beneath the central segment's axis, in kilometres, with the record marking it as measured, and the calculated carbon dioxide interval of the primary melts, in weight per cent, with the record marking it as estimated from the trace-element proxies. What keeps this from being a clean answer is that the returned set is scoped by record type rather than by the question, so those rows sit among many that answer nothing asked, and it carries several competing intervals on each axis: three depth intervals for the axial events and, for carbon dioxide, the primary melt values from two different proxies alongside pre-eruptive values and the southern comparison segment's values. Each row's subject and quantity kind let a reader tell them apart, but nothing in the result marks which pairing is the central association the question asks about.",
      "source_locators": [
        "page:2:block:004",
        "page:2:block:006",
        "page:7:block:012",
        "page:5:block:005",
        "page:8:block:007",
        "page:8:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on the compiled analyses lists barium among the incompatible trace elements measured in the segment's samples, which is exactly what the record's name and material kind assert.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block describing the sea floor names basalts as an observed rock type; the record asserts nothing beyond the name.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The opening block names carbon dioxide as one of the two volatiles, which carries both the name and the volatile classification.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same opening sentence names water as the second volatile, supporting the name and the classification.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on crustal accretion names melt as the mantle-derived material; the record carries only the name.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block spells out mid-ocean ridge basalt and its abbreviation.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block names olivine as the host of the melt inclusions used to set the volatile ratios.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on the sea floor observations names peridotites alongside pillow basalts.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The methods block distinguishes pre-eruptive melts from primary melts by name.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The opening block names the primary melts as the melts whose carbon dioxide content is reported.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same enrichment sentence lists rubidium with barium as an incompatible trace element.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The opening block names volatiles as a class and gives its two members.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block raising the magmatic-tectonic possibility names the volcano among its comparison cases.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on the shallow seismicity names the axial valley as a feature of the study area.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block introducing the boundary gives both the abbreviation and the words it stands for.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block placing the study area names Chain as one of the two transform faults bounding the ridge segment.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on crustal accretion names the oceanic crust.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on the intersection segment names a westward dipping detachment fault, which is the record's feature kind in substance.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block placing the study names the equatorial Atlantic Ocean.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same comparison sentence names the peninsula.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block generalising the model to ultraslow ridges names the ridge.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block reports an extinct hydrothermal vent field on the discontinuity's flank, which supports both the name and the feature kind; the missing space in the text layer is a projection artifact.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The comparison sentence names Iceland, broken across a line by the text layer.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The figure caption names an inactive hydrothermal mound suggested by the dive observations.",
          "source_locators": [
            "page:2:block:007"
          ]
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The closing discussion block names the plate as the place where comparable reflections were seen.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The compilation block names the ridge whose seamount data were updated.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on volatile-driven melt flushing gives both the boundary's full name and its abbreviation.",
          "source_locators": [
            "page:5:block:010"
          ]
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block defining the boundary names the brittle lithosphere.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The opening block names the mantle as the site of melting and of the reported earthquakes.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block placing the study gives the ridge's full name and its abbreviation.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The comparison sentence names the island and the ocean it lies in.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The schematic caption names the Moho and calls it an interface, matching name and feature kind.",
          "source_locators": [
            "page:7:block:011"
          ]
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block describing the segment gives the neo-volcanic ridge and the orientation the record carries.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on the shallow events names high-angle normal faults, matching both name and feature kind.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW One block gives the discontinuity's length and the orientation the record carries; the block introducing the subsections is where the discontinuities are called non-transform.",
          "source_locators": [
            "page:2:block:001",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW One block gives the second discontinuity's offset and the orientation the record carries; the subsection block supplies the non-transform wording.",
          "source_locators": [
            "page:2:block:001",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on the intersection segment gives the abbreviation and its expansion.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The compilation block names the massif and places it at a non-transform discontinuity.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block naming the four subsections gives this one's name.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same subsection block names the short ridge segment.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block ending the tectonic description gives the southern segment's name and the orientation the record carries.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block placing the study names the transform fault; the same block treats it as one of the bounding transforms.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same block gives the intersection's abbreviation and its expansion.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block raising the shear-zone hypothesis names semi-brittle high-temperature mylonite shear zones, matching name and feature kind.",
          "source_locators": [
            "page:3:block:003"
          ]
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on the cold-lithosphere explanation gives the ridge's full name and its abbreviation.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block computing saturation says a carbon dioxide solubility model was used.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The results block names the double-difference relocation step applied after the initial locations.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The focal-mechanism block names first-motion polarities as the input to the solutions.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on the velocity-model check names the minimum one-dimensional model that was searched for.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The magnitude block names the local magnitude scale used.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The depth-resolution block identifies this model as the fastest of the five.",
          "source_locators": [
            "page:7:block:009"
          ]
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block selecting a velocity model identifies this one as the best-fitting average model.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The results block names the non-linear location algorithm used for the initial hypocenters.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The results block names the active-source wide-angle refraction profile used to fix the velocity model.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The results block names the trigger algorithm used for automatic arrival detection.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The introduction block attributes the expected earthquake depths to thermal models.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on the velocity ratio names Wadati diagrams as its source.",
          "source_locators": [
            "page:7:block:002"
          ]
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block names the tool and gives the address the record carries; the space inside the address is a line-wrap artifact of the text layer.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block names the toolbox and begins its address, which continues into the following block; read together the two give the address the record carries, and the numeral in the tool's name is the version the record records.",
          "source_locators": [
            "page:8:block:010",
            "page:8:block:011"
          ]
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block gives the package, its version in parentheses and its address.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same block gives the relocation program, its version in parentheses and its address.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same block names the location code and gives its address.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same block names the picking software and gives its address.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same block names the inversion program and gives its address.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same block names the catalog-analysis software and gives its address.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block defining the global trends gives the carbon dioxide to barium ratio with its stated spread, and names barium, which is what the record's subject reference points at.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the carbon dioxide to rubidium ratio with its stated spread and names rubidium, the record's subject reference.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives the velocity ratio used to estimate shear-wave velocity in the inversion; the record's projection carries no subject.",
          "source_locators": [
            "page:7:block:002"
          ]
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block names olivine melt inclusions among the materials the global trends were defined from.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block says the published analyses of these samples inside the network footprint were compiled.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The figure caption names popping rocks as one of the plotted sample sets.",
          "source_locators": [
            "page:6:block:005"
          ]
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The bathymetry caption names the rock samples plotted on the map.",
          "source_locators": [
            "page:2:block:007"
          ]
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The block that formalises the relation also formalises both endpoints, and it places the ridge inside the equatorial Atlantic in so many words.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation's block formalises the faults endpoint and says the complex's surface is heavily cut by them; the complex itself is introduced in earlier blocks.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation's block formalises both endpoints and puts the core complex on the ridge's outside corner.",
          "source_locators": [
            "page:2:block:007"
          ]
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation's block formalises both endpoints and says the intersection segment, which the same block names as this record, is bounded by the detachment fault.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation's block formalises both endpoints and puts this segment immediately south of the first discontinuity.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation's block formalises both endpoints and calls the southern segment the adjacent one.",
          "source_locators": [
            "page:8:block:005"
          ]
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation's block formalises both endpoints and names the southern segment as the ridge lying south of the second discontinuity.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation's block formalises the vent-field endpoint and puts the field on the eastern flank of the discontinuity; the discontinuity is introduced in earlier blocks.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence gives the authors' causal reading, that the deep mantle earthquakes follow from degassing of the volatile, and names the volatile the subject resolves to; a later block the record also reaches marks it as the preferred of four possibilities.",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002"
          ]
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence says the sea floor basalts are mostly degassed, and the surrounding block ties those samples to the two segments the record's name mentions.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence spells out the assumption the trace-element estimate rests on and names the volatile the subject resolves to.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence gives the eastward relocation of the ridge axis and describes it entirely by reference to the core complex the subject resolves to.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence offers a cold, thick lithosphere as the explanation, and the rest of the block withdraws it, which is the disposition the record carries.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence argues that the unexpected depths beneath the ridge axis are not a location artifact, and names the ridge the subject resolves to.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence infers the detachment fault is inactive from the absence of deep seismicity beneath the valley floor.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence places most of the events in the mantle below ten kilometres, which is what the record's name asserts.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence puts hydrothermal cooling of the lithosphere forward as a hypothesis and the rest of the block sets it aside, matching the recorded disposition.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence offers the magmatic-tectonic association as the third possibility; a later block the record also reaches withdraws it, matching the recorded disposition.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence concludes that magmatism dominates crustal accretion at the segment the subject resolves to.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence attributes melt at the boundary to a combination of the two volatiles, and the boundary is the subject the record resolves to.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence infers from the observed depths that ascending melt resides in the mantle at those depths.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence raises localized high strain in mylonite shear zones as a hypothesis and the block then rules it out for this segment, matching the recorded disposition.",
          "source_locators": [
            "page:3:block:003"
          ]
        },
        {
          "row_index": 94,
          "source_support": "PARTIAL",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence supports the claim itself, that the seismic record is a brief snapshot in time, and it does name the ridge; but what the claim is predicated of is the temporal reach of the recorded dataset, not the ridge the subject reference resolves to, so the subject projection is only partly borne out.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence gives the number of earthquakes located and confines it to the region around the intersection the subject resolves to.",
          "source_locators": [
            "page:2:block:003"
          ]
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "rationale": "SUBJECT_IN_BLOCK The relocation block states how many events ended up along the ridge; both the count and its scope come from that sentence, and the record carries no statement digest.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "rationale": "SUBJECT_IN_BLOCK The same relocation sentence gives the transform fault's event total and its scope; the record carries no statement digest.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The opening block gives the approximate mass fraction of carbon dioxide in the primary melts, with the unit, and says it comes from a synthesis of rock analyses rather than direct measurement.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the lower bound on barium in the segment's samples with its unit.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states the floor on primary melt carbon dioxide for the studied segment, with its unit, as the outcome of the calculation.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the proportion of the volatile lost when a gas phase nucleates.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same enrichment sentence gives the rubidium floor and its unit.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the approximate temperature at which melt is present for anhydrous peridotite at the boundary.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block puts the boundary at about ten kilometres beneath the southern discontinuity, read off the observed seismicity.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the depth the boundary would take under the cold-lithosphere explanation and marks that reading as hypothetical.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 106,
          "source_support": "PARTIAL",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the isotherm as a single figure with a stated tolerance. The row expands that tolerance into the interval and then carries the same tolerance again as a separate uncertainty, so the interval and the uncertainty are not both supported as independent facts.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block says the boundary stays shallower than ten kilometres off axis, with the unit.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block caps the brittle lithosphere at about ten kilometres at the segment boundaries.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the average carbon dioxide concentration reported for the region's segments with its unit and credits it to earlier work.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the primary melt carbon dioxide interval derived from the barium proxy for this segment, with its unit.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the barium-derived interval for the southern segment the subject resolves to.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the pre-eruptive interval estimated from barium for this segment.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the lower pre-eruptive interval estimated from barium for the southern segment.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The results block gives the calculated volatile content of the melts generated along this segment, with its unit.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the comparison figure for the southern segment.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the ceiling of the regional carbon dioxide concentrations with its unit.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the rubidium-derived primary melt interval for this segment.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the rubidium-derived interval for the southern segment.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the pre-eruptive interval estimated from rubidium for this segment.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the lower pre-eruptive interval estimated from rubidium for the southern segment.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block dates the crust of the western flank in the same clause that gives its thickness.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK That clause gives the thickness and its tolerance, and the schematic caption repeats the same figure for the segment.",
          "source_locators": [
            "page:2:block:006",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The schematic caption gives the depth interval below sea floor of the deep events beneath the ridge axis.",
          "source_locators": [
            "page:7:block:012"
          ]
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the depth interval over which continued degassing would produce earthquakes and marks it as expected rather than observed.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block placing the study gives the half-spreading rate with its unit.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block puts the mantle hosting these earthquakes above eleven hundred degrees.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The comparison sentence gives the depth floor for the Icelandic cases; the country's name is broken across a line by the text layer.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the isotherm interval the hypothetical boundary depth would correspond to.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 129,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the age of the cold lithosphere behind the edge effect.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 130,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the temperature interval at those depths and attributes it to thermal modelling, which is the determination the record carries.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 131,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The acquisition block gives the length of ridge axis the network covered.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 132,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the approximate length of the ridge segment between the two transform faults.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 133,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The comparison sentence gives the depth floor for the Mayotte case.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 134,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the width of the median valley, which is the other name the subject carries.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 135,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the melt fraction proposed at the base of the boundary.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 136,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the discontinuity's approximate length.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 137,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block says the events beneath the southern discontinuity reach about ten kilometres.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 138,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block caps the depth range observed beneath the southern discontinuity.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 139,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The key-observations block gives the normal-depth interval beneath the southern discontinuity.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 140,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the ridge offset at the discontinuity.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 141,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same capping sentence gives the shallower ceiling beneath the core complex.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 142,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the shallow focal depths of the cluster on the western side of the valley.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 143,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the depth the off-axis shallow seismicity west of the segment axis reaches.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 144,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the estimated pre-eruptive carbon dioxide interval for the segment with its unit.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 145,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the observed depth interval of the deep earthquakes beneath the segment's axis.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 146,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The key-observations block gives the approximate depth interval of the deep microseismicity beneath the segment's ridge axis.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 147,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the segment's approximate length.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 148,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the southern segment's length.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 149,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The acquisition block gives the length of the transform fault the network covered.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 150,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the highest melt carbon dioxide previously reported at that ridge.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 151,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same proposal gives the ceiling on water content at the base of the boundary.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 152,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block defining the global trends gives the carbon dioxide to barium ratio with its spread and names barium, which the subject reference resolves to.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 153,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the carbon dioxide to rubidium ratio with its spread and names rubidium.",
          "source_locators": [
            "page:5:block:004"
          ]
        }
      ]
    },
    {
      "question_id": "CQ-04",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "One row carries the preferred mechanism as a claim: its located sentence attributes the deep mantle earthquakes to degassing of carbon dioxide from the ascending melt, the record marks the claim a possibility with a preferred disposition, and a further block the same record reaches marks it as the last of the four possibilities and the one the authors favour. The three rejected alternatives are returned beside it carrying an unsupported disposition, so preference is distinguishable from rejection. That covers ascending melt, the degassing, the earthquake trigger and the epistemic status. The volume change and the extensional stress the mechanism turns on are not addressed by any returned row: the sentence that states them formalises only the name of the mantle, and the pressure-increase observation that the retained capture names as a formalisation target of the neighbouring sentence is absent from the returned witnesses. Two of the requested parts therefore have no row of their own.",
      "source_locators": [
        "page:1:block:001",
        "page:5:block:002",
        "page:5:block:003",
        "page:4:block:002",
        "page:3:block:001",
        "page:3:block:002",
        "page:3:block:003"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on the compiled analyses lists barium among the incompatible trace elements measured in the segment's samples, which is exactly what the record's name and material kind assert.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block describing the sea floor names basalts as an observed rock type; the record asserts nothing beyond the name.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The opening block names carbon dioxide as one of the two volatiles, which carries both the name and the volatile classification.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same opening sentence names water as the second volatile, supporting the name and the classification.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on crustal accretion names melt as the mantle-derived material; the record carries only the name.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block spells out mid-ocean ridge basalt and its abbreviation.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block names olivine as the host of the melt inclusions used to set the volatile ratios.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on the sea floor observations names peridotites alongside pillow basalts.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The methods block distinguishes pre-eruptive melts from primary melts by name.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The opening block names the primary melts as the melts whose carbon dioxide content is reported.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same enrichment sentence lists rubidium with barium as an incompatible trace element.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The opening block names volatiles as a class and gives its two members.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block raising the magmatic-tectonic possibility names the volcano among its comparison cases.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on the shallow seismicity names the axial valley as a feature of the study area.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block introducing the boundary gives both the abbreviation and the words it stands for.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block placing the study area names Chain as one of the two transform faults bounding the ridge segment.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on crustal accretion names the oceanic crust.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on the intersection segment names a westward dipping detachment fault, which is the record's feature kind in substance.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block placing the study names the equatorial Atlantic Ocean.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same comparison sentence names the peninsula.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block generalising the model to ultraslow ridges names the ridge.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block reports an extinct hydrothermal vent field on the discontinuity's flank, which supports both the name and the feature kind; the missing space in the text layer is a projection artifact.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The comparison sentence names Iceland, broken across a line by the text layer.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The figure caption names an inactive hydrothermal mound suggested by the dive observations.",
          "source_locators": [
            "page:2:block:007"
          ]
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The closing discussion block names the plate as the place where comparable reflections were seen.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The compilation block names the ridge whose seamount data were updated.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on volatile-driven melt flushing gives both the boundary's full name and its abbreviation.",
          "source_locators": [
            "page:5:block:010"
          ]
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block defining the boundary names the brittle lithosphere.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The opening block names the mantle as the site of melting and of the reported earthquakes.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block placing the study gives the ridge's full name and its abbreviation.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The comparison sentence names the island and the ocean it lies in.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The schematic caption names the Moho and calls it an interface, matching name and feature kind.",
          "source_locators": [
            "page:7:block:011"
          ]
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block describing the segment gives the neo-volcanic ridge and the orientation the record carries.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on the shallow events names high-angle normal faults, matching both name and feature kind.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW One block gives the discontinuity's length and the orientation the record carries; the block introducing the subsections is where the discontinuities are called non-transform.",
          "source_locators": [
            "page:2:block:001",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW One block gives the second discontinuity's offset and the orientation the record carries; the subsection block supplies the non-transform wording.",
          "source_locators": [
            "page:2:block:001",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on the intersection segment gives the abbreviation and its expansion.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The compilation block names the massif and places it at a non-transform discontinuity.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block naming the four subsections gives this one's name.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same subsection block names the short ridge segment.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block ending the tectonic description gives the southern segment's name and the orientation the record carries.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block placing the study names the transform fault; the same block treats it as one of the bounding transforms.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same block gives the intersection's abbreviation and its expansion.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block raising the shear-zone hypothesis names semi-brittle high-temperature mylonite shear zones, matching name and feature kind.",
          "source_locators": [
            "page:3:block:003"
          ]
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on the cold-lithosphere explanation gives the ridge's full name and its abbreviation.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block computing saturation says a carbon dioxide solubility model was used.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The results block names the double-difference relocation step applied after the initial locations.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The focal-mechanism block names first-motion polarities as the input to the solutions.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on the velocity-model check names the minimum one-dimensional model that was searched for.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The magnitude block names the local magnitude scale used.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The depth-resolution block identifies this model as the fastest of the five.",
          "source_locators": [
            "page:7:block:009"
          ]
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block selecting a velocity model identifies this one as the best-fitting average model.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The results block names the non-linear location algorithm used for the initial hypocenters.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The results block names the active-source wide-angle refraction profile used to fix the velocity model.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The results block names the trigger algorithm used for automatic arrival detection.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The introduction block attributes the expected earthquake depths to thermal models.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The block on the velocity ratio names Wadati diagrams as its source.",
          "source_locators": [
            "page:7:block:002"
          ]
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block names the tool and gives the address the record carries; the space inside the address is a line-wrap artifact of the text layer.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block names the toolbox and begins its address, which continues into the following block; read together the two give the address the record carries, and the numeral in the tool's name is the version the record records.",
          "source_locators": [
            "page:8:block:010",
            "page:8:block:011"
          ]
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block gives the package, its version in parentheses and its address.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same block gives the relocation program, its version in parentheses and its address.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same block names the location code and gives its address.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same block names the picking software and gives its address.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same block names the inversion program and gives its address.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same block names the catalog-analysis software and gives its address.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The block that formalises the relation also formalises both endpoints, and it places the ridge inside the equatorial Atlantic in so many words.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation's block formalises the faults endpoint and says the complex's surface is heavily cut by them; the complex itself is introduced in earlier blocks.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation's block formalises both endpoints and puts the core complex on the ridge's outside corner.",
          "source_locators": [
            "page:2:block:007"
          ]
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation's block formalises both endpoints and says the intersection segment, which the same block names as this record, is bounded by the detachment fault.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation's block formalises both endpoints and puts this segment immediately south of the first discontinuity.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation's block formalises both endpoints and calls the southern segment the adjacent one.",
          "source_locators": [
            "page:8:block:005"
          ]
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation's block formalises both endpoints and names the southern segment as the ridge lying south of the second discontinuity.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation's block formalises the vent-field endpoint and puts the field on the eastern flank of the discontinuity; the discontinuity is introduced in earlier blocks.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence gives the authors' causal reading, that the deep mantle earthquakes follow from degassing of the volatile, and names the volatile the subject resolves to; a later block the record also reaches marks it as the preferred of four possibilities.",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002"
          ]
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence says the sea floor basalts are mostly degassed, and the surrounding block ties those samples to the two segments the record's name mentions.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence spells out the assumption the trace-element estimate rests on and names the volatile the subject resolves to.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence gives the eastward relocation of the ridge axis and describes it entirely by reference to the core complex the subject resolves to.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence offers a cold, thick lithosphere as the explanation, and the rest of the block withdraws it, which is the disposition the record carries.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence argues that the unexpected depths beneath the ridge axis are not a location artifact, and names the ridge the subject resolves to.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence infers the detachment fault is inactive from the absence of deep seismicity beneath the valley floor.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence places most of the events in the mantle below ten kilometres, which is what the record's name asserts.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence puts hydrothermal cooling of the lithosphere forward as a hypothesis and the rest of the block sets it aside, matching the recorded disposition.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence offers the magmatic-tectonic association as the third possibility; a later block the record also reaches withdraws it, matching the recorded disposition.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence concludes that magmatism dominates crustal accretion at the segment the subject resolves to.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence attributes melt at the boundary to a combination of the two volatiles, and the boundary is the subject the record resolves to.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence infers from the observed depths that ascending melt resides in the mantle at those depths.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence raises localized high strain in mylonite shear zones as a hypothesis and the block then rules it out for this segment, matching the recorded disposition.",
          "source_locators": [
            "page:3:block:003"
          ]
        },
        {
          "row_index": 87,
          "source_support": "PARTIAL",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence supports the claim itself, that the seismic record is a brief snapshot in time, and it does name the ridge; but what the claim is predicated of is the temporal reach of the recorded dataset, not the ridge the subject reference resolves to, so the subject projection is only partly borne out.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located sentence gives the number of earthquakes located and confines it to the region around the intersection the subject resolves to.",
          "source_locators": [
            "page:2:block:003"
          ]
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "rationale": "SUBJECT_IN_BLOCK The relocation block states how many events ended up along the ridge; both the count and its scope come from that sentence, and the record carries no statement digest.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "rationale": "SUBJECT_IN_BLOCK The same relocation sentence gives the transform fault's event total and its scope; the record carries no statement digest.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The opening block gives the approximate mass fraction of carbon dioxide in the primary melts, with the unit, and says it comes from a synthesis of rock analyses rather than direct measurement.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the lower bound on barium in the segment's samples with its unit.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states the floor on primary melt carbon dioxide for the studied segment, with its unit, as the outcome of the calculation.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the proportion of the volatile lost when a gas phase nucleates.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same enrichment sentence gives the rubidium floor and its unit.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the approximate temperature at which melt is present for anhydrous peridotite at the boundary.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block puts the boundary at about ten kilometres beneath the southern discontinuity, read off the observed seismicity.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the depth the boundary would take under the cold-lithosphere explanation and marks that reading as hypothetical.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 99,
          "source_support": "PARTIAL",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the isotherm as a single figure with a stated tolerance. The row expands that tolerance into the interval and then carries the same tolerance again as a separate uncertainty, so the interval and the uncertainty are not both supported as independent facts.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block says the boundary stays shallower than ten kilometres off axis, with the unit.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block caps the brittle lithosphere at about ten kilometres at the segment boundaries.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the average carbon dioxide concentration reported for the region's segments with its unit and credits it to earlier work.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the primary melt carbon dioxide interval derived from the barium proxy for this segment, with its unit.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the barium-derived interval for the southern segment the subject resolves to.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the pre-eruptive interval estimated from barium for this segment.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the lower pre-eruptive interval estimated from barium for the southern segment.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The results block gives the calculated volatile content of the melts generated along this segment, with its unit.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the comparison figure for the southern segment.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the ceiling of the regional carbon dioxide concentrations with its unit.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the rubidium-derived primary melt interval for this segment.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the rubidium-derived interval for the southern segment.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the pre-eruptive interval estimated from rubidium for this segment.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the lower pre-eruptive interval estimated from rubidium for the southern segment.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block dates the crust of the western flank in the same clause that gives its thickness.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK That clause gives the thickness and its tolerance, and the schematic caption repeats the same figure for the segment.",
          "source_locators": [
            "page:2:block:006",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The schematic caption gives the depth interval below sea floor of the deep events beneath the ridge axis.",
          "source_locators": [
            "page:7:block:012"
          ]
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the depth interval over which continued degassing would produce earthquakes and marks it as expected rather than observed.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block placing the study gives the half-spreading rate with its unit.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block puts the mantle hosting these earthquakes above eleven hundred degrees.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The comparison sentence gives the depth floor for the Icelandic cases; the country's name is broken across a line by the text layer.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the isotherm interval the hypothetical boundary depth would correspond to.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the age of the cold lithosphere behind the edge effect.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the temperature interval at those depths and attributes it to thermal modelling, which is the determination the record carries.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The acquisition block gives the length of ridge axis the network covered.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the approximate length of the ridge segment between the two transform faults.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The comparison sentence gives the depth floor for the Mayotte case.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the width of the median valley, which is the other name the subject carries.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the melt fraction proposed at the base of the boundary.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 129,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the discontinuity's approximate length.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 130,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block says the events beneath the southern discontinuity reach about ten kilometres.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 131,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block caps the depth range observed beneath the southern discontinuity.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 132,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The key-observations block gives the normal-depth interval beneath the southern discontinuity.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 133,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the ridge offset at the discontinuity.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 134,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same capping sentence gives the shallower ceiling beneath the core complex.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 135,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the shallow focal depths of the cluster on the western side of the valley.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 136,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the depth the off-axis shallow seismicity west of the segment axis reaches.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 137,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the estimated pre-eruptive carbon dioxide interval for the segment with its unit.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 138,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the observed depth interval of the deep earthquakes beneath the segment's axis.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 139,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The key-observations block gives the approximate depth interval of the deep microseismicity beneath the segment's ridge axis.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 140,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the segment's approximate length.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 141,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the southern segment's length.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 142,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The acquisition block gives the length of the transform fault the network covered.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 143,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the highest melt carbon dioxide previously reported at that ridge.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 144,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same proposal gives the ceiling on water content at the base of the boundary.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 145,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block defining the global trends gives the carbon dioxide to barium ratio with its spread and names barium, which the subject reference resolves to.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 146,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the carbon dioxide to rubidium ratio with its spread and names rubidium.",
          "source_locators": [
            "page:5:block:004"
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
  "rationale": "DIGEST_OK SUBJECT_IN_BLOCK one or two sentences in your own words"
}
```
