# Malleus paper v4 run-21 source-grounded review record

Template. The row counts are substituted at freeze, from the frozen cell's own
query result, at the same time as `paper-v4/evaluation-v4/review-task-v4.template.md`.
No placeholder may survive instantiation.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

Fill one `rows` entry per returned row, in order, zero-based: 24 for
CQ-01, 122 for CQ-02, 178 for CQ-03, 166 for
CQ-04, 490 in all. Cite reading block ids only. Write the reasons in
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
  "status": "HUMAN_RATIFIED",
  "inputs": {
    "review_protocol_sha256": "sha256:88b69f6e80a3b9eac3a2c990178186df9c52fed3ced5c4e020162b0c202fa795",
    "review_input_manifest_sha256": "sha256:ca37103e0145350fc9526ed23071d219a463c798eb8e9d85b1a47a98ac37fdc8"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-preliminary-run-21",
    "completed_at": "2026-09-06T13:01:27Z"
  },
  "questions": [
    {
      "question_id": "CQ-01",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The rows name the campaign that acquired the data and they name the instrument kind used, and they cover the acquisition and processing chain in detail through methods, software artifacts and the relations tying software to method. The count of deployed instruments is nowhere in the returned rows: no row carries a number of instruments, and the observing system is present only as an instrument record named OBS with no network record and no cardinality, even though the block the campaign and instrument rows derive from states the network size. One of the four requested parts is therefore unanswered by the rows, which is why this is partial and not responsive.",
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
            "page:7:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The projection carries only a name and both cited blocks name that relocation method in the methods narrative, the first as the method the hypocenters were relocated with and the second as the relocation actually performed."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the magnitude scale and prints the formula immediately after it, and the projected expression is the same character sequence the text layer carries, artifacts included."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block states that this location algorithm was used to obtain hypocenters, which is the whole of the projected name."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the search algorithm used for the initial hypocenters, matching the projected name."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks name the trigger algorithm used for automatic arrival detection, so the projected name rests on prose in each of them."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the diagrams and says what was obtained from them, which covers the only projected field."
        },
        {
          "row_index": 6,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The campaign name is supported by both cited blocks. The projected duration is not: the first block gives that figure as the length of continuous seismic recording, not as the length of the cruise, and the second places the experiment across two months, so the row attaches a recording duration to the campaign without the qualifier the prose carries."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the solubility model and uses it to compute a saturation pressure, depth and temperature, which supports both the name and its classification as a numerical model."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block names the tool, says what it was used for, and gives the same address the row projects."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010",
            "page:8:block:011"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The name and the purpose sit in the first cited block, whose text layer breaks the address across the block boundary, and the remainder of that address is the whole of the second cited block, so the projected URL is supported only by citing both."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first cited block names the package and its use for focal mechanisms; the second gives the version number and the address the row projects."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first cited block names the program as the one the relocations were run with; the second carries the version and the address the row projects."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names this velocity model by that label and describes its effect on the located depths, which supports the name and its classification as a numerical model."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block names this velocity model by that label and records that it was chosen as the best fitting one, supporting both projected fields."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first cited block names the program as the one used for the initial locations; the second gives the address the row projects and confirms it is distributed software."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first cited block names the package as the one the detection ran inside; the second names it as software with the address the row projects."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first cited block names the program and what it was used to search for; the second gives the address the row projects."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first cited block names the software as the one the completeness and b value were computed with; the second gives the address the row projects."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The projection is a bare name and the cited figure-caption block names it, as the source of the dive observations plotted on the map. The block says nothing further about it, but nothing further is projected."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:2:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks name ocean-bottom seismometers under this abbreviation, the first as the network that acquired the data and the second as the deployed instruments drawn on the map."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block uses exactly this name when it says what the amplitude for the magnitude formula is measured on."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL The relation is formalized from the same block that formalizes both of its endpoints, so the pointer and the pairing sit in one place. That block says the relocations of that kind were determined using this program, and the code-availability block repeats the pairing, which is what the implements edge asserts."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004"
          ],
          "rationale": "DERIVATION_LOCAL The relation's block also formalizes both endpoints. Its prose calls the algorithm the program's own, which is a direct statement of the implements pairing rather than a co-occurrence."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002"
          ],
          "rationale": "DERIVATION_LOCAL The relation's block also formalizes both endpoints. It states that the detection algorithm was run within the named package, which supports the implements pairing as projected."
        }
      ]
    },
    {
      "question_id": "CQ-02",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "The rows name the ridge subsection the deep microseismicity belongs to and they place those events beneath its ridge axis with a depth range, and a further row gives the trend the deep events line up along relative to the axial faults. Both halves of the question are therefore answered directly by rows rather than by inference across them. The spatial part reaches the reader through the quantity label of the depth observations and through claim statements rather than through a typed spatial relation, and the earthquake population itself is not a record here, but nothing in the question is left unaddressed and no row makes the identification ambiguous.",
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
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this volcano among the settings where comparable magmatic-tectonic activity has been reported at depth, which carries both the name and the volcano classification."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block identifies the main axial normal faults as the structures the deep events run parallel to, so the name and the fault type both sit in the prose."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005",
            "page:4:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first block discusses seismicity beneath the floor of the axial valley and the second labels it on a cross-section; the projected kind is the feature itself."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:7:block:011"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first block introduces the abbreviation and defines it as the separation between brittle and ductile lithosphere; the second draws it as a boundary line in the schematic, which supports the boundary classification."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this transform fault as one of the two bounding the studied ridge stretch, and uses the abbreviation for transform faults defined earlier in the reading."
        },
        {
          "row_index": 5,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:4:block:003",
            "page:4:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The name is in the map legend and in the caption, but the caption treats this surface as belonging to the core complex rather than being one. The classification therefore goes past what the cited prose supports, while the name does not."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:7:block:011"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both blocks treat the crust as a layer of measured thickness sitting above the mantle, which is what the name and the layer classification assert."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block describes a fault dipping west that bounds the intersection segment along its eastern side, which covers both the name and the kind."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block places the study in that ocean by name, and the basin classification is the ordinary reading of it."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this peninsula as one of the Icelandic comparison sites, which is the whole of the projection."
        },
        {
          "row_index": 10,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block gives both strike directions and the discontinuity they characterize, so the name and the orientations hold. It calls them faults and nothing more, so the normal-fault classification is not what the cited prose says."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block calls these normal faults and gives both strikes, which covers name, kind and orientations."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block calls these normal faults, gives both strikes, and says they cut the core complex surface, which covers every projected field."
        },
        {
          "row_index": 13,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:4:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block gives the orientation and describes them as high-angle inward dipping faults bounding the segment, so name and orientation hold. It does not classify them as normal faults."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block is a map legend that carries this feature name, and the projected kind is the same term."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this ridge as one of the ultraslow-spreading ridges where deep mantle events have been seen, which supports name and kind."
        },
        {
          "row_index": 16,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:4:block:004",
            "page:4:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first block is a legend entry that carries the name alone. The caption block shades the hummocky sea floor and the cones in two different colours, treating them as separate classes, so the cone classification does not follow from the reading."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007",
            "page:4:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first block describes an inactive hydrothermal mound inferred from the submersible dives and the second labels it on the map, which covers the name and the mound classification."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this plate as the place where comparable sub-horizontal reflections were seen, supporting name and plate classification."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this ridge in the compilation of updated maximum-depth data, which supports name and kind."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first block names the boundary in full as where melt may sit at sub-solidus temperatures; the second gives the abbreviation the row projects. The boundary classification follows from both."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block attributes the cold-edge effect to old lithosphere, using the name and treating it as a layer."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this seamount and locates it on a ridge, which covers name and kind."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:7:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first block reports the deep events at mantle depths; the second labels it beside the crust in the schematic, which is where the layer classification comes from."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first block gives the full ridge name with its abbreviation and the second spells the expansion out again, so name and ridge classification both hold."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block describes the ridge stretch between the two transforms as a segment of stated length, which is what the name and the kind assert."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this island as one of the comparison sites, which is the whole projection."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block describes the median valley of the magmatic segment with its width; a median valley at a ridge axis is the axial valley, so the classification holds."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010",
            "page:7:block:011"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The schematic label carries the name and the caption calls it the expected interface drawn as a line, which supports the boundary classification."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this young volcanic ridge inside the segment and gives its strike, which is the orientation projected."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first block introduces this discontinuity by name among the four subsections and identifies it as a non-transform discontinuity; the second gives the orientation."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first block names this discontinuity as the second of the two non-transform discontinuities; the second gives the orientation the row projects."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both blocks name the oceanic core complex with its abbreviation and place it beside the ridge axis, which covers name and kind."
        },
        {
          "row_index": 33,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:005",
            "page:4:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both blocks carry the name, so the name holds. The prose makes this the edge of the core complex rather than a core complex in its own right, so the projected kind is not what the cited blocks support."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this massif and says where it sits, which covers name and kind."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this subsection as the intersection segment and lists it among the four ridge subsections, which supports name and segment classification."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this subsection and calls it a short ridge segment, which is exactly what the row projects."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first block names the segment south of the second discontinuity; the second gives its length and the orientation the row projects."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this transform fault as one of the two bounding the studied stretch, covering name and kind."
        },
        {
          "row_index": 39,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:3:block:003",
            "page:6:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The legend block carries the name and nothing else. The reading elsewhere treats this valley as the floor of the transform fault, not as a valley on the ridge axis, so the axial-valley classification is not supported."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the ridge-transform intersection with its abbreviation, which is both the name and the kind."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block is a map legend carrying this feature name, and the projected kind repeats it."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:5:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first block gives the full ridge name with the abbreviation the row projects; the second uses the abbreviation among ultraslow-spreading ridges, which supports the ridge classification."
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this supersegment in the compilation of updated data, which supports the name, and the segment classification follows from it."
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this numbered ridge segment in the same compilation, covering name and kind."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block is a map legend carrying this name, and the kind is the same term."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports an extinct hydrothermal vent field on the flank of the northern discontinuity, which supports the name, the vent-field kind and the inactive status."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:4:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both blocks name volcanic cones as observed morphology in the segment, which covers name and kind."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this ocean as where the offshore comparison site lies, which supports name and basin classification."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The relation is formalized from the same block that formalizes the faults, and that block states that the faults cut the surface of the core complex, which is the edge the row asserts."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "DERIVATION_LOCAL One block formalizes the relation and both endpoints. It names the seamount as belonging to the ridge, which is the part-of edge the row asserts."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The relation and both endpoints come from the same block, which places the ridge segment between the two transforms, so bounding by this one is stated rather than inferred."
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL Same block for the relation and both endpoints. The segment is described as lying between the two transforms, which supports bounding by this one."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL The relation block also formalizes both endpoints. It places the core complex at the ridge\u2019s outside corner, which supports the containment edge as the caption means it."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The relation and both endpoints are formalized in one block, which says the intersection segment is bounded eastward by the detachment fault. The block also gives the segment its short name, so the endpoint identification does not depend on another block."
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The relation block is one of the blocks that formalize the endpoints. It places the segment immediately south of the discontinuity, which is the adjacency asserted."
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The relation block also formalizes the fault endpoint. It states that the segment is bounded by those inward dipping faults; the negation carried in the same sentence is about detachment faults, not about this edge."
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The relation block formalizes both endpoints. It names the segment as the one lying south of the discontinuity, which is the adjacency asserted."
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DERIVATION_LOCAL The relation block also formalizes the vent field. It places that vent field on the eastern side of the discontinuity, which supports the containment edge."
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is the sentence the record reproduces and its digest recomputes. The block reports the deep events under the segment axis lining up along a single trend parallel to the axial faults, and it names the segment, so the claim is about the segment shown. The sentence runs past the end of the block, so the retained text stops mid-clause, but nothing in the projection depends on the missing words."
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block concludes from the location tests that the deep events under the segment axis are required by the data rather than artifacts, and it names the segment, which is what the record claims and about what."
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the degassing mechanism, the strain it produces under extension and the earthquakes it triggers in the mantle, so both the statement and the mantle as its subject rest on this block."
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment, states the degassing explanation for its deep microseismicity, and marks that explanation as the one the authors prefer, which supports the statement and the preferred disposition alike."
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block describes the mound as inactive and attributes the inference to the dive observations, which is the claim and its subject."
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block records the absence of active venting on the segment axis and names the segment, which supports the negated claim and its subject."
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states that no current eruption is evidenced in the axial valley and gives the grounds, so the negated claim and the valley as its subject both hold."
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block attributes the shallow events under the dome to ruptures on the faults cutting its surface, and the dome is the core complex the row names as subject."
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states where the massif sits and why it is included in the compilation, which is the claim and its subject."
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block calls the intersection segment amagmatic and describes what bounds it, and the same block gives that segment the short name the row uses as subject."
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports normal velocity ratios from tomography in the named segment, which supports the claim and the segment as its subject."
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reads the boundary depth off the seismicity beneath the discontinuity and gives it as about ten kilometres, which matches the value, the unit and the approximate qualification, and the boundary is the subject."
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the depth the boundary would have under the cold and thick lithosphere explanation, which is the hypothesised value and unit the row carries; the boundary is named in the same block."
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the isotherm value with its stated tolerance and ties it to the definition of the boundary, so value, uncertainty, unit and subject all rest here."
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states that the boundary stays shallower than ten kilometres off axis, which is the open upper bound and unit the row carries."
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the barium-based pre-eruptive range for the named segment, and the surrounding sentences say the figures are estimates from a fixed ratio, which supports the values, the unit and the estimated determination."
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the barium-based range for the southern segment in the same sentence pair, matching the values, unit and estimated status the row carries."
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the barium-based primary-melt range for the named segment, with the unit and the estimation language the row carries."
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the barium-based primary-melt range for the southern segment, which is the value pair, unit and status projected."
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the calculated volatile content of the melts along the named segment as a range in weight percent, which is the value pair and unit the row carries."
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the comparison range for the southern segment, matching the values and unit projected."
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states a floor for the primary-melt concentration along the named segment, which is the open lower bound and unit the row carries."
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the rubidium-based pre-eruptive range for the named segment alongside the barium one, which supports value, unit and estimated status."
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the rubidium-based range for the southern segment, matching the projected values and unit."
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the rubidium-based primary-melt range for the named segment, which is what the row projects."
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium-based primary-melt range for the southern segment, matching the values and unit."
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the age of the cold lithosphere responsible for the edge effect, which is the value, unit and subject the row carries."
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the length of ridge axis the network covered, and names the ridge, so value, unit and subject all rest here."
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the length of the transform covered by the network and names the transform, which is the value and subject projected."
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the crustal thickness of the western flank with its tolerance and the age of that crust, which supports value, uncertainty, unit and the crust as subject."
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the depth range of the deep earthquakes observed beneath the named segment axis, which is the value pair, unit and subject the row carries."
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block lists the three depth observations and gives the deep microseismicity beneath the named segment axis as an approximate range, which supports the values, the unit, the approximate qualification and the subject."
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block has the rising melt continuing to degas and generating mantle earthquakes across the stated depth interval, which is the hypothesised range, unit and subject."
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the shallower-than bound observed beneath the discontinuity, matching the open upper bound, unit and subject."
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the shallower bound beneath the core complex, which is the value and subject this row projects."
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the average concentration reported for segments in that ocean region and marks it as suggested by earlier work, which supports the value, the unit and the estimated status; the region is named in the same block."
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the number of events located along the ridge after relocation, and the ridge is the scope the count is stated for, so both the count and its subject rest here."
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the number of events located along the transform, which is the count and the subject the row projects."
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The schematic caption ties the boundary line to a single isotherm value, which is the value, unit and subject the row carries."
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same caption gives the crustal thickness beneath the named segment with its tolerance, matching the value, uncertainty and unit for the crust as subject."
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The schematic caption gives the depth range of the deep earthquakes below the sea floor beneath the ridge axis and names the ridge, which supports the values, the unit and the subject."
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block says how many events were put in the subset built to test the deep locations beneath the named segment, so the count, its scope and the segment as subject all rest here."
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block places these earthquakes in a hot mantle above a stated temperature, which is the open lower bound, the unit and the subject."
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the melt fraction another study found necessary at the boundary\u2019s base, matching the value, the percentage unit and the modelled determination."
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the half rate at which the ridge spreads here, which is the value, unit and subject the row projects."
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the approximate length of the ridge segment between the two transforms, which is the value, unit and subject."
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the depth floor of the offshore comparison activity and names the island, so value, unit and subject hold."
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the width of the median valley in the magmatic segment, which is the value, unit and subject the row carries."
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block infers from microseismicity across that depth interval that ascending melt sits in the mantle at those depths, which supports the range, unit and subject."
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the modelled temperature interval for that depth interval and concludes the mantle there is hot, which supports the values, the unit, the modelled determination and the subject."
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block records that no earthquakes appear below the stated depth beneath the named ridge axis, which is the negated open lower bound, the unit and the subject."
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the normal depth range of the earthquakes beneath the southern discontinuity, matching the values, unit and subject."
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the approximate length of the northern discontinuity, which is the value, unit and subject."
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block says the earthquakes beneath that discontinuity reach down to about ten kilometres, which supports the bound, the unit and the subject; the approximation in the prose is not carried by the projected qualification, which states an open upper bound instead."
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the ridge offset of the southern discontinuity, which is the value, unit and subject."
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the shallow focal depths of the cluster west of the axial valley, which is the range, unit and subject the row projects."
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the depth the off-axis shallow seismicity west of the named segment axis reaches, which supports the bound, the unit and the segment as subject."
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the estimated pre-eruptive concentration range for the named segment after fractional crystallization, matching the values, unit and estimated status."
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the approximate length of the named segment, which is the value, unit and subject."
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the length of the southern magmatic segment, which is the value, unit and subject."
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the depth range of the shallow earthquakes at the intersection\u2019s outside corner, which supports the values, the unit and the intersection as subject."
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the highest melt concentration previously reported at that ridge, which is the value, unit and subject the row projects."
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence that gives the western flank thickness also gives the age of that crust, which is the value, unit and subject here."
        }
      ]
    },
    {
      "question_id": "CQ-03",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The set does contain what the question asks for. Earthquake depths beneath the central segment come back with units and a measured modality, and calculated primary-melt CO2 comes back with units and an estimated or derived status. What the rows do not do is single either out. Several different depth ranges and several different CO2 ranges are returned side by side, for the central segment and for its southern neighbour, and nothing in the row representation marks which pair is the reported answer for the central association. Most of the returned rows are named features, materials, methods and software that carry no quantity at all.",
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
          "rationale": "NO_SUBJECT_IN_ROW The relocation paragraph names the double-difference location method as the technique applied after the initial hypocentre step, which is the whole of the row.",
          "source_locators": [
            "page:2:block:002",
            "page:7:block:006"
          ]
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The magnitude section names the local magnitude scale ML and prints the same defining expression the row carries.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The results paragraph names the non-linear earthquake location algorithm used for the hypocentres; the row claims nothing beyond the name.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The earthquake-location paragraph names the non-linear oct-tree search algorithm.",
          "source_locators": [
            "page:7:block:004"
          ]
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks name the short-term-average/long-term-average trigger algorithm used for automatic detection.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The Vp/Vs paragraph names Wadati diagrams as the technique that yields the ratio.",
          "source_locators": [
            "page:7:block:002"
          ]
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The degassing-depth paragraph names the CO2 solubility model and computes a saturation pressure with it, which bears out the name and the numerical-model kind.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block names Global Mapper and gives the same access URL the row carries.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block names the GMT 6 toolbox, and its URL runs on into the second cited block.",
          "source_locators": [
            "page:8:block:010",
            "page:8:block:011"
          ]
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The focal-mechanism paragraph names the HASH package and the code block gives version 1.2 with the same URL.",
          "source_locators": [
            "page:8:block:003",
            "page:8:block:010"
          ]
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The relocation paragraph names the hypoDD program and the code block gives version 1.3 with the same URL.",
          "source_locators": [
            "page:7:block:006",
            "page:8:block:010"
          ]
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The depth-resolution paragraph names Model 1 as the fastest velocity model, covering name and numerical-model kind.",
          "source_locators": [
            "page:7:block:009"
          ]
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The velocity-model paragraph names Model 5 as the average velocity model that was selected.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Four cited blocks name the NonLinLoc program and the code block supplies the access URL.",
          "source_locators": [
            "page:7:block:004",
            "page:7:block:005",
            "page:7:block:007",
            "page:8:block:010"
          ]
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Three cited blocks name the SEISAN package and the code block supplies the access URL.",
          "source_locators": [
            "page:6:block:002",
            "page:8:block:002",
            "page:8:block:010"
          ]
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The model-evaluation paragraph names the VELEST program and the code block gives its URL.",
          "source_locators": [
            "page:6:block:004",
            "page:8:block:010"
          ]
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The magnitude paragraph names the ZMAP software and the code block gives its URL.",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ]
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The trace-element and proxy sentences treat Ba as one of the incompatible elements behind the CO2 estimate, which covers name and element kind.",
          "source_locators": [
            "page:5:block:004",
            "page:6:block:005",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited blocks refer to basalt and basaltic rock on the seafloor and in the sample set, covering the name and the rock kind.",
          "source_locators": [
            "page:1:block:001",
            "page:2:block:001",
            "page:3:block:001",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW CO2 is named across all four cited blocks as the volatile species at issue, and the formula is the name.",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002",
            "page:6:block:001",
            "page:7:block:012"
          ]
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The solubility sentence has CO2 nucleating a gas phase, which covers the name and the fluid-phase kind.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The volatiles sentence and the LAB sentence both name H2O beside CO2; the text layer splits the digit off, but a reader sees the species.",
          "source_locators": [
            "page:1:block:001",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks discuss magma and magmatic systems, covering the name and the melt kind.",
          "source_locators": [
            "page:4:block:003",
            "page:5:block:002"
          ]
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Melt is named as the material derived from the mantle and again as the ascending phase in the Fig. 6 interpretation.",
          "source_locators": [
            "page:1:block:002",
            "page:7:block:010",
            "page:7:block:012"
          ]
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW MORB is named in the compilation paragraphs and in the proxy sentence, covering name and rock kind.",
          "source_locators": [
            "page:5:block:004",
            "page:8:block:005",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks refer to mylonite shear zones, covering the name and the rock kind.",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:003"
          ]
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Olivine appears as the host of the melt inclusions and as the Fo90 composition used in the calculation.",
          "source_locators": [
            "page:5:block:004",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Peridotite is named on the seafloor, in the sub-solidus sentence and in the crust-free lithosphere sentence.",
          "source_locators": [
            "page:1:block:006",
            "page:2:block:001",
            "page:6:block:001",
            "page:7:block:010"
          ]
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The NTD1 origin sentence names pillow basalts on the seafloor.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Three cited blocks refer to the primary melt or primary melts as the object of the CO2 estimate.",
          "source_locators": [
            "page:1:block:001",
            "page:6:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Rb appears in the same trace-element and proxy sentences as Ba, covering name and element kind.",
          "source_locators": [
            "page:5:block:004",
            "page:6:block:005",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The magmatic-tectonic paragraph names Askja Volcano in Iceland.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The alignment sentence names the main axial normal faults that the deep events run parallel to.",
          "source_locators": [
            "page:4:block:003"
          ]
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The axial valley is named in the detachment-inactivity sentence and again in the Fig. 3 panel labels.",
          "source_locators": [
            "page:2:block:005",
            "page:4:block:004"
          ]
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The abstract and the introduction name the brittle-ductile boundary and its abbreviation, and the Fig. 6 caption treats it as an interface.",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:004",
            "page:7:block:010",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The study-area sentence names the Chain TF as one bound of the segment, and TF is the paper's own abbreviation for transform fault.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 36,
          "source_support": "PARTIAL",
          "rationale": "NO_SUBJECT_IN_ROW The caption puts the corrugated surface on the OCC and the panel legend repeats the term, so the name holds; what the cited prose will not carry is the row's classification of that surface as itself an oceanic core complex.",
          "source_locators": [
            "page:4:block:003",
            "page:4:block:006"
          ]
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited blocks treat the crust as the layer above the mantle and give its thickness.",
          "source_locators": [
            "page:2:block:006",
            "page:7:block:010",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The RTI sentence names the westward dipping detachment fault that bounds the segment.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The opening sentence of the study places the work in the equatorial Atlantic Ocean.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The magmatic-tectonic paragraph names the Fagradalsfjall Peninsula in Iceland.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 41,
          "source_support": "PARTIAL",
          "rationale": "NO_SUBJECT_IN_ROW The NTD1 sentence gives both strike directions the row carries, but it calls them faults without qualifying them as normal faults, so the row's fault kind runs past the cited prose.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The NTD2 sentence names normal faults with exactly the two strikes the row carries.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The OCC sentence names normal faults with the two strikes the row carries.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 44,
          "source_support": "PARTIAL",
          "rationale": "NO_SUBJECT_IN_ROW The cited sentence gives the NNW-SSE orientation and the inward dipping description, but it never calls these faults normal faults, so that field is unsupported.",
          "source_locators": [
            "page:4:block:001"
          ]
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The Fig. 1 legend lists a fracture zone among the mapped features, and here name and kind are the same term, so the thin legend basis still covers what the row asserts.",
          "source_locators": [
            "page:3:block:003"
          ]
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The ultraslow-ridge sentence names the Gakkel Ridge as a spreading ridge.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 47,
          "source_support": "PARTIAL",
          "rationale": "NO_SUBJECT_IN_ROW The panel legend lists Hummocky as its own map symbol alongside Volcanoes, so the name holds while the row's volcanic-cone kind does not follow from the cited block.",
          "source_locators": [
            "page:4:block:004"
          ]
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The Fig. 1 caption describes an inactive hydrothermal mound and the Fig. 3 legend repeats the label.",
          "source_locators": [
            "page:2:block:007",
            "page:4:block:004"
          ]
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The LAB paragraph names the young Juan de Fuca plate.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The maximum-depth compilation names the Knipovich Ridge.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The abstract and the Keller sentence both name the lithosphere-asthenosphere boundary and its abbreviation.",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010"
          ]
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cold-edge sentence names the lithosphere and gives its age.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The compilation sentence names the Logachev Seamount.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The abstract places the deep earthquakes in the mantle and the Fig. 6 labels list it beside the crust.",
          "source_locators": [
            "page:1:block:001",
            "page:7:block:010"
          ]
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The Fig. 1 caption spells the abbreviation out and three further blocks name the ridge.",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:005",
            "page:2:block:007",
            "page:8:block:002"
          ]
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The study-area sentence names the MAR segment between the two transform faults and the Fig. 5 caption refers to it again.",
          "source_locators": [
            "page:1:block:005",
            "page:6:block:005"
          ]
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The magmatic-tectonic paragraph names Mayotte Island.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The RC2 description puts a 10-km-wide median valley on that ridge segment, which is the segment's axial valley.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The Fig. 6 labels and caption name the Moho and treat it as an interface.",
          "source_locators": [
            "page:7:block:010",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The RC2 sentence names an N154 degrees E oriented neo-volcanic ridge, matching the row's name and orientation.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The subdivision sentence names NTD1 as the first non-transform discontinuity and the description block gives the N76 degrees E orientation.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ]
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The subdivision sentence names NTD2, the description block gives the N110 degrees E orientation, and two further blocks label it.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001",
            "page:4:block:005",
            "page:7:block:010"
          ]
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The RTI sentence and the Fig. 1 caption both spell out the oceanic core complex and its abbreviation.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007",
            "page:7:block:010"
          ]
        },
        {
          "row_index": 64,
          "source_support": "PARTIAL",
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks use the term OCC termination, so the name holds; neither supports treating the termination itself as an oceanic core complex.",
          "source_locators": [
            "page:2:block:005",
            "page:4:block:003"
          ]
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The compilation paragraph names the Rainbow massif and places it at a non-transform discontinuity.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The subdivision sentence names RC1 as one of the four ridge subsections.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The subdivision sentence calls RC2 a short ridge segment and the Fig. 6 labels name it again.",
          "source_locators": [
            "page:1:block:005",
            "page:7:block:010"
          ]
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Two cited blocks name RC3 as the ridge segment south of NTD2 and give its orientation of about N165 degrees E.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ]
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Five cited blocks name the Romanche TF or the Romanche transform.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007",
            "page:5:block:005",
            "page:6:block:003",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 70,
          "source_support": "PARTIAL",
          "rationale": "NO_SUBJECT_IN_ROW The Fig. 1 legend lists the Romanche transform valley, so the name holds, but a transform valley is not the ridge's axial valley and the block gives no ground for the row's kind.",
          "source_locators": [
            "page:3:block:003"
          ]
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The study-area sentence spells out the ridge-transform intersection and its abbreviation.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The Fig. 1 legend lists a suspended valley, and the row's name and kind are that same term.",
          "source_locators": [
            "page:3:block:003"
          ]
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cold-lithosphere sentence spells out the Southwest Indian Ridge and its abbreviation.",
          "source_locators": [
            "page:3:block:001",
            "page:5:block:009"
          ]
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The compilation sentence names the SWIR oblique Supersegment among the ridge sites whose depths were updated.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same compilation sentence names SWIR segment 8.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The Fig. 1 legend lists a transverse ridge, and name and kind coincide.",
          "source_locators": [
            "page:3:block:003"
          ]
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The hydrothermal-cooling paragraph reports an extinct hydrothermal vent field on the NTD1 flank, which covers the name and the inactive status; the text layer runs vent and field together.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The magmatic-origin sentence and the Fig. 3 caption both name volcanic cones.",
          "source_locators": [
            "page:3:block:001",
            "page:4:block:007"
          ]
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The magmatic-tectonic paragraph places Mayotte in the western Indian Ocean.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The trace-element sentence gives CO2 over Ba as 81.3 with an uncertainty of 23, matching numerator, denominator, value and uncertainty.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The methods sentence repeats CO2 over Ba as 81.3 with an uncertainty of 23 as the constant used for the estimate.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The same trace-element sentence gives CO2 over Rb as 991 with an uncertainty of 129.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The methods sentence repeats CO2 over Rb as 991 with an uncertainty of 129.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The Vp/Vs paragraph gives the ratio as about 1.7 from the Wadati diagrams, matching value, approximation and calculated modality.",
          "source_locators": [
            "page:7:block:002"
          ]
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The Fig. 5 caption lists melt inclusions as one of the plotted sample sets.",
          "source_locators": [
            "page:6:block:005"
          ]
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Four cited blocks refer to the compiled MORB samples.",
          "source_locators": [
            "page:5:block:004",
            "page:6:block:005",
            "page:8:block:005"
          ]
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The Fig. 5 caption lists popping rocks among the plotted samples.",
          "source_locators": [
            "page:6:block:005"
          ]
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The Fig. 5 caption names MORB whole rocks as a plotted sample set.",
          "source_locators": [
            "page:6:block:005"
          ]
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relocation sentence has hypoDD carrying out the double-difference relocations, which is what the pairing asserts, and the same block formalises the program endpoint.",
          "source_locators": [
            "page:7:block:006"
          ]
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The location paragraph attributes the oct-tree search algorithm to NonLinLoc and formalises both endpoints.",
          "source_locators": [
            "page:7:block:004"
          ]
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The detection sentence places the trigger algorithm inside the SEISAN package and formalises SEISAN in the same block.",
          "source_locators": [
            "page:6:block:002"
          ]
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The OCC sentence has the normal faults cutting the complex's surface, and it is the block that formalises the fault endpoint.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The compilation sentence names the Logachev Seamount as belonging to the Knipovich Ridge and formalises both endpoints.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The study-area sentence places the MAR segment between the Romanche and Chain transform faults, which carries the Chain bound, and it formalises both endpoints.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The same sentence carries the Romanche bound of the segment and formalises both endpoints.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The Fig. 1 caption puts the oceanic core complex on the outside corner of the MAR, and that block formalises both endpoints.",
          "source_locators": [
            "page:2:block:007"
          ]
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The RTI sentence has the segment bounded to the east by the detachment fault and formalises both endpoints.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The RC2 description places the segment immediately south of NTD1, which is what adjacency asserts, and that block formalises the NTD1 endpoint.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The cited sentence has RC2 bounded by the inward dipping faults and formalises the fault endpoint.",
          "source_locators": [
            "page:4:block:001"
          ]
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The naming sentence places RC3 immediately south of NTD2 and formalises both endpoints.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The hydrothermal paragraph puts the extinct vent field on the eastern flank of NTD1 and formalises the vent-field endpoint.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The MORB methods sentence has the authors analysing samples from segment RC2 and formalises the sample endpoint.",
          "source_locators": [
            "page:8:block:005"
          ]
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The same sentence covers the RC3 samples and formalises the sample endpoint.",
          "source_locators": [
            "page:8:block:005"
          ]
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence is a statement about what Model 1 does to the event depths, so the record is about the model it names.",
          "source_locators": [
            "page:7:block:009"
          ]
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence is a judgement on Model 5 itself, naming it the best-fitting model.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence states the authors' preference for Model 5, so the model is what the claim is about.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The claim characterises the geochemical behaviour of CO2, which is the subject the row shows.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence characterises seafloor basalts as degassed, and basalt is the subject.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence describes the orientation of the deep events beneath the RC2 axis, so the segment is the locus the claim characterises.",
          "source_locators": [
            "page:4:block:003"
          ]
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence is a verdict on the deep events beneath the RC2 ridge axis, which the block names.",
          "source_locators": [
            "page:8:block:001"
          ]
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The mechanism sentence puts the triggered earthquakes in the mantle, which is the subject the record carries.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence is about the deep microseismicity beneath RC2 and marks the explanation as the authors' preferred one, which matches the row's disposition.",
          "source_locators": [
            "page:5:block:002"
          ]
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The Fig. 1 caption is about the inactive hydrothermal mound the record takes as its subject.",
          "source_locators": [
            "page:2:block:007"
          ]
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence is a negative observation about the RC2 axis.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence denies a current eruption in the axial valley, which is the subject.",
          "source_locators": [
            "page:4:block:003"
          ]
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence explains the shallow earthquakes beneath the OCC dome, so the complex is what the claim is about.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The compilation sentence is about the Rainbow massif and its setting.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence characterises the RTI segment, which the row shows under its RC1 name and its RTI segment tag.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence reports normal Vp/Vs ratios for segment RC2.",
          "source_locators": [
            "page:7:block:003"
          ]
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The calculation sentence concludes that the analysed samples are degassed, so the sample set is the subject.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The enrichment sentence puts Ba above 89 ppm in the RC2 samples, matching value, unit and open lower bound.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The solubility sentence gives an 80 to 90 per cent loss for CO2 on saturation, matching the range, the unit and the hypothesised modality.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The abstract gives about 0.4 to 3.0 wt% CO2 in the primary melts, matching bounds, unit, approximation and calculated status.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same enrichment sentence puts Rb above 8 ppm, matching the row's bound and unit.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The LAB paragraph gives about 1250 degrees C as the sub-solidus temperature for anhydrous peridotites.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The NTD2 sentence puts the BDB at about 10 km, matching value and unit.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cold-lithosphere explanation puts the BDB at about 20 km under that hypothesis, and the row records it as hypothesised.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The introduction ties the maximum earthquake depth to the 700 plus or minus 100 degrees C isotherms, matching value, uncertainty and unit.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 129,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The off-axis sentence keeps the BDB shallower than 10 km, matching the open upper bound.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 130,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods result gives CO2 from Ba as 0.7 to 4.6 wt% for RC2, matching bounds, unit and estimated status.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 131,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same paragraph gives CO2 from Ba as 0.06 to 0.8 wt% for RC3.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 132,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The primary-melt result gives CO2 from Ba90 as 0.4 to 3.0 wt% for RC2.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 133,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives CO2 from Ba90 as 0.04 to 0.5 wt% for RC3.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 134,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The results paragraph gives calculated CO2 of 0.4 to 3.0 wt% for melts along RC2.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 135,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives 0.04 to 0.7 wt% for RC3.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 136,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods conclusion sets a floor of 0.4 wt% CO2 in the primary melts along RC2, matching the open lower bound.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 137,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods result gives CO2 from Rb as 0.9 to 4.3 wt% for RC2.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 138,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same paragraph gives CO2 from Rb as 0.07 to 1.0 wt% for RC3.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 139,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The primary-melt sentence gives CO2 from Rb90 as 0.5 to 2.8 wt% for RC2.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 140,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives CO2 from Rb90 as 0.05 to 0.7 wt% for RC3.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 141,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cold-edge sentence gives the lithosphere an age of 45 Ma.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 142,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The acquisition sentence gives 120 km of MAR axis covered.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 143,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives 140 km of the eastern Romanche TF covered.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 144,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The refraction sentence gives the western-flank crust a thickness of 5.4 plus or minus 0.3 km.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 145,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The observation sentence puts the deep earthquakes beneath the RC2 axis at 16 to 19 km.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 146,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The key-observations sentence puts the deep microseismicity beneath the RC2 ridge axis at about 10 to 20 km.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 147,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The degassing sentence puts the produced earthquakes between 10 and 20 km in the mantle, and the row keeps it hypothesised.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 148,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The depth sentence caps the events beneath NTD2 below 10 km.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 149,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence caps the events beneath the OCC below 6 km.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 150,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The equatorial-Atlantic sentence gives an average of about 2800 ppm CO2 at several segments.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 151,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The relocation result counts 317 events along the MAR.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 152,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence counts 197 events along the Romanche TF.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 153,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The Fig. 6 caption ties the BDB to the 750 degrees C isotherm.",
          "source_locators": [
            "page:7:block:011"
          ]
        },
        {
          "row_index": 154,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same caption gives the crust beneath RC2 a thickness of about 5.4 plus or minus 0.3 km.",
          "source_locators": [
            "page:7:block:011"
          ]
        },
        {
          "row_index": 155,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The Fig. 6 interpretation gives the deep earthquakes beneath the MAR axis as 10 to 19 km below the seafloor.",
          "source_locators": [
            "page:7:block:012"
          ]
        },
        {
          "row_index": 156,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The validation sentence counts 45 events in the subset built for the deep locations beneath RC2.",
          "source_locators": [
            "page:7:block:010"
          ]
        },
        {
          "row_index": 157,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The RC2 discussion puts these earthquakes in a mantle hotter than 1100 degrees C.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 158,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The LAB paragraph gives about 1.1 per cent melt required at the base of the boundary, and the row keeps it modelled and hypothesised.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 159,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The study-area sentence gives the MAR a half-spreading rate of 16 mm/yr.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 160,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the segment a length of about 200 km.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 161,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The magmatic-tectonic sentence gives depths greater than 30 km offshore Mayotte.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 162,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The RC2 description gives the median valley a width of 10 km.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 163,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The LAB paragraph reads the 10 to 20 km microseismicity as ascending melt residing in the mantle at those depths.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 164,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The thermal-modelling sentence gives 1100 to 1200 degrees C at 10 to 20 km depth and the row records it as modelled.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 165,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence denies earthquakes deeper than 20 km beneath the RC2 axis, matching the negated modality and the bound.",
          "source_locators": [
            "page:5:block:007"
          ]
        },
        {
          "row_index": 166,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The key-observations sentence gives 4 to 10 km for the events beneath the southern NTD2.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 167,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The NTD1 sentence gives a length of about 35 km.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 168,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The NTD2 sentence takes the earthquakes down to about 10 km.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 169,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The NTD2 sentence gives a ridge offset of about 33 km.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 170,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cluster sentence gives focal depths of about 2 to 6 km on the western side of the axial valley.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 171,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The off-axis sentence takes the shallow microseismicity west of the RC2 axis down to 6 km.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 172,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The fractionation sentence gives pre-eruptive CO2 of 0.7 to 4.6 wt% for RC2.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 173,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The RC2 description gives the segment a length of about 22 km.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 174,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The RC3 sentence gives a length of 50 km.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 175,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The key-observations sentence gives 0 to 6 km for the shallow earthquakes at the RTI outside corner.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 176,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The comparison sentence gives 1.9 wt% as the highest CO2 previously reported at the SWIR.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 177,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The refraction sentence gives the western-flank crust an age of 8 Ma.",
          "source_locators": [
            "page:2:block:006"
          ]
        }
      ]
    },
    {
      "question_id": "CQ-04",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The preferred mechanism is present and it is marked as a hypothesis rather than a fact. One row carries the preferred disposition under a hypothesised modality and names the ascending melt and the CO2 degassing; a second row, also hypothesised, carries the volume change, the extensional stresses and the triggering of the deep earthquakes; a third gives the Fig. 6 reading of the deep events as a consequence of that degassing. The question is answered only by reading those rows together, and nothing in the representation links them or marks them off from the surrounding rows, which are named features, materials and software with no bearing on the mechanism.",
      "source_locators": [
        "page:5:block:002",
        "page:5:block:003",
        "page:7:block:012"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The relocation paragraph names the double-difference location method as the technique applied after the initial hypocentre step, which is the whole of the row.",
          "source_locators": [
            "page:2:block:002",
            "page:7:block:006"
          ]
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The magnitude section names the local magnitude scale ML and prints the same defining expression the row carries.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The results paragraph names the non-linear earthquake location algorithm used for the hypocentres; the row claims nothing beyond the name.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The earthquake-location paragraph names the non-linear oct-tree search algorithm.",
          "source_locators": [
            "page:7:block:004"
          ]
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks name the short-term-average/long-term-average trigger algorithm used for automatic detection.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The Vp/Vs paragraph names Wadati diagrams as the technique that yields the ratio.",
          "source_locators": [
            "page:7:block:002"
          ]
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The degassing-depth paragraph names the CO2 solubility model and computes a saturation pressure with it, which bears out the name and the numerical-model kind.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block names Global Mapper and gives the same access URL the row carries.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block names the GMT 6 toolbox, and its URL runs on into the second cited block.",
          "source_locators": [
            "page:8:block:010",
            "page:8:block:011"
          ]
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The focal-mechanism paragraph names the HASH package and the code block gives version 1.2 with the same URL.",
          "source_locators": [
            "page:8:block:003",
            "page:8:block:010"
          ]
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The relocation paragraph names the hypoDD program and the code block gives version 1.3 with the same URL.",
          "source_locators": [
            "page:7:block:006",
            "page:8:block:010"
          ]
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The depth-resolution paragraph names Model 1 as the fastest velocity model, covering name and numerical-model kind.",
          "source_locators": [
            "page:7:block:009"
          ]
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The velocity-model paragraph names Model 5 as the average velocity model that was selected.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Four cited blocks name the NonLinLoc program and the code block supplies the access URL.",
          "source_locators": [
            "page:7:block:004",
            "page:7:block:005",
            "page:7:block:007",
            "page:8:block:010"
          ]
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Three cited blocks name the SEISAN package and the code block supplies the access URL.",
          "source_locators": [
            "page:6:block:002",
            "page:8:block:002",
            "page:8:block:010"
          ]
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The model-evaluation paragraph names the VELEST program and the code block gives its URL.",
          "source_locators": [
            "page:6:block:004",
            "page:8:block:010"
          ]
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The magnitude paragraph names the ZMAP software and the code block gives its URL.",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ]
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The trace-element and proxy sentences treat Ba as one of the incompatible elements behind the CO2 estimate, which covers name and element kind.",
          "source_locators": [
            "page:5:block:004",
            "page:6:block:005",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited blocks refer to basalt and basaltic rock on the seafloor and in the sample set, covering the name and the rock kind.",
          "source_locators": [
            "page:1:block:001",
            "page:2:block:001",
            "page:3:block:001",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW CO2 is named across all four cited blocks as the volatile species at issue, and the formula is the name.",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002",
            "page:6:block:001",
            "page:7:block:012"
          ]
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The solubility sentence has CO2 nucleating a gas phase, which covers the name and the fluid-phase kind.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The volatiles sentence and the LAB sentence both name H2O beside CO2; the text layer splits the digit off, but a reader sees the species.",
          "source_locators": [
            "page:1:block:001",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks discuss magma and magmatic systems, covering the name and the melt kind.",
          "source_locators": [
            "page:4:block:003",
            "page:5:block:002"
          ]
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Melt is named as the material derived from the mantle and again as the ascending phase in the Fig. 6 interpretation.",
          "source_locators": [
            "page:1:block:002",
            "page:7:block:010",
            "page:7:block:012"
          ]
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW MORB is named in the compilation paragraphs and in the proxy sentence, covering name and rock kind.",
          "source_locators": [
            "page:5:block:004",
            "page:8:block:005",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks refer to mylonite shear zones, covering the name and the rock kind.",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:003"
          ]
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Olivine appears as the host of the melt inclusions and as the Fo90 composition used in the calculation.",
          "source_locators": [
            "page:5:block:004",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Peridotite is named on the seafloor, in the sub-solidus sentence and in the crust-free lithosphere sentence.",
          "source_locators": [
            "page:1:block:006",
            "page:2:block:001",
            "page:6:block:001",
            "page:7:block:010"
          ]
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The NTD1 origin sentence names pillow basalts on the seafloor.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Three cited blocks refer to the primary melt or primary melts as the object of the CO2 estimate.",
          "source_locators": [
            "page:1:block:001",
            "page:6:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Rb appears in the same trace-element and proxy sentences as Ba, covering name and element kind.",
          "source_locators": [
            "page:5:block:004",
            "page:6:block:005",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The magmatic-tectonic paragraph names Askja Volcano in Iceland.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The alignment sentence names the main axial normal faults that the deep events run parallel to.",
          "source_locators": [
            "page:4:block:003"
          ]
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The axial valley is named in the detachment-inactivity sentence and again in the Fig. 3 panel labels.",
          "source_locators": [
            "page:2:block:005",
            "page:4:block:004"
          ]
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The abstract and the introduction name the brittle-ductile boundary and its abbreviation, and the Fig. 6 caption treats it as an interface.",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:004",
            "page:7:block:010",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The study-area sentence names the Chain TF as one bound of the segment, and TF is the paper's own abbreviation for transform fault.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 36,
          "source_support": "PARTIAL",
          "rationale": "NO_SUBJECT_IN_ROW The caption puts the corrugated surface on the OCC and the panel legend repeats the term, so the name holds; what the cited prose will not carry is the row's classification of that surface as itself an oceanic core complex.",
          "source_locators": [
            "page:4:block:003",
            "page:4:block:006"
          ]
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited blocks treat the crust as the layer above the mantle and give its thickness.",
          "source_locators": [
            "page:2:block:006",
            "page:7:block:010",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The RTI sentence names the westward dipping detachment fault that bounds the segment.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The opening sentence of the study places the work in the equatorial Atlantic Ocean.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The magmatic-tectonic paragraph names the Fagradalsfjall Peninsula in Iceland.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 41,
          "source_support": "PARTIAL",
          "rationale": "NO_SUBJECT_IN_ROW The NTD1 sentence gives both strike directions the row carries, but it calls them faults without qualifying them as normal faults, so the row's fault kind runs past the cited prose.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The NTD2 sentence names normal faults with exactly the two strikes the row carries.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The OCC sentence names normal faults with the two strikes the row carries.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 44,
          "source_support": "PARTIAL",
          "rationale": "NO_SUBJECT_IN_ROW The cited sentence gives the NNW-SSE orientation and the inward dipping description, but it never calls these faults normal faults, so that field is unsupported.",
          "source_locators": [
            "page:4:block:001"
          ]
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The Fig. 1 legend lists a fracture zone among the mapped features, and here name and kind are the same term, so the thin legend basis still covers what the row asserts.",
          "source_locators": [
            "page:3:block:003"
          ]
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The ultraslow-ridge sentence names the Gakkel Ridge as a spreading ridge.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 47,
          "source_support": "PARTIAL",
          "rationale": "NO_SUBJECT_IN_ROW The panel legend lists Hummocky as its own map symbol alongside Volcanoes, so the name holds while the row's volcanic-cone kind does not follow from the cited block.",
          "source_locators": [
            "page:4:block:004"
          ]
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The Fig. 1 caption describes an inactive hydrothermal mound and the Fig. 3 legend repeats the label.",
          "source_locators": [
            "page:2:block:007",
            "page:4:block:004"
          ]
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The LAB paragraph names the young Juan de Fuca plate.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The maximum-depth compilation names the Knipovich Ridge.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The abstract and the Keller sentence both name the lithosphere-asthenosphere boundary and its abbreviation.",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010"
          ]
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cold-edge sentence names the lithosphere and gives its age.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The compilation sentence names the Logachev Seamount.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The abstract places the deep earthquakes in the mantle and the Fig. 6 labels list it beside the crust.",
          "source_locators": [
            "page:1:block:001",
            "page:7:block:010"
          ]
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The Fig. 1 caption spells the abbreviation out and three further blocks name the ridge.",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:005",
            "page:2:block:007",
            "page:8:block:002"
          ]
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The study-area sentence names the MAR segment between the two transform faults and the Fig. 5 caption refers to it again.",
          "source_locators": [
            "page:1:block:005",
            "page:6:block:005"
          ]
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The magmatic-tectonic paragraph names Mayotte Island.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The RC2 description puts a 10-km-wide median valley on that ridge segment, which is the segment's axial valley.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The Fig. 6 labels and caption name the Moho and treat it as an interface.",
          "source_locators": [
            "page:7:block:010",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The RC2 sentence names an N154 degrees E oriented neo-volcanic ridge, matching the row's name and orientation.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The subdivision sentence names NTD1 as the first non-transform discontinuity and the description block gives the N76 degrees E orientation.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ]
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The subdivision sentence names NTD2, the description block gives the N110 degrees E orientation, and two further blocks label it.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001",
            "page:4:block:005",
            "page:7:block:010"
          ]
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The RTI sentence and the Fig. 1 caption both spell out the oceanic core complex and its abbreviation.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007",
            "page:7:block:010"
          ]
        },
        {
          "row_index": 64,
          "source_support": "PARTIAL",
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks use the term OCC termination, so the name holds; neither supports treating the termination itself as an oceanic core complex.",
          "source_locators": [
            "page:2:block:005",
            "page:4:block:003"
          ]
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The compilation paragraph names the Rainbow massif and places it at a non-transform discontinuity.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The subdivision sentence names RC1 as one of the four ridge subsections.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The subdivision sentence calls RC2 a short ridge segment and the Fig. 6 labels name it again.",
          "source_locators": [
            "page:1:block:005",
            "page:7:block:010"
          ]
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Two cited blocks name RC3 as the ridge segment south of NTD2 and give its orientation of about N165 degrees E.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ]
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Five cited blocks name the Romanche TF or the Romanche transform.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007",
            "page:5:block:005",
            "page:6:block:003",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 70,
          "source_support": "PARTIAL",
          "rationale": "NO_SUBJECT_IN_ROW The Fig. 1 legend lists the Romanche transform valley, so the name holds, but a transform valley is not the ridge's axial valley and the block gives no ground for the row's kind.",
          "source_locators": [
            "page:3:block:003"
          ]
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The study-area sentence spells out the ridge-transform intersection and its abbreviation.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The Fig. 1 legend lists a suspended valley, and the row's name and kind are that same term.",
          "source_locators": [
            "page:3:block:003"
          ]
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cold-lithosphere sentence spells out the Southwest Indian Ridge and its abbreviation.",
          "source_locators": [
            "page:3:block:001",
            "page:5:block:009"
          ]
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The compilation sentence names the SWIR oblique Supersegment among the ridge sites whose depths were updated.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same compilation sentence names SWIR segment 8.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The Fig. 1 legend lists a transverse ridge, and name and kind coincide.",
          "source_locators": [
            "page:3:block:003"
          ]
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The hydrothermal-cooling paragraph reports an extinct hydrothermal vent field on the NTD1 flank, which covers the name and the inactive status; the text layer runs vent and field together.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The magmatic-origin sentence and the Fig. 3 caption both name volcanic cones.",
          "source_locators": [
            "page:3:block:001",
            "page:4:block:007"
          ]
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The magmatic-tectonic paragraph places Mayotte in the western Indian Ocean.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relocation sentence has hypoDD carrying out the double-difference relocations, which is what the pairing asserts, and the same block formalises the program endpoint.",
          "source_locators": [
            "page:7:block:006"
          ]
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The location paragraph attributes the oct-tree search algorithm to NonLinLoc and formalises both endpoints.",
          "source_locators": [
            "page:7:block:004"
          ]
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The detection sentence places the trigger algorithm inside the SEISAN package and formalises SEISAN in the same block.",
          "source_locators": [
            "page:6:block:002"
          ]
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The OCC sentence has the normal faults cutting the complex's surface, and it is the block that formalises the fault endpoint.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The compilation sentence names the Logachev Seamount as belonging to the Knipovich Ridge and formalises both endpoints.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The study-area sentence places the MAR segment between the Romanche and Chain transform faults, which carries the Chain bound, and it formalises both endpoints.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The same sentence carries the Romanche bound of the segment and formalises both endpoints.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The Fig. 1 caption puts the oceanic core complex on the outside corner of the MAR, and that block formalises both endpoints.",
          "source_locators": [
            "page:2:block:007"
          ]
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The RTI sentence has the segment bounded to the east by the detachment fault and formalises both endpoints.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The RC2 description places the segment immediately south of NTD1, which is what adjacency asserts, and that block formalises the NTD1 endpoint.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The cited sentence has RC2 bounded by the inward dipping faults and formalises the fault endpoint.",
          "source_locators": [
            "page:4:block:001"
          ]
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The naming sentence places RC3 immediately south of NTD2 and formalises both endpoints.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The hydrothermal paragraph puts the extinct vent field on the eastern flank of NTD1 and formalises the vent-field endpoint.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence is a statement about what Model 1 does to the event depths, so the record is about the model it names.",
          "source_locators": [
            "page:7:block:009"
          ]
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence is a judgement on Model 5 itself, naming it the best-fitting model.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence states the authors' preference for Model 5, so the model is what the claim is about.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The claim characterises the geochemical behaviour of CO2, which is the subject the row shows.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence characterises seafloor basalts as degassed, and basalt is the subject.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence describes the orientation of the deep events beneath the RC2 axis, so the segment is the locus the claim characterises.",
          "source_locators": [
            "page:4:block:003"
          ]
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence is a verdict on the deep events beneath the RC2 ridge axis, which the block names.",
          "source_locators": [
            "page:8:block:001"
          ]
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The mechanism sentence puts the triggered earthquakes in the mantle, which is the subject the record carries.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence is about the deep microseismicity beneath RC2 and marks the explanation as the authors' preferred one, which matches the row's disposition.",
          "source_locators": [
            "page:5:block:002"
          ]
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The Fig. 1 caption is about the inactive hydrothermal mound the record takes as its subject.",
          "source_locators": [
            "page:2:block:007"
          ]
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence is a negative observation about the RC2 axis.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence denies a current eruption in the axial valley, which is the subject.",
          "source_locators": [
            "page:4:block:003"
          ]
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence explains the shallow earthquakes beneath the OCC dome, so the complex is what the claim is about.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The compilation sentence is about the Rainbow massif and its setting.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence characterises the RTI segment, which the row shows under its RC1 name and its RTI segment tag.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence reports normal Vp/Vs ratios for segment RC2.",
          "source_locators": [
            "page:7:block:003"
          ]
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The enrichment sentence puts Ba above 89 ppm in the RC2 samples, matching value, unit and open lower bound.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The solubility sentence gives an 80 to 90 per cent loss for CO2 on saturation, matching the range, the unit and the hypothesised modality.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The abstract gives about 0.4 to 3.0 wt% CO2 in the primary melts, matching bounds, unit, approximation and calculated status.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same enrichment sentence puts Rb above 8 ppm, matching the row's bound and unit.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The LAB paragraph gives about 1250 degrees C as the sub-solidus temperature for anhydrous peridotites.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The NTD2 sentence puts the BDB at about 10 km, matching value and unit.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cold-lithosphere explanation puts the BDB at about 20 km under that hypothesis, and the row records it as hypothesised.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The introduction ties the maximum earthquake depth to the 700 plus or minus 100 degrees C isotherms, matching value, uncertainty and unit.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The off-axis sentence keeps the BDB shallower than 10 km, matching the open upper bound.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods result gives CO2 from Ba as 0.7 to 4.6 wt% for RC2, matching bounds, unit and estimated status.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same paragraph gives CO2 from Ba as 0.06 to 0.8 wt% for RC3.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The primary-melt result gives CO2 from Ba90 as 0.4 to 3.0 wt% for RC2.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives CO2 from Ba90 as 0.04 to 0.5 wt% for RC3.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The results paragraph gives calculated CO2 of 0.4 to 3.0 wt% for melts along RC2.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives 0.04 to 0.7 wt% for RC3.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods conclusion sets a floor of 0.4 wt% CO2 in the primary melts along RC2, matching the open lower bound.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods result gives CO2 from Rb as 0.9 to 4.3 wt% for RC2.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same paragraph gives CO2 from Rb as 0.07 to 1.0 wt% for RC3.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The primary-melt sentence gives CO2 from Rb90 as 0.5 to 2.8 wt% for RC2.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives CO2 from Rb90 as 0.05 to 0.7 wt% for RC3.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 129,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cold-edge sentence gives the lithosphere an age of 45 Ma.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 130,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The acquisition sentence gives 120 km of MAR axis covered.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 131,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives 140 km of the eastern Romanche TF covered.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 132,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The refraction sentence gives the western-flank crust a thickness of 5.4 plus or minus 0.3 km.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 133,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The observation sentence puts the deep earthquakes beneath the RC2 axis at 16 to 19 km.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 134,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The key-observations sentence puts the deep microseismicity beneath the RC2 ridge axis at about 10 to 20 km.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 135,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The degassing sentence puts the produced earthquakes between 10 and 20 km in the mantle, and the row keeps it hypothesised.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 136,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The depth sentence caps the events beneath NTD2 below 10 km.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 137,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence caps the events beneath the OCC below 6 km.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 138,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The equatorial-Atlantic sentence gives an average of about 2800 ppm CO2 at several segments.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 139,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The relocation result counts 317 events along the MAR.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 140,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence counts 197 events along the Romanche TF.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 141,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The Fig. 6 caption ties the BDB to the 750 degrees C isotherm.",
          "source_locators": [
            "page:7:block:011"
          ]
        },
        {
          "row_index": 142,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same caption gives the crust beneath RC2 a thickness of about 5.4 plus or minus 0.3 km.",
          "source_locators": [
            "page:7:block:011"
          ]
        },
        {
          "row_index": 143,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The Fig. 6 interpretation gives the deep earthquakes beneath the MAR axis as 10 to 19 km below the seafloor.",
          "source_locators": [
            "page:7:block:012"
          ]
        },
        {
          "row_index": 144,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The validation sentence counts 45 events in the subset built for the deep locations beneath RC2.",
          "source_locators": [
            "page:7:block:010"
          ]
        },
        {
          "row_index": 145,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The RC2 discussion puts these earthquakes in a mantle hotter than 1100 degrees C.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 146,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The LAB paragraph gives about 1.1 per cent melt required at the base of the boundary, and the row keeps it modelled and hypothesised.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 147,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The study-area sentence gives the MAR a half-spreading rate of 16 mm/yr.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 148,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the segment a length of about 200 km.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 149,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The magmatic-tectonic sentence gives depths greater than 30 km offshore Mayotte.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 150,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The RC2 description gives the median valley a width of 10 km.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 151,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The LAB paragraph reads the 10 to 20 km microseismicity as ascending melt residing in the mantle at those depths.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 152,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The thermal-modelling sentence gives 1100 to 1200 degrees C at 10 to 20 km depth and the row records it as modelled.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 153,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The sentence denies earthquakes deeper than 20 km beneath the RC2 axis, matching the negated modality and the bound.",
          "source_locators": [
            "page:5:block:007"
          ]
        },
        {
          "row_index": 154,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The key-observations sentence gives 4 to 10 km for the events beneath the southern NTD2.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 155,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The NTD1 sentence gives a length of about 35 km.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 156,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The NTD2 sentence takes the earthquakes down to about 10 km.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 157,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The NTD2 sentence gives a ridge offset of about 33 km.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 158,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The cluster sentence gives focal depths of about 2 to 6 km on the western side of the axial valley.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 159,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The off-axis sentence takes the shallow microseismicity west of the RC2 axis down to 6 km.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 160,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The fractionation sentence gives pre-eruptive CO2 of 0.7 to 4.6 wt% for RC2.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 161,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The RC2 description gives the segment a length of about 22 km.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 162,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The RC3 sentence gives a length of 50 km.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 163,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The key-observations sentence gives 0 to 6 km for the shallow earthquakes at the RTI outside corner.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 164,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The comparison sentence gives 1.9 wt% as the highest CO2 previously reported at the SWIR.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 165,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The refraction sentence gives the western-flank crust an age of 8 Ma.",
          "source_locators": [
            "page:2:block:006"
          ]
        }
      ]
    }
  ],
  "ratification": {
    "evaluator_kind": "HUMAN_AUTHOR",
    "actor_id": "actor:luis",
    "disposition": "RATIFIED_AS_RECORDED",
    "completed_at": "2026-09-06T20:56:46Z",
    "notes": "Ratified as recorded. Decided by Luis in chat on 2026-09-06 (\"5 ratify, yes\") after the overseer's progress reports of 13:15Z and 20:5xZ presented every cell's responsiveness labels, support counts and PARTIAL rows; recorded by the overseer session at his instruction. Run-20 is the cell of record by the same ruling."
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
