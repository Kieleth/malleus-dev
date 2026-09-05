# Malleus paper v4 run-04 source-grounded review record

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

Fill one `rows` entry per returned row, in order, zero-based: 17 for CQ-01, 69
for CQ-02, 83 for CQ-03, 71 for CQ-04. Cite reading block ids only. Write the
reasons in your own words and copy no source passage into this record.

```json
{
  "schema": "malleus.paper-v4.source-grounded-review/v2",
  "status": "HUMAN_RATIFIED",
  "inputs": {
    "review_protocol_sha256": "sha256:7cee52a7d6ea5018fe8443e621c72280b05c2bb5cc1e4a2eeaa27208665ed379",
    "review_input_manifest_sha256": "sha256:3a263dcf18e83d3844d1b44774e44be08e4c8ac28fe6a50816e479c3c7edaf98"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-preliminary-run-04",
    "completed_at": "2026-09-05T01:29:34Z"
  },
  "questions": [
    {
      "question_id": "CQ-01",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "The first two rows answer the question directly: an ocean-bottom seismometer network of 19 instruments, fielded as part of the SMARTIES cruise, with the count and its scope carried on the network record. The acquisition and processing chain comes back as well, from triggered detections through location and relocation to the velocity-model test subset, each tied to the software that produced it. The remaining rows, the catalogue b value and magnitude of completeness and the RC2 depth range, are by-products of the type cross-product and bear on other questions, but nothing this question asks for is missing.",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002",
        "page:8:block:010"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ],
          "rationale": "Both the Results block and the Methods block state the deployment: 19 ocean-bottom seismometers forming one network, fielded on the SMARTIES cruise. That covers the network, its instrument count and its place in that campaign."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ],
          "rationale": "Both the Results block and the Methods block state the deployment: 19 ocean-bottom seismometers forming one network, fielded on the SMARTIES cruise. That covers the network, its instrument count and its place in that campaign. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002",
            "page:8:block:010"
          ],
          "rationale": "The Methods block says an automatic trigger inside the SEISAN package produced 760 events, which were then written into that package's database, and the code block gives SEISAN the phase-picking role. Count, detection stage and tool all hold."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005",
            "page:7:block:004",
            "page:8:block:010"
          ],
          "rationale": "The Results state 514 events located around the Romanche ridge-transform intersection and the Methods repeat that total; NonLinLoc is named as the program that produced the hypocentres. The row asserts no exclusivity, and the later replacement of part of that catalogue by relocations is carried on a separate record."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006",
            "page:7:block:007",
            "page:8:block:010"
          ],
          "rationale": "The Methods name hypoDD as the double-difference relocation program and report that 276 events came out well relocated and took the place of the earlier ones in the final catalogue; the code block gives version 1.3."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004",
            "page:8:block:010"
          ],
          "rationale": "The Methods describe a 360-earthquake sub-dataset selected on at least six arrivals and a station gap no wider than 180 degrees, built to run VELEST for a minimum 1-D velocity model, which matches the count, the selection criteria and the tool."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002",
            "page:8:block:010"
          ],
          "rationale": "The Methods block says an automatic trigger inside the SEISAN package produced 760 events, which were then written into that package's database, and the code block gives SEISAN the phase-picking role. Count, detection stage and tool all hold. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005",
            "page:7:block:004",
            "page:8:block:010"
          ],
          "rationale": "The Results state 514 events located around the Romanche ridge-transform intersection and the Methods repeat that total; NonLinLoc is named as the program that produced the hypocentres. The row asserts no exclusivity, and the later replacement of part of that catalogue by relocations is carried on a separate record. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006",
            "page:7:block:007",
            "page:8:block:010"
          ],
          "rationale": "The Methods name hypoDD as the double-difference relocation program and report that 276 events came out well relocated and took the place of the earlier ones in the final catalogue; the code block gives version 1.3. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004",
            "page:8:block:010"
          ],
          "rationale": "The Methods describe a 360-earthquake sub-dataset selected on at least six arrivals and a station gap no wider than 180 degrees, built to run VELEST for a minimum 1-D velocity model, which matches the count, the selection criteria and the tool. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ],
          "rationale": "Both the Results and the Methods put the spacing of the OBS network at about 30 km, against the same 19-instrument network; the only thing the record drops is the source's rounding marker on the value."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ],
          "rationale": "Both the Results and the Methods put the spacing of the OBS network at about 30 km, against the same 19-instrument network; the only thing the record drops is the source's rounding marker on the value. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ],
          "rationale": "The magnitude section states that the b value of 0.87 was calculated with the ZMAP software, and the code block confirms ZMAP's catalogue-statistics role."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ],
          "rationale": "The same magnitude section gives a magnitude of completeness of 1.5 calculated with ZMAP, which matches the value, the derived status and the tool the row names."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ],
          "rationale": "The magnitude section states that the b value of 0.87 was calculated with the ZMAP software, and the code block confirms ZMAP's catalogue-statistics role. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ],
          "rationale": "The same magnitude section gives a magnitude of completeness of 1.5 calculated with ZMAP, which matches the value, the derived status and the tool the row names. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:2:block:004"
          ],
          "rationale": "The Results put the deep events under the RC2 ridge axis at depths of 16 to 19 km, and a second Results block names that same deep population under the same axis, so the bounded depth in km and the population it concerns both hold. The relation's own locator lands on the general data-acquisition block, which carries neither, so I judged the pairing on the reading."
        }
      ]
    },
    {
      "question_id": "CQ-02",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "One row states that the deep microseismicity sits under segment RC2, and the record names place those events under that segment's ridge axis, so the named subsection and the position of the events relative to the axis are both answered. Two sibling rows separate the normal-depth events under NTD2 and the shallow events under the oceanic core complex, which keeps the deep population distinct rather than blurring the three. One limitation worth recording: the typed relation says only that the events lie beneath the segment; the ridge-axis detail sits in the record's name and count scope rather than in the relation.",
      "source_locators": [
        "page:2:block:004",
        "page:1:block:005",
        "page:3:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004",
            "page:3:block:002",
            "page:1:block:005"
          ],
          "rationale": "The key-observations block puts the deep microseismicity under the axis of segment RC2, which gives the population, the segment and the beneath relation; RC2's magmatic character comes from the discussion block concluding that magmatism dominates its crustal accretion."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004",
            "page:2:block:001"
          ],
          "rationale": "The same key-observations block places normal-depth events under the southern discontinuity NTD2, and the geological description gives NTD2 its N110\u00b0E orientation."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004",
            "page:1:block:005"
          ],
          "rationale": "The key-observations block places the shallow events at the intersection's outside corner, under the faulted dome of the core complex and off-axis to the west of segment RC1, and the study-area block introduces that complex."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:2:block:004"
          ],
          "rationale": "The Results put the deep events under the RC2 ridge axis at depths of 16 to 19 km, and a second Results block names that same deep population under the same axis, so the bounded depth in km and the population it concerns both hold. The relation's own locator lands on the general data-acquisition block, which carries neither, so I judged the pairing on the reading."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "The study-area block gives the MAR half-spreading rate here as 16 mm/yr and identifies the ridge itself, so the value, the unit and the feature all hold. The relation's locator points instead at the data-acquisition block, so the pairing is judged on the reading."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:002"
          ],
          "rationale": "The Results attribute 5.4 \u00b1 0.3 km of crust to the 8 Ma western flank of this ridge in the reasoning about the segment, matching value, uncertainty and unit, and the discussion supports calling RC2 magmatic."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:004"
          ],
          "rationale": "The discussion says microseismicity reaching 10 km under NTD2 shows the brittle-ductile boundary sits at about that depth there, and the introduction defines the boundary the observation concerns."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:004"
          ],
          "rationale": "The discussion presents the cold, thick lithosphere explanation under which the brittle-ductile boundary would sit near 20 km, which matches both the value and the hypothesised status the record carries."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "The introduction explains that on slow- and ultraslow-spreading ridges this boundary is set from the deepest earthquakes, taken to mark the 700 \u00b1 100 \u00b0C isotherms, which gives the value, the uncertainty, the unit and the feature."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001",
            "page:5:block:010"
          ],
          "rationale": "The discussion reports another study's proposal that roughly 1.1 % melt must sit where the lithosphere meets the asthenosphere, and the preceding block introduces that boundary. The relation itself derives from an unrelated data-acquisition block, so the pairing is judged on the reading."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "One block carries the whole row: the cold, thick lithosphere explanation, and the thermal-modelling figure of 1100 to 1200 \u00b0C at 10 to 20 km that the authors use to conclude the mantle under the RC2 axis is hot, which is exactly the challenge the row records."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "The same block reports shallow off-axis events west of the RC2 axis showing the boundary stays above 10 km, and uses that against the cold lithosphere explanation. The record keeps the figure as an upper bound with no lower value, as the source does."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006",
            "page:5:block:002"
          ],
          "rationale": "The solubility calculation puts saturation and the onset of degassing near 25 km for a melt above 0.7 wt% CO2, and says that agrees with the deep microseismicity observed, which is the supporting link the row records; the preferred hypothesis itself is stated in the earlier block."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "One block carries the whole row: the cold, thick lithosphere explanation, and the thermal-modelling figure of 1100 to 1200 \u00b0C at 10 to 20 km that the authors use to conclude the mantle under the RC2 axis is hot, which is exactly the challenge the row records. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "The same block reports shallow off-axis events west of the RC2 axis showing the boundary stays above 10 km, and uses that against the cold lithosphere explanation. The record keeps the figure as an upper bound with no lower value, as the source does. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006",
            "page:5:block:002"
          ],
          "rationale": "The solubility calculation puts saturation and the onset of degassing near 25 km for a melt above 0.7 wt% CO2, and says that agrees with the deep microseismicity observed, which is the supporting link the row records; the preferred hypothesis itself is stated in the earlier block. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:2:block:004"
          ],
          "rationale": "The Results put the deep events under the RC2 ridge axis at depths of 16 to 19 km, and a second Results block names that same deep population under the same axis, so the bounded depth in km and the population it concerns both hold. The relation's own locator lands on the general data-acquisition block, which carries neither, so I judged the pairing on the reading."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "The study-area block gives the MAR half-spreading rate here as 16 mm/yr and identifies the ridge itself, so the value, the unit and the feature all hold. The relation's locator points instead at the data-acquisition block, so the pairing is judged on the reading."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:002"
          ],
          "rationale": "The Results attribute 5.4 \u00b1 0.3 km of crust to the 8 Ma western flank of this ridge in the reasoning about the segment, matching value, uncertainty and unit, and the discussion supports calling RC2 magmatic."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:004"
          ],
          "rationale": "The discussion says microseismicity reaching 10 km under NTD2 shows the brittle-ductile boundary sits at about that depth there, and the introduction defines the boundary the observation concerns."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:004"
          ],
          "rationale": "The discussion presents the cold, thick lithosphere explanation under which the brittle-ductile boundary would sit near 20 km, which matches both the value and the hypothesised status the record carries."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "The introduction explains that on slow- and ultraslow-spreading ridges this boundary is set from the deepest earthquakes, taken to mark the 700 \u00b1 100 \u00b0C isotherms, which gives the value, the uncertainty, the unit and the feature."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001",
            "page:5:block:010"
          ],
          "rationale": "The discussion reports another study's proposal that roughly 1.1 % melt must sit where the lithosphere meets the asthenosphere, and the preceding block introduces that boundary. The relation itself derives from an unrelated data-acquisition block, so the pairing is judged on the reading."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "One block carries the whole row: the cold, thick lithosphere explanation, and the thermal-modelling figure of 1100 to 1200 \u00b0C at 10 to 20 km that the authors use to conclude the mantle under the RC2 axis is hot, which is exactly the challenge the row records."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "The same block reports shallow off-axis events west of the RC2 axis showing the boundary stays above 10 km, and uses that against the cold lithosphere explanation. The record keeps the figure as an upper bound with no lower value, as the source does."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:5:block:005",
            "page:5:block:002"
          ],
          "rationale": "The Methods put the RC2 primary-melt CO2 at 0.4 to 3.0 wt% from the Ba90 proxy, the Results tie that volatile enrichment to the segment where the deep mantle earthquakes were found, and the preferred hypothesis names CO2 escaping from melt on its way up."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006",
            "page:5:block:002"
          ],
          "rationale": "The solubility calculation puts saturation and the onset of degassing near 25 km for a melt above 0.7 wt% CO2, and says that agrees with the deep microseismicity observed, which is the supporting link the row records; the preferred hypothesis itself is stated in the earlier block."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "One block carries the whole row: the cold, thick lithosphere explanation, and the thermal-modelling figure of 1100 to 1200 \u00b0C at 10 to 20 km that the authors use to conclude the mantle under the RC2 axis is hot, which is exactly the challenge the row records. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "The same block reports shallow off-axis events west of the RC2 axis showing the boundary stays above 10 km, and uses that against the cold lithosphere explanation. The record keeps the figure as an upper bound with no lower value, as the source does. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:5:block:005",
            "page:5:block:002"
          ],
          "rationale": "The Methods put the RC2 primary-melt CO2 at 0.4 to 3.0 wt% from the Ba90 proxy, the Results tie that volatile enrichment to the segment where the deep mantle earthquakes were found, and the preferred hypothesis names CO2 escaping from melt on its way up. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006",
            "page:5:block:002"
          ],
          "rationale": "The solubility calculation puts saturation and the onset of degassing near 25 km for a melt above 0.7 wt% CO2, and says that agrees with the deep microseismicity observed, which is the supporting link the row records; the preferred hypothesis itself is stated in the earlier block. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "The study-area block places the work where the Romanche transform meets the ridge on its eastern side, which is the intersection the row records."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:3:block:002"
          ],
          "rationale": "The geological description gives segment RC2 a median valley and a neo-volcanic ridge striking N154\u00b0E, so the feature, its strike and its position inside RC2 all hold."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "The study area says two non-transform discontinuities break the studied ridge portion, and the following block gives NTD1 its N76\u00b0E orientation and its magmatic and tectonic origin."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "The same pair of blocks gives the two discontinuities that break this ridge portion, with NTD2 offsetting it on a N110\u00b0E trend."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "The block describes NTD2 as affected over large areas by normal faults striking N115\u00b0E and N145\u00b0E, which gives both the fault set and its containment."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "The study-area block puts a prominent oceanic core complex at the RTI segment east of the ridge axis, and the figure caption places it at the ridge's outside corner, so the complex and its position within the intersection hold."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:1:block:005"
          ],
          "rationale": "The description says normal faults striking about N20\u00b0E and N20\u00b0W cut the surface of the core complex heavily, which matches the strike and the containment."
        },
        {
          "row_index": 38,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "The study area states outright that a detachment fault dipping westward bounds the RTI segment on its eastern side, but the source only says the lack of deep microseismicity near the complex's termination suggests that fault is now inactive. The row carries the inactive status flat, without that hedge."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:005",
            "page:2:block:001",
            "page:3:block:002"
          ],
          "rationale": "The Methods treat RC3 as the segment next to the studied RC2 on its southern side, and the geological description gives RC3 its magmatic character and its ~N165\u00b0E orientation."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "The study area identifies RC3 as the segment lying south of NTD2 on this stretch of the MAR, and the next block gives its magmatic character and orientation."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "The study-area block splits the studied ridge portion into four subsections, the first being the RTI segment named RC1, which is the containment the row records."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "The same subdivision lists NTD1 among the four subsections of the studied ridge, and the following block gives its orientation and its mixed origin."
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:002"
          ],
          "rationale": "RC2 is listed among the four subsections of the studied MAR portion, and the discussion supports its magmatic character."
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "NTD2 is the fourth of the listed subsections of the studied ridge, and its N110\u00b0E orientation is given in the following block."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:3:block:002"
          ],
          "rationale": "The description gives segment RC2 a median valley about 10 km across, which is the axial valley and the containment the row records."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002",
            "page:2:block:001"
          ],
          "rationale": "The discussion reports an extinct vent field observed on NTD1's eastern flank, which carries the field, its inactive state and its location in one sentence."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:2:block:004"
          ],
          "rationale": "The discussion offers the cold, thick lithosphere as one explanation for the deep earthquakes and then argues against it in the same block, which supports both the hypothesis framing and the not-supported disposition; the population concerned is the deep microseismicity under the RC2 axis named in the Results."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002",
            "page:2:block:004"
          ],
          "rationale": "The block states the hydrothermal-cooling hypothesis for the large earthquake depths and then closes it off, noting no active venting on the RC2 axis and an extinct field too far away to matter, so the hypothesis framing and its rejection both hold for the deep RC2 population."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003",
            "page:4:block:001",
            "page:2:block:004"
          ],
          "rationale": "The discussion raises localized high strain in semi-brittle mylonite shear zones as another hypothesis and says in the same sentence that the observations do not support it, the reason running into the next block; the population is the deep RC2 microseismicity."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002",
            "page:4:block:003",
            "page:5:block:001",
            "page:2:block:004"
          ],
          "rationale": "The block the locator reaches only presents the magmatic-tectonic possibility. The rejection that the record's not-supported disposition asserts sits in the two following blocks, which the derivation does not reach and which say the Iceland and Mayotte settings differ and that melt movement does not apply here. Judged on the reading, the hypothesis and its disposition both hold."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:002",
            "page:2:block:004"
          ],
          "rationale": "One sentence names the fourth possibility as the authors' preferred one: the deep microseismicity under segment RC2 tied to CO2 escaping from melt as it ascends. That matches the record's name, its hypothesised modality and its preferred disposition."
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "A single block carries both records and the link between them: the hydrothermal-cooling hypothesis, the negative finding that no active venting is seen on the RC2 axis, and the use of that finding to set the hypothesis aside."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003",
            "page:4:block:002",
            "page:5:block:001"
          ],
          "rationale": "The negative finding that the axial valley shows no sign of an eruption under way, and its use against the magmatic-tectonic possibility, are both stated where the locator lands. Where the row also carries the target's not-supported disposition, that rests on the following block, which the derivation does not reach and which concludes melt movement does not apply here."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001",
            "page:3:block:003"
          ],
          "rationale": "The block states that inward-dipping high-angle faults bound the RC2 axial valley and that nothing there points to detachment faulting, and the preceding block says explicitly that this is why the mylonite shear-zone hypothesis is not supported."
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "A single block carries both records and the link between them: the hydrothermal-cooling hypothesis, the negative finding that no active venting is seen on the RC2 axis, and the use of that finding to set the hypothesis aside. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003",
            "page:4:block:002",
            "page:5:block:001"
          ],
          "rationale": "The negative finding that the axial valley shows no sign of an eruption under way, and its use against the magmatic-tectonic possibility, are both stated where the locator lands. Where the row also carries the target's not-supported disposition, that rests on the following block, which the derivation does not reach and which concludes melt movement does not apply here. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001",
            "page:3:block:003"
          ],
          "rationale": "The block states that inward-dipping high-angle faults bound the RC2 axial valley and that nothing there points to detachment faulting, and the preceding block says explicitly that this is why the mylonite shear-zone hypothesis is not supported. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:2:block:004"
          ],
          "rationale": "The discussion offers the cold, thick lithosphere as one explanation for the deep earthquakes and then argues against it in the same block, which supports both the hypothesis framing and the not-supported disposition; the population concerned is the deep microseismicity under the RC2 axis named in the Results. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002",
            "page:2:block:004"
          ],
          "rationale": "The block states the hydrothermal-cooling hypothesis for the large earthquake depths and then closes it off, noting no active venting on the RC2 axis and an extinct field too far away to matter, so the hypothesis framing and its rejection both hold for the deep RC2 population. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003",
            "page:4:block:001",
            "page:2:block:004"
          ],
          "rationale": "The discussion raises localized high strain in semi-brittle mylonite shear zones as another hypothesis and says in the same sentence that the observations do not support it, the reason running into the next block; the population is the deep RC2 microseismicity. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002",
            "page:4:block:003",
            "page:5:block:001",
            "page:2:block:004"
          ],
          "rationale": "The block the locator reaches only presents the magmatic-tectonic possibility. The rejection that the record's not-supported disposition asserts sits in the two following blocks, which the derivation does not reach and which say the Iceland and Mayotte settings differ and that melt movement does not apply here. Judged on the reading, the hypothesis and its disposition both hold. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:002",
            "page:2:block:004"
          ],
          "rationale": "One sentence names the fourth possibility as the authors' preferred one: the deep microseismicity under segment RC2 tied to CO2 escaping from melt as it ascends. That matches the record's name, its hypothesised modality and its preferred disposition. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "A single block carries both records and the link between them: the hydrothermal-cooling hypothesis, the negative finding that no active venting is seen on the RC2 axis, and the use of that finding to set the hypothesis aside."
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003",
            "page:4:block:002",
            "page:5:block:001"
          ],
          "rationale": "The negative finding that the axial valley shows no sign of an eruption under way, and its use against the magmatic-tectonic possibility, are both stated where the locator lands. Where the row also carries the target's not-supported disposition, that rests on the following block, which the derivation does not reach and which concludes melt movement does not apply here."
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001",
            "page:3:block:003"
          ],
          "rationale": "The block states that inward-dipping high-angle faults bound the RC2 axial valley and that nothing there points to detachment faulting, and the preceding block says explicitly that this is why the mylonite shear-zone hypothesis is not supported."
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "A single block carries both records and the link between them: the hydrothermal-cooling hypothesis, the negative finding that no active venting is seen on the RC2 axis, and the use of that finding to set the hypothesis aside. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003",
            "page:4:block:002",
            "page:5:block:001"
          ],
          "rationale": "The negative finding that the axial valley shows no sign of an eruption under way, and its use against the magmatic-tectonic possibility, are both stated where the locator lands. Where the row also carries the target's not-supported disposition, that rests on the following block, which the derivation does not reach and which concludes melt movement does not apply here. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001",
            "page:3:block:003"
          ],
          "rationale": "The block states that inward-dipping high-angle faults bound the RC2 axial valley and that nothing there points to detachment faulting, and the preceding block says explicitly that this is why the mylonite shear-zone hypothesis is not supported. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        }
      ]
    },
    {
      "question_id": "CQ-03",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "Both quantities come back as bounded values with units and estimate status: the earthquake depth of 16 to 19 km in km, recorded as measured, and the CO2 concentration calculated for the primary melt of segment RC2 from both proxies, in wt%, recorded as calculated and derived. The subject of each is identifiable from the record name, and the neighbouring RC3 values are separately named so the two segments do not blur. The wider 10 to 20 km depth band the source also reports for the deep events appears only as text inside the population's name and count scope, not as a second bounded quantity.",
      "source_locators": [
        "page:2:block:006",
        "page:8:block:007",
        "page:2:block:004"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "The study-area block gives the MAR half-spreading rate here as 16 mm/yr and identifies the ridge itself, so the value, the unit and the feature all hold. The relation's locator points instead at the data-acquisition block, so the pairing is judged on the reading."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:002"
          ],
          "rationale": "The Results attribute 5.4 \u00b1 0.3 km of crust to the 8 Ma western flank of this ridge in the reasoning about the segment, matching value, uncertainty and unit, and the discussion supports calling RC2 magmatic."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:2:block:004"
          ],
          "rationale": "The Results put the deep events under the RC2 ridge axis at depths of 16 to 19 km, and a second Results block names that same deep population under the same axis, so the bounded depth in km and the population it concerns both hold. The relation's own locator lands on the general data-acquisition block, which carries neither, so I judged the pairing on the reading."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ],
          "rationale": "The magnitude section states that the b value of 0.87 was calculated with the ZMAP software, and the code block confirms ZMAP's catalogue-statistics role."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ],
          "rationale": "The same magnitude section gives a magnitude of completeness of 1.5 calculated with ZMAP, which matches the value, the derived status and the tool the row names."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "One block carries the whole row: the cold, thick lithosphere explanation, and the thermal-modelling figure of 1100 to 1200 \u00b0C at 10 to 20 km that the authors use to conclude the mantle under the RC2 axis is hot, which is exactly the challenge the row records."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "The same block reports shallow off-axis events west of the RC2 axis showing the boundary stays above 10 km, and uses that against the cold lithosphere explanation. The record keeps the figure as an upper bound with no lower value, as the source does."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006",
            "page:5:block:002"
          ],
          "rationale": "The solubility calculation puts saturation and the onset of degassing near 25 km for a melt above 0.7 wt% CO2, and says that agrees with the deep microseismicity observed, which is the supporting link the row records; the preferred hypothesis itself is stated in the earlier block."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "One block carries the whole row: the cold, thick lithosphere explanation, and the thermal-modelling figure of 1100 to 1200 \u00b0C at 10 to 20 km that the authors use to conclude the mantle under the RC2 axis is hot, which is exactly the challenge the row records. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "The same block reports shallow off-axis events west of the RC2 axis showing the boundary stays above 10 km, and uses that against the cold lithosphere explanation. The record keeps the figure as an upper bound with no lower value, as the source does. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006",
            "page:5:block:002"
          ],
          "rationale": "The solubility calculation puts saturation and the onset of degassing near 25 km for a melt above 0.7 wt% CO2, and says that agrees with the deep microseismicity observed, which is the supporting link the row records; the preferred hypothesis itself is stated in the earlier block. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:8:block:005"
          ],
          "rationale": "The Methods put the RC2 primary-melt CO2 at 0.4 to 3.0 wt% using the Ba90 proxy and describe the MORB samples compiled for that segment, so the bounded value, the unit, the calculated status and the sample it concerns all hold."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:8:block:005"
          ],
          "rationale": "The same Methods sentence gives 0.5 to 2.8 wt% from the Rb90 proxy for RC2 against that same compiled sample set, matching value, unit and subject."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:8:block:005"
          ],
          "rationale": "The Methods give 0.04 to 0.5 wt% from the Ba90 proxy for RC3 and describe the sample compilation for that segment, which covers the value, the unit and the subject."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:8:block:005"
          ],
          "rationale": "The same sentence gives 0.05 to 0.7 wt% from the Rb90 proxy for RC3 against the RC3 sample set."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:5:block:005",
            "page:5:block:002"
          ],
          "rationale": "The Methods put the RC2 primary-melt CO2 at 0.4 to 3.0 wt% from the Ba90 proxy, the Results tie that volatile enrichment to the segment where the deep mantle earthquakes were found, and the preferred hypothesis names CO2 escaping from melt on its way up."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:5:block:005",
            "page:5:block:002"
          ],
          "rationale": "The Methods put the RC2 primary-melt CO2 at 0.4 to 3.0 wt% from the Ba90 proxy, the Results tie that volatile enrichment to the segment where the deep mantle earthquakes were found, and the preferred hypothesis names CO2 escaping from melt on its way up. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "The study-area block gives the MAR half-spreading rate here as 16 mm/yr and identifies the ridge itself, so the value, the unit and the feature all hold. The relation's locator points instead at the data-acquisition block, so the pairing is judged on the reading."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:002"
          ],
          "rationale": "The Results attribute 5.4 \u00b1 0.3 km of crust to the 8 Ma western flank of this ridge in the reasoning about the segment, matching value, uncertainty and unit, and the discussion supports calling RC2 magmatic."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:2:block:004"
          ],
          "rationale": "The Results put the deep events under the RC2 ridge axis at depths of 16 to 19 km, and a second Results block names that same deep population under the same axis, so the bounded depth in km and the population it concerns both hold. The relation's own locator lands on the general data-acquisition block, which carries neither, so I judged the pairing on the reading."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:8:block:005"
          ],
          "rationale": "The Methods put the RC2 primary-melt CO2 at 0.4 to 3.0 wt% using the Ba90 proxy and describe the MORB samples compiled for that segment, so the bounded value, the unit, the calculated status and the sample it concerns all hold. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:8:block:005"
          ],
          "rationale": "The same Methods sentence gives 0.5 to 2.8 wt% from the Rb90 proxy for RC2 against that same compiled sample set, matching value, unit and subject. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:8:block:005"
          ],
          "rationale": "The Methods give 0.04 to 0.5 wt% from the Ba90 proxy for RC3 and describe the sample compilation for that segment, which covers the value, the unit and the subject. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:8:block:005"
          ],
          "rationale": "The same sentence gives 0.05 to 0.7 wt% from the Rb90 proxy for RC3 against the RC3 sample set. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ],
          "rationale": "The magnitude section states that the b value of 0.87 was calculated with the ZMAP software, and the code block confirms ZMAP's catalogue-statistics role."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ],
          "rationale": "The same magnitude section gives a magnitude of completeness of 1.5 calculated with ZMAP, which matches the value, the derived status and the tool the row names."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "One block carries the whole row: the cold, thick lithosphere explanation, and the thermal-modelling figure of 1100 to 1200 \u00b0C at 10 to 20 km that the authors use to conclude the mantle under the RC2 axis is hot, which is exactly the challenge the row records."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "The same block reports shallow off-axis events west of the RC2 axis showing the boundary stays above 10 km, and uses that against the cold lithosphere explanation. The record keeps the figure as an upper bound with no lower value, as the source does."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:5:block:005",
            "page:5:block:002"
          ],
          "rationale": "The Methods put the RC2 primary-melt CO2 at 0.4 to 3.0 wt% from the Ba90 proxy, the Results tie that volatile enrichment to the segment where the deep mantle earthquakes were found, and the preferred hypothesis names CO2 escaping from melt on its way up. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006",
            "page:5:block:002"
          ],
          "rationale": "The solubility calculation puts saturation and the onset of degassing near 25 km for a melt above 0.7 wt% CO2, and says that agrees with the deep microseismicity observed, which is the supporting link the row records; the preferred hypothesis itself is stated in the earlier block."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "One block carries the whole row: the cold, thick lithosphere explanation, and the thermal-modelling figure of 1100 to 1200 \u00b0C at 10 to 20 km that the authors use to conclude the mantle under the RC2 axis is hot, which is exactly the challenge the row records. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "The same block reports shallow off-axis events west of the RC2 axis showing the boundary stays above 10 km, and uses that against the cold lithosphere explanation. The record keeps the figure as an upper bound with no lower value, as the source does. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:5:block:005",
            "page:5:block:002"
          ],
          "rationale": "The Methods put the RC2 primary-melt CO2 at 0.4 to 3.0 wt% from the Ba90 proxy, the Results tie that volatile enrichment to the segment where the deep mantle earthquakes were found, and the preferred hypothesis names CO2 escaping from melt on its way up. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006",
            "page:5:block:002"
          ],
          "rationale": "The solubility calculation puts saturation and the onset of degassing near 25 km for a melt above 0.7 wt% CO2, and says that agrees with the deep microseismicity observed, which is the supporting link the row records; the preferred hypothesis itself is stated in the earlier block. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "The study-area block places the work where the Romanche transform meets the ridge on its eastern side, which is the intersection the row records."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:3:block:002"
          ],
          "rationale": "The geological description gives segment RC2 a median valley and a neo-volcanic ridge striking N154\u00b0E, so the feature, its strike and its position inside RC2 all hold."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "The study area says two non-transform discontinuities break the studied ridge portion, and the following block gives NTD1 its N76\u00b0E orientation and its magmatic and tectonic origin."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "The same pair of blocks gives the two discontinuities that break this ridge portion, with NTD2 offsetting it on a N110\u00b0E trend."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "The block describes NTD2 as affected over large areas by normal faults striking N115\u00b0E and N145\u00b0E, which gives both the fault set and its containment."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "The study-area block puts a prominent oceanic core complex at the RTI segment east of the ridge axis, and the figure caption places it at the ridge's outside corner, so the complex and its position within the intersection hold."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:1:block:005"
          ],
          "rationale": "The description says normal faults striking about N20\u00b0E and N20\u00b0W cut the surface of the core complex heavily, which matches the strike and the containment."
        },
        {
          "row_index": 41,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "The study area states outright that a detachment fault dipping westward bounds the RTI segment on its eastern side, but the source only says the lack of deep microseismicity near the complex's termination suggests that fault is now inactive. The row carries the inactive status flat, without that hedge."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:005",
            "page:2:block:001",
            "page:3:block:002"
          ],
          "rationale": "The Methods treat RC3 as the segment next to the studied RC2 on its southern side, and the geological description gives RC3 its magmatic character and its ~N165\u00b0E orientation."
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "The study area identifies RC3 as the segment lying south of NTD2 on this stretch of the MAR, and the next block gives its magmatic character and orientation."
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "The study-area block splits the studied ridge portion into four subsections, the first being the RTI segment named RC1, which is the containment the row records."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "The same subdivision lists NTD1 among the four subsections of the studied ridge, and the following block gives its orientation and its mixed origin."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:002"
          ],
          "rationale": "RC2 is listed among the four subsections of the studied MAR portion, and the discussion supports its magmatic character."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "NTD2 is the fourth of the listed subsections of the studied ridge, and its N110\u00b0E orientation is given in the following block."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:3:block:002"
          ],
          "rationale": "The description gives segment RC2 a median valley about 10 km across, which is the axial valley and the containment the row records."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002",
            "page:2:block:001"
          ],
          "rationale": "The discussion reports an extinct vent field observed on NTD1's eastern flank, which carries the field, its inactive state and its location in one sentence."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004",
            "page:3:block:002",
            "page:1:block:005"
          ],
          "rationale": "The key-observations block puts the deep microseismicity under the axis of segment RC2, which gives the population, the segment and the beneath relation; RC2's magmatic character comes from the discussion block concluding that magmatism dominates its crustal accretion."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004",
            "page:2:block:001"
          ],
          "rationale": "The same key-observations block places normal-depth events under the southern discontinuity NTD2, and the geological description gives NTD2 its N110\u00b0E orientation."
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004",
            "page:1:block:005"
          ],
          "rationale": "The key-observations block places the shallow events at the intersection's outside corner, under the faulted dome of the core complex and off-axis to the west of segment RC1, and the study-area block introduces that complex."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002",
            "page:8:block:010"
          ],
          "rationale": "The Methods block says an automatic trigger inside the SEISAN package produced 760 events, which were then written into that package's database, and the code block gives SEISAN the phase-picking role. Count, detection stage and tool all hold."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005",
            "page:7:block:004",
            "page:8:block:010"
          ],
          "rationale": "The Results state 514 events located around the Romanche ridge-transform intersection and the Methods repeat that total; NonLinLoc is named as the program that produced the hypocentres. The row asserts no exclusivity, and the later replacement of part of that catalogue by relocations is carried on a separate record."
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006",
            "page:7:block:007",
            "page:8:block:010"
          ],
          "rationale": "The Methods name hypoDD as the double-difference relocation program and report that 276 events came out well relocated and took the place of the earlier ones in the final catalogue; the code block gives version 1.3."
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004",
            "page:8:block:010"
          ],
          "rationale": "The Methods describe a 360-earthquake sub-dataset selected on at least six arrivals and a station gap no wider than 180 degrees, built to run VELEST for a minimum 1-D velocity model, which matches the count, the selection criteria and the tool."
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:3:block:002"
          ],
          "rationale": "The geological description of RC2 cites basalts seen widely on the seafloor as support for a magmatically robust segment, which covers the sample, its material and the segment it came from."
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "The same block reports pillow basalts together with peridotites at NTD1's seafloor as the basis for its mixed origin, which gives the sample, its material and its provenance."
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:005",
            "page:6:block:005",
            "page:3:block:002"
          ],
          "rationale": "The Methods say the MORB samples were pulled from PetDB inside the OBS network footprint and analysed for RC2, and the figure caption identifies the compiled material as whole-rock MORB."
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:005",
            "page:6:block:005",
            "page:2:block:001"
          ],
          "rationale": "The same Methods sentence covers RC3 to the south, the figure caption identifies the material, and the geological description gives RC3 its magmatic character and orientation."
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:2:block:004"
          ],
          "rationale": "The discussion offers the cold, thick lithosphere as one explanation for the deep earthquakes and then argues against it in the same block, which supports both the hypothesis framing and the not-supported disposition; the population concerned is the deep microseismicity under the RC2 axis named in the Results."
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002",
            "page:2:block:004"
          ],
          "rationale": "The block states the hydrothermal-cooling hypothesis for the large earthquake depths and then closes it off, noting no active venting on the RC2 axis and an extinct field too far away to matter, so the hypothesis framing and its rejection both hold for the deep RC2 population."
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003",
            "page:4:block:001",
            "page:2:block:004"
          ],
          "rationale": "The discussion raises localized high strain in semi-brittle mylonite shear zones as another hypothesis and says in the same sentence that the observations do not support it, the reason running into the next block; the population is the deep RC2 microseismicity."
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002",
            "page:4:block:003",
            "page:5:block:001",
            "page:2:block:004"
          ],
          "rationale": "The block the locator reaches only presents the magmatic-tectonic possibility. The rejection that the record's not-supported disposition asserts sits in the two following blocks, which the derivation does not reach and which say the Iceland and Mayotte settings differ and that melt movement does not apply here. Judged on the reading, the hypothesis and its disposition both hold."
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:002",
            "page:2:block:004"
          ],
          "rationale": "One sentence names the fourth possibility as the authors' preferred one: the deep microseismicity under segment RC2 tied to CO2 escaping from melt as it ascends. That matches the record's name, its hypothesised modality and its preferred disposition."
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "A single block carries both records and the link between them: the hydrothermal-cooling hypothesis, the negative finding that no active venting is seen on the RC2 axis, and the use of that finding to set the hypothesis aside."
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003",
            "page:4:block:002",
            "page:5:block:001"
          ],
          "rationale": "The negative finding that the axial valley shows no sign of an eruption under way, and its use against the magmatic-tectonic possibility, are both stated where the locator lands. Where the row also carries the target's not-supported disposition, that rests on the following block, which the derivation does not reach and which concludes melt movement does not apply here."
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001",
            "page:3:block:003"
          ],
          "rationale": "The block states that inward-dipping high-angle faults bound the RC2 axial valley and that nothing there points to detachment faulting, and the preceding block says explicitly that this is why the mylonite shear-zone hypothesis is not supported."
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "A single block carries both records and the link between them: the hydrothermal-cooling hypothesis, the negative finding that no active venting is seen on the RC2 axis, and the use of that finding to set the hypothesis aside. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003",
            "page:4:block:002",
            "page:5:block:001"
          ],
          "rationale": "The negative finding that the axial valley shows no sign of an eruption under way, and its use against the magmatic-tectonic possibility, are both stated where the locator lands. Where the row also carries the target's not-supported disposition, that rests on the following block, which the derivation does not reach and which concludes melt movement does not apply here. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001",
            "page:3:block:003"
          ],
          "rationale": "The block states that inward-dipping high-angle faults bound the RC2 axial valley and that nothing there points to detachment faulting, and the preceding block says explicitly that this is why the mylonite shear-zone hypothesis is not supported. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:2:block:004"
          ],
          "rationale": "The discussion offers the cold, thick lithosphere as one explanation for the deep earthquakes and then argues against it in the same block, which supports both the hypothesis framing and the not-supported disposition; the population concerned is the deep microseismicity under the RC2 axis named in the Results. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002",
            "page:2:block:004"
          ],
          "rationale": "The block states the hydrothermal-cooling hypothesis for the large earthquake depths and then closes it off, noting no active venting on the RC2 axis and an extinct field too far away to matter, so the hypothesis framing and its rejection both hold for the deep RC2 population. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003",
            "page:4:block:001",
            "page:2:block:004"
          ],
          "rationale": "The discussion raises localized high strain in semi-brittle mylonite shear zones as another hypothesis and says in the same sentence that the observations do not support it, the reason running into the next block; the population is the deep RC2 microseismicity. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002",
            "page:4:block:003",
            "page:5:block:001",
            "page:2:block:004"
          ],
          "rationale": "The block the locator reaches only presents the magmatic-tectonic possibility. The rejection that the record's not-supported disposition asserts sits in the two following blocks, which the derivation does not reach and which say the Iceland and Mayotte settings differ and that melt movement does not apply here. Judged on the reading, the hypothesis and its disposition both hold. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:002",
            "page:2:block:004"
          ],
          "rationale": "One sentence names the fourth possibility as the authors' preferred one: the deep microseismicity under segment RC2 tied to CO2 escaping from melt as it ascends. That matches the record's name, its hypothesised modality and its preferred disposition. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "A single block carries both records and the link between them: the hydrothermal-cooling hypothesis, the negative finding that no active venting is seen on the RC2 axis, and the use of that finding to set the hypothesis aside."
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003",
            "page:4:block:002",
            "page:5:block:001"
          ],
          "rationale": "The negative finding that the axial valley shows no sign of an eruption under way, and its use against the magmatic-tectonic possibility, are both stated where the locator lands. Where the row also carries the target's not-supported disposition, that rests on the following block, which the derivation does not reach and which concludes melt movement does not apply here."
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001",
            "page:3:block:003"
          ],
          "rationale": "The block states that inward-dipping high-angle faults bound the RC2 axial valley and that nothing there points to detachment faulting, and the preceding block says explicitly that this is why the mylonite shear-zone hypothesis is not supported."
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "A single block carries both records and the link between them: the hydrothermal-cooling hypothesis, the negative finding that no active venting is seen on the RC2 axis, and the use of that finding to set the hypothesis aside. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003",
            "page:4:block:002",
            "page:5:block:001"
          ],
          "rationale": "The negative finding that the axial valley shows no sign of an eruption under way, and its use against the magmatic-tectonic possibility, are both stated where the locator lands. Where the row also carries the target's not-supported disposition, that rests on the following block, which the derivation does not reach and which concludes melt movement does not apply here. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001",
            "page:3:block:003"
          ],
          "rationale": "The block states that inward-dipping high-angle faults bound the RC2 axial valley and that nothing there points to detachment faulting, and the preceding block says explicitly that this is why the mylonite shear-zone hypothesis is not supported. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        }
      ]
    },
    {
      "question_id": "CQ-04",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The preferred mechanism comes back explicitly and with its epistemic status: CO2 escaping from melt on its way up, typed as a mechanism hypothesis, modality hypothesised, disposition preferred, and related to the deep microseismicity under segment RC2. The four rejected alternatives are returned alongside it carrying a not-supported disposition, so the preference reads as a choice among candidates rather than a bare assertion. What is missing is the interior of the mechanism. No returned row carries the volume change that degassing produces, the small pressure increase, or the extensional stresses the source makes the triggering condition, so the chain from degassing to earthquake nucleation is not represented in the rows. The question asks for those parts by name, so the rows answer the mechanism and its status but not the whole of what was asked.",
      "source_locators": [
        "page:5:block:002",
        "page:5:block:003",
        "page:2:block:004"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "A single block carries both records and the link between them: the hydrothermal-cooling hypothesis, the negative finding that no active venting is seen on the RC2 axis, and the use of that finding to set the hypothesis aside."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003",
            "page:4:block:002",
            "page:5:block:001"
          ],
          "rationale": "The negative finding that the axial valley shows no sign of an eruption under way, and its use against the magmatic-tectonic possibility, are both stated where the locator lands. Where the row also carries the target's not-supported disposition, that rests on the following block, which the derivation does not reach and which concludes melt movement does not apply here."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001",
            "page:3:block:003"
          ],
          "rationale": "The block states that inward-dipping high-angle faults bound the RC2 axial valley and that nothing there points to detachment faulting, and the preceding block says explicitly that this is why the mylonite shear-zone hypothesis is not supported."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "A single block carries both records and the link between them: the hydrothermal-cooling hypothesis, the negative finding that no active venting is seen on the RC2 axis, and the use of that finding to set the hypothesis aside. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003",
            "page:4:block:002",
            "page:5:block:001"
          ],
          "rationale": "The negative finding that the axial valley shows no sign of an eruption under way, and its use against the magmatic-tectonic possibility, are both stated where the locator lands. Where the row also carries the target's not-supported disposition, that rests on the following block, which the derivation does not reach and which concludes melt movement does not apply here. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001",
            "page:3:block:003"
          ],
          "rationale": "The block states that inward-dipping high-angle faults bound the RC2 axial valley and that nothing there points to detachment faulting, and the preceding block says explicitly that this is why the mylonite shear-zone hypothesis is not supported. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:2:block:004"
          ],
          "rationale": "The discussion offers the cold, thick lithosphere as one explanation for the deep earthquakes and then argues against it in the same block, which supports both the hypothesis framing and the not-supported disposition; the population concerned is the deep microseismicity under the RC2 axis named in the Results."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002",
            "page:2:block:004"
          ],
          "rationale": "The block states the hydrothermal-cooling hypothesis for the large earthquake depths and then closes it off, noting no active venting on the RC2 axis and an extinct field too far away to matter, so the hypothesis framing and its rejection both hold for the deep RC2 population."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003",
            "page:4:block:001",
            "page:2:block:004"
          ],
          "rationale": "The discussion raises localized high strain in semi-brittle mylonite shear zones as another hypothesis and says in the same sentence that the observations do not support it, the reason running into the next block; the population is the deep RC2 microseismicity."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002",
            "page:4:block:003",
            "page:5:block:001",
            "page:2:block:004"
          ],
          "rationale": "The block the locator reaches only presents the magmatic-tectonic possibility. The rejection that the record's not-supported disposition asserts sits in the two following blocks, which the derivation does not reach and which say the Iceland and Mayotte settings differ and that melt movement does not apply here. Judged on the reading, the hypothesis and its disposition both hold."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:002",
            "page:2:block:004"
          ],
          "rationale": "One sentence names the fourth possibility as the authors' preferred one: the deep microseismicity under segment RC2 tied to CO2 escaping from melt as it ascends. That matches the record's name, its hypothesised modality and its preferred disposition."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "A single block carries both records and the link between them: the hydrothermal-cooling hypothesis, the negative finding that no active venting is seen on the RC2 axis, and the use of that finding to set the hypothesis aside."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003",
            "page:4:block:002",
            "page:5:block:001"
          ],
          "rationale": "The negative finding that the axial valley shows no sign of an eruption under way, and its use against the magmatic-tectonic possibility, are both stated where the locator lands. Where the row also carries the target's not-supported disposition, that rests on the following block, which the derivation does not reach and which concludes melt movement does not apply here."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001",
            "page:3:block:003"
          ],
          "rationale": "The block states that inward-dipping high-angle faults bound the RC2 axial valley and that nothing there points to detachment faulting, and the preceding block says explicitly that this is why the mylonite shear-zone hypothesis is not supported."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "A single block carries both records and the link between them: the hydrothermal-cooling hypothesis, the negative finding that no active venting is seen on the RC2 axis, and the use of that finding to set the hypothesis aside. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003",
            "page:4:block:002",
            "page:5:block:001"
          ],
          "rationale": "The negative finding that the axial valley shows no sign of an eruption under way, and its use against the magmatic-tectonic possibility, are both stated where the locator lands. Where the row also carries the target's not-supported disposition, that rests on the following block, which the derivation does not reach and which concludes melt movement does not apply here. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001",
            "page:3:block:003"
          ],
          "rationale": "The block states that inward-dipping high-angle faults bound the RC2 axial valley and that nothing there points to detachment faulting, and the preceding block says explicitly that this is why the mylonite shear-zone hypothesis is not supported. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:2:block:004"
          ],
          "rationale": "The discussion offers the cold, thick lithosphere as one explanation for the deep earthquakes and then argues against it in the same block, which supports both the hypothesis framing and the not-supported disposition; the population concerned is the deep microseismicity under the RC2 axis named in the Results. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002",
            "page:2:block:004"
          ],
          "rationale": "The block states the hydrothermal-cooling hypothesis for the large earthquake depths and then closes it off, noting no active venting on the RC2 axis and an extinct field too far away to matter, so the hypothesis framing and its rejection both hold for the deep RC2 population. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003",
            "page:4:block:001",
            "page:2:block:004"
          ],
          "rationale": "The discussion raises localized high strain in semi-brittle mylonite shear zones as another hypothesis and says in the same sentence that the observations do not support it, the reason running into the next block; the population is the deep RC2 microseismicity. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002",
            "page:4:block:003",
            "page:5:block:001",
            "page:2:block:004"
          ],
          "rationale": "The block the locator reaches only presents the magmatic-tectonic possibility. The rejection that the record's not-supported disposition asserts sits in the two following blocks, which the derivation does not reach and which say the Iceland and Mayotte settings differ and that melt movement does not apply here. Judged on the reading, the hypothesis and its disposition both hold. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:002",
            "page:2:block:004"
          ],
          "rationale": "One sentence names the fourth possibility as the authors' preferred one: the deep microseismicity under segment RC2 tied to CO2 escaping from melt as it ascends. That matches the record's name, its hypothesised modality and its preferred disposition. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "One block carries the whole row: the cold, thick lithosphere explanation, and the thermal-modelling figure of 1100 to 1200 \u00b0C at 10 to 20 km that the authors use to conclude the mantle under the RC2 axis is hot, which is exactly the challenge the row records."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "The same block reports shallow off-axis events west of the RC2 axis showing the boundary stays above 10 km, and uses that against the cold lithosphere explanation. The record keeps the figure as an upper bound with no lower value, as the source does."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006",
            "page:5:block:002"
          ],
          "rationale": "The solubility calculation puts saturation and the onset of degassing near 25 km for a melt above 0.7 wt% CO2, and says that agrees with the deep microseismicity observed, which is the supporting link the row records; the preferred hypothesis itself is stated in the earlier block."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "One block carries the whole row: the cold, thick lithosphere explanation, and the thermal-modelling figure of 1100 to 1200 \u00b0C at 10 to 20 km that the authors use to conclude the mantle under the RC2 axis is hot, which is exactly the challenge the row records. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "The same block reports shallow off-axis events west of the RC2 axis showing the boundary stays above 10 km, and uses that against the cold lithosphere explanation. The record keeps the figure as an upper bound with no lower value, as the source does. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006",
            "page:5:block:002"
          ],
          "rationale": "The solubility calculation puts saturation and the onset of degassing near 25 km for a melt above 0.7 wt% CO2, and says that agrees with the deep microseismicity observed, which is the supporting link the row records; the preferred hypothesis itself is stated in the earlier block. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "The study-area block gives the MAR half-spreading rate here as 16 mm/yr and identifies the ridge itself, so the value, the unit and the feature all hold. The relation's locator points instead at the data-acquisition block, so the pairing is judged on the reading."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:002"
          ],
          "rationale": "The Results attribute 5.4 \u00b1 0.3 km of crust to the 8 Ma western flank of this ridge in the reasoning about the segment, matching value, uncertainty and unit, and the discussion supports calling RC2 magmatic."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:2:block:004"
          ],
          "rationale": "The Results put the deep events under the RC2 ridge axis at depths of 16 to 19 km, and a second Results block names that same deep population under the same axis, so the bounded depth in km and the population it concerns both hold. The relation's own locator lands on the general data-acquisition block, which carries neither, so I judged the pairing on the reading."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:004"
          ],
          "rationale": "The discussion says microseismicity reaching 10 km under NTD2 shows the brittle-ductile boundary sits at about that depth there, and the introduction defines the boundary the observation concerns."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:004"
          ],
          "rationale": "The discussion presents the cold, thick lithosphere explanation under which the brittle-ductile boundary would sit near 20 km, which matches both the value and the hypothesised status the record carries."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "The introduction explains that on slow- and ultraslow-spreading ridges this boundary is set from the deepest earthquakes, taken to mark the 700 \u00b1 100 \u00b0C isotherms, which gives the value, the uncertainty, the unit and the feature."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001",
            "page:5:block:010"
          ],
          "rationale": "The discussion reports another study's proposal that roughly 1.1 % melt must sit where the lithosphere meets the asthenosphere, and the preceding block introduces that boundary. The relation itself derives from an unrelated data-acquisition block, so the pairing is judged on the reading."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:5:block:005",
            "page:5:block:002"
          ],
          "rationale": "The Methods put the RC2 primary-melt CO2 at 0.4 to 3.0 wt% from the Ba90 proxy, the Results tie that volatile enrichment to the segment where the deep mantle earthquakes were found, and the preferred hypothesis names CO2 escaping from melt on its way up."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:5:block:005",
            "page:5:block:002"
          ],
          "rationale": "The Methods put the RC2 primary-melt CO2 at 0.4 to 3.0 wt% from the Ba90 proxy, the Results tie that volatile enrichment to the segment where the deep mantle earthquakes were found, and the preferred hypothesis names CO2 escaping from melt on its way up. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "One block carries the whole row: the cold, thick lithosphere explanation, and the thermal-modelling figure of 1100 to 1200 \u00b0C at 10 to 20 km that the authors use to conclude the mantle under the RC2 axis is hot, which is exactly the challenge the row records."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "The same block reports shallow off-axis events west of the RC2 axis showing the boundary stays above 10 km, and uses that against the cold lithosphere explanation. The record keeps the figure as an upper bound with no lower value, as the source does."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:5:block:005",
            "page:5:block:002"
          ],
          "rationale": "The Methods put the RC2 primary-melt CO2 at 0.4 to 3.0 wt% from the Ba90 proxy, the Results tie that volatile enrichment to the segment where the deep mantle earthquakes were found, and the preferred hypothesis names CO2 escaping from melt on its way up. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006",
            "page:5:block:002"
          ],
          "rationale": "The solubility calculation puts saturation and the onset of degassing near 25 km for a melt above 0.7 wt% CO2, and says that agrees with the deep microseismicity observed, which is the supporting link the row records; the preferred hypothesis itself is stated in the earlier block."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "One block carries the whole row: the cold, thick lithosphere explanation, and the thermal-modelling figure of 1100 to 1200 \u00b0C at 10 to 20 km that the authors use to conclude the mantle under the RC2 axis is hot, which is exactly the challenge the row records. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "The same block reports shallow off-axis events west of the RC2 axis showing the boundary stays above 10 km, and uses that against the cold lithosphere explanation. The record keeps the figure as an upper bound with no lower value, as the source does. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007",
            "page:5:block:005",
            "page:5:block:002"
          ],
          "rationale": "The Methods put the RC2 primary-melt CO2 at 0.4 to 3.0 wt% from the Ba90 proxy, the Results tie that volatile enrichment to the segment where the deep mantle earthquakes were found, and the preferred hypothesis names CO2 escaping from melt on its way up. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006",
            "page:5:block:002"
          ],
          "rationale": "The solubility calculation puts saturation and the onset of degassing near 25 km for a melt above 0.7 wt% CO2, and says that agrees with the deep microseismicity observed, which is the supporting link the row records; the preferred hypothesis itself is stated in the earlier block. This row projects a narrower field set on one endpoint than its sibling rows, so fewer property claims are at stake here."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "The study-area block gives the MAR half-spreading rate here as 16 mm/yr and identifies the ridge itself, so the value, the unit and the feature all hold. The relation's locator points instead at the data-acquisition block, so the pairing is judged on the reading."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:002"
          ],
          "rationale": "The Results attribute 5.4 \u00b1 0.3 km of crust to the 8 Ma western flank of this ridge in the reasoning about the segment, matching value, uncertainty and unit, and the discussion supports calling RC2 magmatic."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:2:block:004"
          ],
          "rationale": "The Results put the deep events under the RC2 ridge axis at depths of 16 to 19 km, and a second Results block names that same deep population under the same axis, so the bounded depth in km and the population it concerns both hold. The relation's own locator lands on the general data-acquisition block, which carries neither, so I judged the pairing on the reading."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:004"
          ],
          "rationale": "The discussion says microseismicity reaching 10 km under NTD2 shows the brittle-ductile boundary sits at about that depth there, and the introduction defines the boundary the observation concerns."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:004"
          ],
          "rationale": "The discussion presents the cold, thick lithosphere explanation under which the brittle-ductile boundary would sit near 20 km, which matches both the value and the hypothesised status the record carries."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "The introduction explains that on slow- and ultraslow-spreading ridges this boundary is set from the deepest earthquakes, taken to mark the 700 \u00b1 100 \u00b0C isotherms, which gives the value, the uncertainty, the unit and the feature."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001",
            "page:5:block:010"
          ],
          "rationale": "The discussion reports another study's proposal that roughly 1.1 % melt must sit where the lithosphere meets the asthenosphere, and the preceding block introduces that boundary. The relation itself derives from an unrelated data-acquisition block, so the pairing is judged on the reading."
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "The study-area block places the work where the Romanche transform meets the ridge on its eastern side, which is the intersection the row records."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:3:block:002"
          ],
          "rationale": "The geological description gives segment RC2 a median valley and a neo-volcanic ridge striking N154\u00b0E, so the feature, its strike and its position inside RC2 all hold."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "The study area says two non-transform discontinuities break the studied ridge portion, and the following block gives NTD1 its N76\u00b0E orientation and its magmatic and tectonic origin."
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "The same pair of blocks gives the two discontinuities that break this ridge portion, with NTD2 offsetting it on a N110\u00b0E trend."
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "The block describes NTD2 as affected over large areas by normal faults striking N115\u00b0E and N145\u00b0E, which gives both the fault set and its containment."
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "The study-area block puts a prominent oceanic core complex at the RTI segment east of the ridge axis, and the figure caption places it at the ridge's outside corner, so the complex and its position within the intersection hold."
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:1:block:005"
          ],
          "rationale": "The description says normal faults striking about N20\u00b0E and N20\u00b0W cut the surface of the core complex heavily, which matches the strike and the containment."
        },
        {
          "row_index": 59,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "The study area states outright that a detachment fault dipping westward bounds the RTI segment on its eastern side, but the source only says the lack of deep microseismicity near the complex's termination suggests that fault is now inactive. The row carries the inactive status flat, without that hedge."
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:005",
            "page:2:block:001",
            "page:3:block:002"
          ],
          "rationale": "The Methods treat RC3 as the segment next to the studied RC2 on its southern side, and the geological description gives RC3 its magmatic character and its ~N165\u00b0E orientation."
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "The study area identifies RC3 as the segment lying south of NTD2 on this stretch of the MAR, and the next block gives its magmatic character and orientation."
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "The study-area block splits the studied ridge portion into four subsections, the first being the RTI segment named RC1, which is the containment the row records."
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "The same subdivision lists NTD1 among the four subsections of the studied ridge, and the following block gives its orientation and its mixed origin."
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:002"
          ],
          "rationale": "RC2 is listed among the four subsections of the studied MAR portion, and the discussion supports its magmatic character."
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "NTD2 is the fourth of the listed subsections of the studied ridge, and its N110\u00b0E orientation is given in the following block."
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:3:block:002"
          ],
          "rationale": "The description gives segment RC2 a median valley about 10 km across, which is the axial valley and the containment the row records."
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002",
            "page:2:block:001"
          ],
          "rationale": "The discussion reports an extinct vent field observed on NTD1's eastern flank, which carries the field, its inactive state and its location in one sentence."
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004",
            "page:3:block:002",
            "page:1:block:005"
          ],
          "rationale": "The key-observations block puts the deep microseismicity under the axis of segment RC2, which gives the population, the segment and the beneath relation; RC2's magmatic character comes from the discussion block concluding that magmatism dominates its crustal accretion."
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004",
            "page:2:block:001"
          ],
          "rationale": "The same key-observations block places normal-depth events under the southern discontinuity NTD2, and the geological description gives NTD2 its N110\u00b0E orientation."
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004",
            "page:1:block:005"
          ],
          "rationale": "The key-observations block places the shallow events at the intersection's outside corner, under the faulted dome of the core complex and off-axis to the west of segment RC1, and the study-area block introduces that complex."
        }
      ]
    }
  ],
  "ratification": {
    "evaluator_kind": "HUMAN_AUTHOR",
    "actor_id": "actor:luis",
    "disposition": "RATIFIED_AS_RECORDED",
    "completed_at": "2026-09-05T01:34:13Z",
    "notes": "Ratified as recorded. Decided by Luis in chat on 2026-09-05 after the overseer presented every responsiveness verdict, the support counts, the three PARTIAL rows and the reviewer's three unsettled points (claim statement digests unverifiable from the allowed surface; twelve feature relations and five mechanism relations resolving through one locator to one general block; one NOT_SUPPORTED disposition resting on a block two past its derivation). Luis ordered a root-cause analysis of each of the three at ratification; the analyses are recorded separately and do not alter this record."
  }
}
```

Each `rows` entry has this shape:

```
{
  "row_index": 0,
  "source_support": "SUPPORTED | PARTIAL | UNSUPPORTED | NOT_EVALUABLE",
  "source_locators": ["page:2:block:004"],
  "rationale": "one or two sentences in your own words"
}
```
