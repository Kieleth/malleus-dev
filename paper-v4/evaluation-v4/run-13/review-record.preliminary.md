# Malleus paper v4 run-13 source-grounded review record

Template. The row counts are substituted at freeze, from the frozen cell's own
query result, at the same time as `paper-v4/evaluation-v4/review-task-v4.template.md`.
No placeholder may survive instantiation.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

Fill one `rows` entry per returned row, in order, zero-based: 63 for
CQ-01, 127 for CQ-02, 176 for CQ-03, 149 for
CQ-04, 515 in all. Cite reading block ids only. Write the reasons in
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
    "review_input_manifest_sha256": "sha256:920bf083a0a4b5070452de282a118d83ad4a048fee290ed221720ecb94040f49"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-preliminary-run-13",
    "completed_at": "2026-09-05T14:31:18Z"
  },
  "questions": [
    {
      "question_id": "CQ-01",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "The rows name the campaign that acquired the microseismicity data, carry the instrument network as a record of its own, and give the deployed instrument count with a scope that says it is the deployed network, so each requested part of the question is addressed by rows rather than left to inference. Further counted rows separate the usable instruments and the detection thresholds from the deployment figure, so the several numbers present do not compete for the same slot. Many other rows return organisations, software and methods that the question did not ask for; that is over-return within the question's type sets and does not stop the requested parts from being answered.",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the cruise, so the campaign identity holds, but the roughly three weeks it gives is the continuous recording period of the seismic data, not the length of the cruise, and the row carries no qualifier marking that difference."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:008"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The data-availability block names the cruise reports as an available resource and prints the same fleet campaign address the row carries as its access locator."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The sample-compilation block names the PetDB database and prints the same web address the row carries."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:008",
            "page:8:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The deposit sentence names the Zenodo database and its identifier runs across the two cited blocks, which together give the digits the row records as the DOI."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block introduces the ocean-bottom seismometers by the abbreviation the row uses as the instrument name."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block names Global Mapper, which is the only field this row projects."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block names the GMT 6 toolbox, matching the name this row projects."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The focal-mechanism block names the HASH package as the tool used, matching the row's name."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The relocation block names the hypoDD program as the tool used, matching the row's name."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The earthquake-location block names the NonLinLoc program, matching the row's name."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The seismic-data block names the SEISAN package as the environment the trigger ran in, matching the row's name."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The velocity-model evaluation block names the VELEST program, matching the row's name."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The magnitude block names the ZMAP software as the tool used for the catalogue statistics, matching the row's name."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block says the hypocenters were relocated with a double-difference location method, which is the method name the row carries."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The magnitude block says magnitudes were determined with the local magnitude scale, which is the method name the row carries."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block says hypocenters were obtained with a non-linear earthquake location algorithm, which is the method name the row carries."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The earthquake-location block names the non-linear oct-tree search algorithm used for the initial hypocenters."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block names the short-term-average over long-term-average trigger used for automatic arrival detection."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The Vp/Vs block names Wadati diagrams as the technique that yielded the ratio, matching the row's name."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The degassing-depth block names the CO2 solubility model used to derive the saturation pressure, matching the row's name."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The solubility calculation block attributes the model to Iacono-Marziano and colleagues, matching the row's name."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The discussion block names thermal modelling as the source of the mantle temperature estimate, matching the row's name."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block says a refraction profile was used to find the best one-dimensional velocity model, which is the model the row names."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The depth-resolution block labels the fastest velocity model as Model 1, matching the row's name."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The velocity-model block labels the selected best-fitting model as Model 5, matching the row's name."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:044"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The funding block lists the Regional Council of Brittany among the funders, giving the organisation name the row carries."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The affiliation block lists the Italian institute of environmental geology and geoengineering under the name the row carries."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:044"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The funding block names the European Research Council among the funders, giving the organisation name the row carries."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The affiliation block lists the Geo-Ocean joint research unit under the name and unit number the row carries."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The affiliation block lists the Paris geophysics institute under the name the row carries."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:044"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The funding block names the ISblue project as a funder, giving the name the row carries."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:044"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The funding block names the Chinese national science foundation as a funder, giving the name the row carries."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The affiliation block lists the Second Institute of Oceanography under the name the row carries."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:11:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The publisher note names Springer Nature, giving the organisation name the row carries."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:044"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The funding block names the French oceanographic fleet infrastructure under the name the row carries."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The affiliation block lists the University of Modena under the name the row carries."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The affiliation block lists Universite Paris Cite under the name the row carries."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block names Global Mapper and prints the same address the row carries as its access locator."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010",
            "page:8:block:011"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block names the GMT 6 toolbox and its address runs across the two cited blocks, which together give the locator the row carries."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The focal-mechanism block names the HASH package and the code-availability block gives the same version number and address the row carries."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The relocation block names the hypoDD program and the code-availability block gives the same version number and address the row carries."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The location block names NonLinLoc and the code-availability block gives the same address the row carries."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The seismic-data block names the SEISAN package and the code-availability block gives the same address the row carries."
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The evaluation block names VELEST and the code-availability block gives the same address the row carries."
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The magnitude block names ZMAP and the code-availability block gives the same repository address the row carries."
        },
        {
          "row_index": 45,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:10:block:044",
            "page:2:block:002"
          ],
          "rationale": "DERIVATION_LOCAL The funding block names both endpoints in one funding sentence, and that block is also one the target organisation is formalized from. The block supports funding of the cruise's ship time specifically, while the row asserts an unqualified funding relation to the campaign and projects no slot for that narrower scope."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006"
          ],
          "rationale": "DERIVATION_LOCAL The relocation block names the double-difference relocations and the program that produced them, so the use relation and both endpoint names rest on the same sentence, which is also a block each endpoint is formalized from."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004"
          ],
          "rationale": "DERIVATION_LOCAL The location block describes the oct-tree search as belonging to the named program, which supports the part-of relation, and the same block formalizes both endpoints."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL The relocation block carries the use relation and both endpoint names, and the code-availability block supplies the version and address this row projects on the target."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL The location block carries the part-of relation and both endpoint names, and the code-availability block supplies the address this row projects on the target."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states the minimum number of seismometers that had to record an event for it to be kept, which is the threshold and lower bound the row carries, and the subject is the instrument network that sentence is about."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK Both cited blocks state that the deployed network held nineteen seismometers, which is the count and the scope the row carries, and the network is the subject of those sentences."
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The relocation block states how many instruments each relocated event was recorded on, giving the lower bound the row carries, and the sentence is about the instrument network."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The results block states how many of the seismometers were usable for automatic detection, which is the count and scope the row carries, about the same instrument network."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The velocity-model block states how many one-dimensional models were built, which is the count and scope the row carries, and the subject is the velocity model the study went on to select."
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK Same record as the counted-observation row above: the methods block gives the detection threshold and its lower bound, and the sentence is about the instrument network."
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK This projection drops the count, so what remains to check is the located sentence and the subject; the results block carries the deployment sentence the record points to and it is about the instrument network."
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The focal-mechanism block gives the instrument spacing that limits the solutions, matching the length, unit and approximate qualification the row carries, about the same network."
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK Same record as the counted-observation row above: the relocation block gives the lower bound on recording instruments per event, about the instrument network."
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK This projection drops the count, leaving the located sentence and the subject; the results block carries the usable-instrument sentence the record points to and it is about the network."
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK This projection drops the count, leaving the located sentence and the subject; the velocity-model block carries the model-construction sentence and it is about the velocity model."
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK Same record again under the seismic-observation case: the methods block gives the detection threshold and its lower bound, about the instrument network."
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK Same record again under the seismic-observation case: the relocation block gives the lower bound on recording instruments per event, about the instrument network."
        }
      ]
    },
    {
      "question_id": "CQ-02",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "The rows name the ridge subsection the deep microseismicity belongs to, carry it as a record with its magmatic character, and give its depth interval twice, once from the key observations and once from the deeper interval reported in the discussion, each scoped to the events beneath that segment's ridge axis. The position relative to the axis is carried explicitly: rows place the deep events beneath the axis, place shallower seismicity off axis to the west, and record the direction the deep events line up along relative to the axial faults. Both requested parts are therefore addressed by rows rather than left to inference. Rows for neighbouring segments, other ridges and melt chemistry are over-return within the question's type sets and do not obscure the named subsection.",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:004",
        "page:2:block:006",
        "page:4:block:003"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The study-area block names the Chain transform as one of the two faults bounding the ridge stretch, and the introduction block establishes that the abbreviation stands for a transform fault, which is the fault kind the row carries."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The study-area block says a west-dipping detachment fault bounds the intersection segment on its eastern side, giving both the name and the detachment kind the row carries."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The tectonic block says the core complex surface is cut by normal faults of two strikes, giving the name and the normal kind the row carries."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says the segment is bounded by high-angle inward dipping faults, which is the feature this row names."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:005",
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure block names the Romanche transform as one of the two profile lines, and the introduction block establishes the abbreviation as a transform fault, which is the fault kind the row carries."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The study-area block enumerates the four subsections and names the first non-transform discontinuity with the label the row carries."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The same enumeration names the second non-transform discontinuity with the label the row carries."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The study-area block introduces the oceanic core complex under the abbreviation the row uses as its name."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The study-area block names the ridge segment between the two transforms, which is the feature this row names."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The study-area block gives the intersection segment its label and, in the following sentence, calls it amagmatic, which is the segment character the row carries."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The study-area block gives the short ridge segment its label and the discussion block says the morphology indicates a magmatic origin for it, which is the segment character the row carries."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The study-area block names the segment south of the second discontinuity and the tectonic block calls it a magmatic segment, giving both fields the row carries."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The study-area block introduces the ridge-transform intersection under the abbreviation the row uses as its name."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The discussion block names the Gakkel Ridge as an example of an ultraslow-spreading ridge, giving both the name and the spreading class the row carries."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The depth-compilation block names the Knipovich Ridge among the sites whose data were updated, which is the only field this row projects."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The study-area block names the Mid-Atlantic Ridge in full as the setting of the study, matching the row's name."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The discussion block names the Southwest Indian Ridge by its abbreviation as an example of an ultraslow-spreading ridge, giving both fields the row carries."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The introduction block defines the brittle-ductile boundary and gives the abbreviation the row uses as the name, which is also what the boundary kind restates."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure block names the isotherm the dashed line marks, at the temperature the row carries, and an isotherm is what the boundary kind restates."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The discussion block introduces the lithosphere-asthenosphere boundary with the abbreviation the row uses as the name, which the boundary kind restates."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure block names the expected crust-mantle interface by the short name the row carries, which the boundary kind restates."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL One sentence carries both endpoints and places the faults on the core complex surface, which supports the containment relation, and that block is also one the source fault is formalized from."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007",
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_NON_LOCAL The figure block states that the core complex sits on the outside corner of the ridge, which supports the containment relation, but both endpoints are formalized from the study-area block instead, so the relation's block is not among theirs. Support is unaffected: the sentence names both features and states the placement."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The study-area block says the intersection segment is bounded on the east by the detachment fault, which is the bounding relation, and both endpoints are formalized from that same block."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001",
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The block states the segment is bounded by the inward dipping faults, which is the relation, and it is also the block the target faults are formalized from; the study-area block supplies the source segment's name and character."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The study-area block places the ridge segment between the two named transforms, which supports a bounding relation to the eastern one, and both endpoints are formalized from that block."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The same sentence supports the bounding relation to the western transform, and both endpoints are formalized from that block."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The tectonic block places the short segment immediately south of the first discontinuity, which supports adjacency, and that block is one the source segment is formalized from."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The study-area block names the segment lying south of the second discontinuity, which supports adjacency, and both endpoints are formalized from that block."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:005",
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_NON_LOCAL The methods block calls the southern segment the adjacent one to the studied segment, which supports adjacency, but neither endpoint is formalized from that block, so the relation sits outside its endpoints' blocks. Support is unaffected: the sentence names both segments and states the adjacency."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reasons from missing deep seismicity near the core complex termination to the fault being inactive, which is what the claim records and what its negative modality encodes; the captured span stops one word short of the predicate, but the cited block carries the completion."
        },
        {
          "row_index": 31,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block supports the sentence itself, and the transform's name is in it, but what the sentence is about is the enrichment of the basalts and the low degree of melting of their source; the transform appears only as the place the source lies near, so the record's attribution to the transform as its subject is weakly supported."
        },
        {
          "row_index": 32,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The figure block carries the sentence verbatim and names the transform, but the sentence is about how many segments the schematic shows and uses the transform only as the point they are counted from, so the record is not about the transform in the way the subject slot asserts."
        },
        {
          "row_index": 33,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:4:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The figure block carries the panel description and names the southern discontinuity, but the sentence states what a figure panel contains rather than a property of the discontinuity, so the attribution of the record to that feature as its subject is only partly supported."
        },
        {
          "row_index": 34,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:4:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The figure block carries the sentence and the core complex is named twice in it, but the sentence lists which annotations are drawn on the map and the core complex is one item among faults and a transform trace, so the record is about the figure's markings rather than about the core complex."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The tectonic block states that the core complex surface is cut by normal faults and reads that as recent deformation, which is the claim, and the sentence is about the core complex itself."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the direction the deep earthquakes beneath the segment axis line up along and relates it to the axial normal faults, which is the claim and is a statement about that segment."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The depth-test block concludes that the deep events beneath the segment axis are required by the data and not artifacts, which is the claim and is about that segment."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block presents the degassing explanation for the deep seismicity beneath the segment as the authors' preferred one among several, which supports the claim, its hypothesised modality, the preferred disposition and the paraphrase in the description field."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states that no active vents have been seen on the segment axis, which is the claim and matches its negative modality; the sentence is about that segment."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states that no earthquakes are seen deeper than the stated depth beneath the segment's ridge axis, which is the claim and matches its negative modality."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the authors' suggestion that a small pressure rise from degassing triggers the earthquakes beneath the segment axis, which supports both the claim and its hypothesised modality."
        },
        {
          "row_index": 42,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block carries the caveat verbatim and names the supersegment, but the sentence is about the temporal reach of the microseismicity record; the supersegment is the region that record informs on, so attributing the claim to the supersegment as its subject holds only partly."
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states that tomography finds normal velocity ratios in the segment, which is the claim and is about that segment."
        },
        {
          "row_index": 44,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:3:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The figure block carries the sentence and it does identify the intersection with the profile origin, but what the sentence fixes is a plotting convention rather than a property of the intersection, so the record's subject attribution is only partly supported."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The discussion opening states that the maximum earthquake depth beneath this stretch of the ridge departs from the usual depth-to-spreading-rate relation, which is the claim and is about the ridge."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block contrasts the study segment with the smooth amagmatic morphology of the other ridge, which is the claim and predicates that morphology of the ridge named as subject."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The introduction states that at slow and ultraslow ridges the boundary is defined from the maximum earthquake depth and its corresponding isotherm, which is the claim and is about the boundary."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The figure block states what constrains the boundary drawn in the schematic and which isotherm it corresponds to; although it is a caption, the sentence predicates those properties of the boundary itself."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the expectation that the boundary shallows southward away from the intersection and gives the reason, which is the claim and is about the boundary."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the authors' suggestion that melt at the boundary could come from a combination of the two volatiles, supporting both the claim and its hypothesised modality, and the sentence is about that boundary."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The relocation summary gives the number of events located along the transform, which is the count and the scope the row carries, and the sentence attributes them to that fault."
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the shallow depth limit observed beneath the second discontinuity, matching the upper bound, unit and open-below qualification the row carries, and the sentence is about that discontinuity."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The key-observations block gives the depth interval of the normal-depth earthquakes beneath the southern discontinuity, matching both bounds and the unit the row carries."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block says the earthquakes beneath the second discontinuity reach down to about the depth the row records as its upper bound, and the sentence is about that discontinuity."
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the shallower depth limit beneath the core complex, matching the upper bound, unit and open-below qualification this row carries for that subject."
        },
        {
          "row_index": 56,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:4:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The figure block gives the number of depth-profile transects and says they run along and across the core complex, so the count and its scope are supported, but what is counted is a pair of figure panels rather than a property of the core complex, which weakens the subject attribution."
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The figure block gives the crustal thickness beneath the segment with its stated tolerance, matching the value, uncertainty and unit the row carries, and the sentence is about that segment."
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the depth interval of the deep earthquakes observed beneath the segment axis, matching both bounds and the unit the row carries."
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The key-observations block places the deep microseismicity beneath the segment's ridge axis over the approximate depth interval the row carries, matching both bounds, the unit and the approximate qualification."
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The depth-test block gives the depth interval of the events selected for the fixed-depth test beneath the segment, matching both bounds and the unit the row carries."
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the number of events in that test subset and the cross-section they lie along, matching the count and scope the row carries, and it is a statement about the segment."
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The discussion block gives the depth the off-axis shallow seismicity west of the segment axis reaches down to, matching the upper bound, unit and open-below qualification the row carries."
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The results block gives the number of earthquakes located in the region around the intersection, matching the count and the scope the row carries, and the sentence is about that region."
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The key-observations block gives the depth interval of the shallow earthquakes on the outside corner of the intersection, matching both bounds and the unit the row carries."
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The figure block gives the depth interval of the deep earthquakes beneath the ridge axis, matching both bounds and the unit the row carries, and the ridge is what the sentence is about."
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The abstract gives the depth interval of the reported deep earthquakes along the ridge axis, matching both bounds and the unit the row carries."
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The relocation summary gives the number of events located along the ridge, which is the count and the scope the row carries, and the sentence attributes them to the ridge."
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The results block gives the length of the eastern part of the transform that the network covered, matching the value and unit the row carries."
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK This projection drops the count, leaving the located sentence and the subject; the relocation summary carries the sentence the record points to and attributes the events to the transform."
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the shallow depth limit observed beneath the second discontinuity, matching the upper bound, unit and open-below qualification the row carries, and the sentence is about that discontinuity."
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The key-observations block gives the depth interval of the normal-depth earthquakes beneath the southern discontinuity, matching both bounds and the unit the row carries."
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The tectonic block gives the length of the first discontinuity, matching the approximate value and unit the row carries, and the sentence is about that discontinuity."
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block says the earthquakes beneath the second discontinuity reach down to about the depth the row records as its upper bound, and the sentence is about that discontinuity."
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The tectonic block gives the ridge offset of the second discontinuity, matching the approximate value and unit the row carries."
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the shallower depth limit beneath the core complex, matching the upper bound, unit and open-below qualification this row carries for that subject."
        },
        {
          "row_index": 76,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:4:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK This projection drops the count, leaving the located sentence and the subject; the figure block carries the sentence, but it describes a pair of figure panels rather than a property of the core complex, so the subject attribution holds only partly."
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The geochemistry block gives the barium threshold above which the segment's samples lie, matching the lower bound, unit and open-above qualification the row carries."
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the calculated volatile content of the melts along the segment over the interval the row carries, with the same unit, and marks it as calculated, which matches the modality and the estimated determination."
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the lower calculated interval for the southern segment, matching the bounds and unit this row carries for that subject."
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the estimated pre-eruptive interval for the segment after fractional crystallisation, matching the bounds and unit the row carries and its estimated status."
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states the minimum primary-melt content along the studied segment, matching the lower bound, unit and open-above qualification the row carries."
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the pre-eruptive interval for the segment from the barium proxy, matching the two bounds and unit this row carries for that proxy."
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the barium-derived pre-eruptive interval for the southern segment, matching the bounds and unit this row carries."
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the primary-melt interval for the segment from the fractionation-corrected barium proxy, matching the bounds and unit this row carries."
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the corrected barium-derived primary-melt interval for the southern segment, matching the bounds and unit this row carries."
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the rubidium-derived pre-eruptive interval for the segment, matching the bounds and unit this row carries for that proxy."
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the rubidium-derived pre-eruptive interval for the southern segment, matching the bounds and unit this row carries."
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the primary-melt interval for the segment from the fractionation-corrected rubidium proxy, matching the bounds and unit this row carries."
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the corrected rubidium-derived primary-melt interval for the southern segment, matching the bounds and unit this row carries."
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The figure block gives the crustal thickness beneath the segment with its stated tolerance, matching the value, uncertainty and unit the row carries, and the sentence is about that segment."
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the depth interval of the deep earthquakes observed beneath the segment axis, matching both bounds and the unit the row carries."
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The key-observations block places the deep microseismicity beneath the segment's ridge axis over the approximate depth interval the row carries, matching both bounds, the unit and the approximate qualification."
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The depth-test block gives the depth interval of the events selected for the fixed-depth test beneath the segment, matching both bounds and the unit the row carries."
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK This projection drops the count, leaving the located sentence and the subject; the depth-test block carries the sentence and it is about the segment."
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The discussion block gives the depth the off-axis shallow seismicity west of the segment axis reaches down to, matching the upper bound, unit and open-below qualification the row carries."
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the rubidium threshold above which the segment's samples lie, matching the lower bound, unit and open-above qualification this row carries."
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The tectonic block gives the length of the segment, matching the approximate value and unit the row carries, and the sentence is about that segment."
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The tectonic block gives the length of the southern segment, matching the value and unit the row carries."
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The study-area block gives the length of the ridge segment between the two transforms, matching the approximate value and unit the row carries."
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK This projection drops the count, leaving the located sentence and the subject; the results block carries the sentence and it is about the region around the intersection."
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The key-observations block gives the depth interval of the shallow earthquakes on the outside corner of the intersection, matching both bounds and the unit the row carries."
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The discussion block states the highest melt content previously reported at that ridge and prints the figure, matching the value and unit the row carries, and the sentence is about that ridge."
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The figure block gives the depth interval of the deep earthquakes beneath the ridge axis, matching both bounds and the unit the row carries, and the ridge is what the sentence is about."
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The abstract gives the depth interval of the reported deep earthquakes along the ridge axis, matching both bounds and the unit the row carries."
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The results block gives the length of the ridge axis the network covered, matching the value and unit the row carries."
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK This projection drops the count, leaving the located sentence and the subject; the relocation summary carries the sentence and attributes the events to the ridge."
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The study-area block gives the half-spreading rate of the ridge in the study area, matching the value and unit the row carries."
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The discussion block reads the seismicity beneath the second discontinuity as putting the boundary at about the depth the row records, and the sentence is about the boundary."
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the depth the boundary would have under the cold thick lithosphere explanation, which supports both the value and the hypothesised modality the row carries, since the source frames it as one explanation."
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block states the depth below which the boundary stays off axis, matching the upper bound, unit and open-below qualification the row carries for the boundary."
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The introduction gives the isotherm and tolerance the maximum earthquake depth corresponds to, matching the value, uncertainty and unit the row carries, and it is stated as a property of the boundary."
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the melt fraction proposed as needed at the base of the boundary, matching the approximate value and unit the row carries, and the modelled determination fits its stated provenance."
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the water content ceiling that accompanies that proposal, matching the upper bound, unit and open-below qualification the row carries."
        },
        {
          "row_index": 114,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block carries the temperature and ties it to the boundary, but it attaches that figure to the anhydrous peridotite solidus and places the melt at sub-solidus temperatures, that is below it, whereas the row's quantity description reads the figure as the temperature at which melt is present."
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the shallow depth limit observed beneath the second discontinuity, matching the upper bound, unit and open-below qualification the row carries, and the sentence is about that discontinuity."
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The key-observations block gives the depth interval of the normal-depth earthquakes beneath the southern discontinuity, matching both bounds and the unit the row carries."
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block says the earthquakes beneath the second discontinuity reach down to about the depth the row records as its upper bound, and the sentence is about that discontinuity."
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the shallower depth limit beneath the core complex, matching the upper bound, unit and open-below qualification this row carries for that subject."
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The figure block gives the crustal thickness beneath the segment with its stated tolerance, matching the value, uncertainty and unit the row carries, and the sentence is about that segment."
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the depth interval of the deep earthquakes observed beneath the segment axis, matching both bounds and the unit the row carries."
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The key-observations block places the deep microseismicity beneath the segment's ridge axis over the approximate depth interval the row carries, matching both bounds, the unit and the approximate qualification."
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The depth-test block gives the depth interval of the events selected for the fixed-depth test beneath the segment, matching both bounds and the unit the row carries."
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The discussion block gives the depth the off-axis shallow seismicity west of the segment axis reaches down to, matching the upper bound, unit and open-below qualification the row carries."
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The key-observations block gives the depth interval of the shallow earthquakes on the outside corner of the intersection, matching both bounds and the unit the row carries."
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The figure block gives the depth interval of the deep earthquakes beneath the ridge axis and marks the depths as measured from the sea floor, which supports the bounds, the unit and the depth reference this row adds."
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The abstract gives the depth interval of the reported deep earthquakes along the ridge axis, matching both bounds and the unit the row carries."
        }
      ]
    },
    {
      "question_id": "CQ-03",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "Rows carry the depth of the deep earthquakes beneath the central magmatic segment as a bounded interval in kilometres, with the observation marked measured, and they carry the calculated CO2 range for the primary melts of that same segment in weight per cent, marked calculated and estimated and labelled with the element the estimate rests on. Unit, bound qualification and estimate status sit on the same row as the values, and the segment is identified through a typed subject reference whose name and character are themselves supported, so every part the question asks for is addressed. Two qualifications: the narrowing to primary rather than pre-eruptive melts is carried in a free-text quantity description rather than a typed link, and the answer-bearing rows sit among many rows on unrelated matters. Both are precision costs, not gaps in coverage.",
      "source_locators": [
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
          "source_locators": [
            "page:8:block:008"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The data-availability block that carries both projected values names the cruise reports and gives the campaign website address."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:005",
            "page:8:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block naming the PetDB database also gives its web address, so the name and the access locator both hold."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:008",
            "page:8:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The data-availability block names the Zenodo deposit and the deposit identifier runs across it and the block that follows; read together they give the identifier as projected."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block on the segment descriptions records basalts observed on the sea floor, which carries the projected name."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block compiling the geochemical analyses introduces mid-ocean ridge basalts under this abbreviation."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block setting out the shear-zone explanation names mylonite shear zones in the mantle, which carries the projected name."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The introduction block reports peridotites observed on the sea floor, which carries the projected name."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block stating the authors' preferred explanation names ascending melt, which carries the projected name."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block that estimates CO2 for the two segments names pre-eruptive melts and separates them from melts in equilibrium with the mantle source, which carries the name and the stage."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block on the corrected element concentrations names primary melts and describes them as being in equilibrium with the mantle source, which carries the name and the stage."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block stating the authors' preferred explanation names ascending melt, which carries the projected name."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block that estimates CO2 for the two segments names pre-eruptive melts and separates them from melts in equilibrium with the mantle source, which carries the name and the stage."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block on the corrected element concentrations names primary melts and describes them as being in equilibrium with the mantle source, which carries the name and the stage."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:7:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block states that the hypocenters were relocated by a double-difference location method, which is the projected name."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The magnitude block states that magnitudes were determined on the local magnitude scale, the projected name."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block states that a non-linear earthquake location algorithm produced the hypocenters, the projected name."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The earthquake-location block names the non-linear oct-tree search algorithm used for the initial hypocenters."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block names the short-term-average over long-term-average trigger used for automatic detection."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block attributes the velocity-ratio estimate to Wadati diagrams, the projected name."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The discussion block applies a CO2 solubility model to the melt, which carries the projected name."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block names the Iacono-Marziano model used for the theoretical solubility calculation."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:7:block:012"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The discussion block attributes the temperature estimate beneath the segment axis to thermal modelling, which carries the projected name."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block names the one-dimensional velocity model chosen for the travel-time calculation, which carries the projected name."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The depth-resolution block identifies the fastest of the tested models by this label, which is the projected name."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block identifies the selected average velocity model by this label, which is the projected name."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The discussion block applies a CO2 solubility model to the melt, which carries the projected name."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block names the Iacono-Marziano model used for the theoretical solubility calculation."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:7:block:012"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The discussion block attributes the temperature estimate beneath the segment axis to thermal modelling, which carries the projected name."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block names the one-dimensional velocity model chosen for the travel-time calculation, which carries the projected name."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The depth-resolution block identifies the fastest of the tested models by this label, which is the projected name."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block identifies the selected average velocity model by this label, which is the projected name."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block introducing the global volatile to trace-element trends gives this ratio with its central value and uncertainty; the text layer breaks the formula with a space that a reader closes. The row's projection withholds the record's assertion locator and statement digest, so no digest token can be written here."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The same block gives this ratio with its central value and uncertainty, again with the formula broken by the text layer. The row's projection withholds the record's assertion locator and statement digest, so no digest token can be written here."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block gives the velocity ratio obtained from Wadati diagrams with numerator and denominator as projected. The block hedges the value as approximate and the projection carries no hedge, which does not change what the row claims. The projection also withholds the record's assertion locator and statement digest, so no digest token can be written here."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The introduction block names the ridge segment between the two transforms, which carries the projected name."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The introduction block names the ridge-transform-intersection subsection and calls it amagmatic, which carries both projected values."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001",
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The introduction block names the segment and the discussion block reading its axial morphology calls it magmatic, so name and character both hold."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001",
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The introduction block names the segment south of the second discontinuity and the following block calls it magmatic, so name and character both hold."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block on the segment descriptions records basalts observed on the sea floor, which carries the projected name."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block compiling the geochemical analyses introduces mid-ocean ridge basalts under this abbreviation."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block setting out the shear-zone explanation names mylonite shear zones in the mantle, which carries the projected name."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The introduction block reports peridotites observed on the sea floor, which carries the projected name."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure-caption block listing what is plotted against CO2 names melt inclusions, the projected name."
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The same figure-caption block names the basalt samples along the two segments, the projected name."
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The same figure-caption block names popping rocks among the plotted sample kinds."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first figure's caption block names the rock samples plotted on the bathymetric map, the projected name."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The discussion block applies a CO2 solubility model to the melt, which carries the projected name."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block names the Iacono-Marziano model used for the theoretical solubility calculation."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The background block that defines the brittle-ductile boundary gives both the abbreviation and the boundary kind as projected."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure-caption block identifies the dashed line as an isotherm at the projected temperature, which carries the name and the boundary kind."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The discussion block naming the lithosphere-asthenosphere boundary gives the abbreviation and the boundary kind as projected."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure-caption block names the expected Moho interface, which carries the name and the discontinuity kind."
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The opening background block names the oceanic crust as a layer distinct from the mantle, which carries name and layer kind."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The background block on the brittle-ductile boundary names the lithosphere as the layer above the partially molten material, carrying name and layer kind."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The opening background block names the mantle as the layer the melt derives from, carrying name and layer kind."
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:7:block:012"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The discussion block attributes the temperature estimate beneath the segment axis to thermal modelling, which carries the projected name."
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block names the one-dimensional velocity model chosen for the travel-time calculation, which carries the projected name."
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The depth-resolution block identifies the fastest of the tested models by this label, which is the projected name."
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block identifies the selected average velocity model by this label, which is the projected name."
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:005",
            "page:1:block:005",
            "page:2:block:001",
            "page:3:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL The assertion that formalises the adjacency sits in a methods block on the sample compilation, and neither endpoint draws its name or its character from that block. The adjacency of the two segments is stated there all the same, and the introduction and segment-description blocks cited with it carry the projected names and magmatic characters."
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:005",
            "page:1:block:005",
            "page:3:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The figure-caption block that formalises the sampling relation is also where the sample record takes its name, and it places those basalt samples along the segment. The segment's magmatic character comes from the discussion block cited with it."
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:005",
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The same figure-caption block formalises the relation and names the sample record, placing those samples along the southern segment. That segment's magmatic character comes from the segment-description block cited with it."
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states that the two corrected element concentrations were computed for melts in equilibrium with a magnesian olivine and used to estimate CO2 in primary melts, and it names those melts."
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reads the depth of the microseismicity as evidence that ascending melt sits, fractionates and evolves at those depths; the ascending melt is named there and is what the sentence is about."
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states that the published geochemical analyses of the ridge basalts inside the network footprint were compiled, and it names that material."
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block cites the observation of basalts on the sea floor as further support for a magmatically robust segment, and names the material. The captured statement is a fragment of that sentence and matches the block as captured."
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states that sea-floor basalts are mostly degassed, which is what the record asserts, and it names the material."
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states that the two corrected element concentrations were computed for melts in equilibrium with a magnesian olivine and used to estimate CO2 in primary melts, and it names those melts."
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reads the depth of the microseismicity as evidence that ascending melt sits, fractionates and evolves at those depths; the ascending melt is named there and is what the sentence is about."
        },
        {
          "row_index": 69,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block supports the statement itself: the dashed lines in the schematic carry isotherms taken from a simulated thermal model. The model is named there only as where those lines came from, not as what the sentence is about, so the record's attachment to the thermal model as its subject is only partly supported."
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block describes choosing among the constructed one-dimensional models on located-event count and residual, so both the statement and its attachment to the velocity model hold."
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block compares the selected model against the minimum model and reports the selected one locating more events; the velocity model is what the sentence is about."
        },
        {
          "row_index": 72,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block supports the statement itself: the dashed lines in the schematic carry isotherms taken from a simulated thermal model. The model is named there only as where those lines came from, not as what the sentence is about, so the record's attachment to the thermal model as its subject is only partly supported."
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block describes choosing among the constructed one-dimensional models on located-event count and residual, so both the statement and its attachment to the velocity model hold."
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block compares the selected model against the minimum model and reports the selected one locating more events; the velocity model is what the sentence is about."
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block concludes that the tested ratio setting gives the lowest residuals and the most locations, and the ratio is what the sentence is about."
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block concludes that the tested ratio setting gives the lowest residuals and the most locations, and the ratio is what the sentence is about."
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the orientation of the deep events beneath the segment axis and their parallelism to the axial normal faults; the segment is named and is where the events lie."
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block concludes from the location tests that these deep events below the segment's ridge axis are required by the data rather than artifacts; the segment is named there."
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the fourth and preferred possibility, tying the deep microseismicity beneath the segment to degassing from the ascending melt. The hypothesised modality, the preferred disposition and the projected description all come from that sentence, and the segment is named in it."
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states that no active vents have been observed on the segment axis, which is the negated content the record carries, and it names the segment."
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states that no events are seen below the stated depth beneath the segment ridge axis, matching the negated content, and it names the segment."
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block puts forward the small pressure rise from degassing of the ascending melt as inducing the events beneath the segment axis, which is the hypothesised content, and it names the segment."
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block cautions that the microseismicity record is a brief snapshot and speaks of the processes along this supersegment, which is the subject as named."
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports normal velocity ratios from tomography in the present segment, and names it."
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states that the published geochemical analyses of the ridge basalts inside the network footprint were compiled, and it names that material."
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block cites the observation of basalts on the sea floor as further support for a magmatically robust segment, and names the material. The captured statement is a fragment of that sentence and matches the block as captured."
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states that sea-floor basalts are mostly degassed, which is what the record asserts, and it names the material."
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The background block states how the boundary is defined from the maximum earthquake depth at slow and ultraslow ridges, so the boundary is what the sentence is about and is named in it."
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The figure-caption block says the thick line stands for the boundary constrained by the maximum earthquake depth, so the sentence is about the boundary and names it."
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the expectation that the boundary shallows southward away from the intersection, which is a claim about the boundary and names it."
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block suggests that melt present at the lithosphere-asthenosphere boundary may owe to a combination of the two volatiles; the boundary is named and is where the claim is located."
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The abstract block carries the suggestion that deep mantle earthquakes follow from CO2 degassing and the volume change it produces, and the discussion block cited with it is where the explanation is called the preferred one, which supports the projected disposition. The mantle is named in the abstract block and is where the earthquakes are placed."
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states that the migrating melt keeps degassing and produces earthquakes in the mantle over a depth interval; the mantle is named and is where the claim is located."
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The opening background block states that oceanic crust forms from mantle-derived melt, which is a claim about the crust and names it."
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states that the volume change from degassing, under extensional stress, raises strain rates locally and sets off deep earthquakes within the mantle; the mantle is named and is where the triggering is placed."
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reads the crustal thickness as placing most of these events in the mantle with a few scattered in the crust; the mantle is named and is where the events are placed."
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports a modelled temperature at the relevant depths and concludes the mantle beneath the segment axis is hot; the mantle is named and is the subject of that conclusion."
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states that how these melts reach the surface through the mantle's upper part is not understood; the mantle is named and bounds the claim."
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reads the sea-floor observations as showing exhumed mantle and supporting a tectonic origin for the subsection; the mantle is named and its presence is what the sentence asserts."
        },
        {
          "row_index": 100,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block supports the statement itself: the dashed lines in the schematic carry isotherms taken from a simulated thermal model. The model is named there only as where those lines came from, not as what the sentence is about, so the record's attachment to the thermal model as its subject is only partly supported."
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block describes choosing among the constructed one-dimensional models on located-event count and residual, so both the statement and its attachment to the velocity model hold."
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block compares the selected model against the minimum model and reports the selected one locating more events; the velocity model is what the sentence is about."
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states how many one-dimensional P-wave models were constructed, matching the projected count and its scope; the models are what is counted and are named there."
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states how many one-dimensional P-wave models were constructed, matching the projected count and its scope; the models are what is counted and are named there."
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The figure-caption block gives the crustal thickness beneath the segment with its uncertainty and an approximation marker, matching the projected bounds, unit and qualification; the segment is named and is where the thickness is measured."
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the depth of the deep earthquakes observed beneath the segment axis as an interval, matching the projected bounds and unit; the segment is named and is where the events lie."
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The observations block places the deep microseismicity beneath the segment ridge axis over an approximate depth interval, matching the projected bounds, unit and qualification; the segment is named."
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block describes the depth-test subset and the interval its events span, matching the projected bounds and unit; the segment is named and is where those events lie."
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same methods block gives the size of that subset and the cross-section it was drawn along, matching the projected count and scope; the segment is named."
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the depth reached by the off-axis shallow microseismicity west of the segment axis as an upper bound, matching the projected bound, unit and qualification; the segment is named."
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the thickness of the older crust on the western ridge flank with its uncertainty, matching the projected value and unit; the crust is what is measured and is named."
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states how many one-dimensional P-wave models were constructed, matching the projected count and its scope; the models are what is counted and are named there."
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the barium enrichment of the segment's samples as a lower bound in the projected unit; the segment is named and scopes the measurement."
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the calculated CO2 content of the melts generated along the segment as an interval in the projected unit and marks it calculated; the segment is named."
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the calculated CO2 interval for the southern segment in the projected unit; that segment is named there."
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the estimated pre-eruptive CO2 range for the segment after fractional crystallisation, matching the projected bounds and unit; the segment is named."
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states the minimum CO2 concentration in the primary melts along the segment, matching the projected lower bound, unit and open-bound qualification; the segment is named."
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the barium-based pre-eruptive CO2 range for the segment, matching the projected bounds, unit and estimation basis; the segment is named."
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the barium-based pre-eruptive CO2 range for the southern segment, matching the projected bounds, unit and basis; that segment is named."
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the barium-corrected primary-melt CO2 range for the segment, matching the projected bounds, unit and estimation basis and marking the values estimated; the segment is named."
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the barium-corrected primary-melt range for the southern segment, matching the projected bounds, unit and basis; that segment is named."
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium-based pre-eruptive CO2 range for the segment, matching the projected bounds, unit and basis; the segment is named."
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium-based pre-eruptive range for the southern segment, matching the projected bounds, unit and basis; that segment is named."
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium-corrected primary-melt range for the segment, matching the projected bounds, unit and basis; the segment is named."
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium-corrected primary-melt range for the southern segment, matching the projected bounds, unit and basis; that segment is named."
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium enrichment of the segment's samples as a lower bound in the projected unit; the segment is named and scopes the measurement."
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the water content proposed at the base of the boundary as an upper bound in the projected unit and attributes it to a modelling argument, which supports the modelled determination; the boundary is named."
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states how many one-dimensional P-wave models were constructed, matching the projected count and its scope; the models are what is counted and are named there."
        },
        {
          "row_index": 129,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states how many one-dimensional P-wave models were constructed, matching the projected count and its scope; the models are what is counted and are named there."
        },
        {
          "row_index": 130,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the interval of velocity ratios used in the location tests, matching the projected bounds; the ratio is what the sentence is about and the row claims no unit for it."
        },
        {
          "row_index": 131,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the interval of velocity ratios used in the location tests, matching the projected bounds; the ratio is what the sentence is about and the row claims no unit for it."
        },
        {
          "row_index": 132,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the barium enrichment of the segment's samples as a lower bound in the projected unit; the segment is named and scopes the measurement."
        },
        {
          "row_index": 133,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the calculated CO2 content of the melts generated along the segment as an interval in the projected unit and marks it calculated; the segment is named."
        },
        {
          "row_index": 134,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the calculated CO2 interval for the southern segment in the projected unit; that segment is named there."
        },
        {
          "row_index": 135,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the estimated pre-eruptive CO2 range for the segment after fractional crystallisation, matching the projected bounds and unit; the segment is named."
        },
        {
          "row_index": 136,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states the minimum CO2 concentration in the primary melts along the segment, matching the projected lower bound, unit and open-bound qualification; the segment is named."
        },
        {
          "row_index": 137,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the barium-based pre-eruptive CO2 range for the segment, matching the projected bounds, unit and estimation basis; the segment is named."
        },
        {
          "row_index": 138,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the barium-based pre-eruptive CO2 range for the southern segment, matching the projected bounds, unit and basis; that segment is named."
        },
        {
          "row_index": 139,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the barium-corrected primary-melt CO2 range for the segment, matching the projected bounds, unit and estimation basis and marking the values estimated; the segment is named."
        },
        {
          "row_index": 140,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the barium-corrected primary-melt range for the southern segment, matching the projected bounds, unit and basis; that segment is named."
        },
        {
          "row_index": 141,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium-based pre-eruptive CO2 range for the segment, matching the projected bounds, unit and basis; the segment is named."
        },
        {
          "row_index": 142,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium-based pre-eruptive range for the southern segment, matching the projected bounds, unit and basis; that segment is named."
        },
        {
          "row_index": 143,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium-corrected primary-melt range for the segment, matching the projected bounds, unit and basis; the segment is named."
        },
        {
          "row_index": 144,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium-corrected primary-melt range for the southern segment, matching the projected bounds, unit and basis; that segment is named."
        },
        {
          "row_index": 145,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The figure-caption block gives the crustal thickness beneath the segment with its uncertainty and an approximation marker, matching the projected bounds, unit and qualification; the segment is named and is where the thickness is measured."
        },
        {
          "row_index": 146,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the depth of the deep earthquakes observed beneath the segment axis as an interval, matching the projected bounds and unit; the segment is named and is where the events lie."
        },
        {
          "row_index": 147,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The observations block places the deep microseismicity beneath the segment ridge axis over an approximate depth interval, matching the projected bounds, unit and qualification; the segment is named."
        },
        {
          "row_index": 148,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block describes the depth-test subset and the interval its events span, matching the projected bounds and unit; the segment is named and is where those events lie."
        },
        {
          "row_index": 149,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same methods block gives the size of that subset and the cross-section it was drawn along, matching the projected count and scope; the segment is named."
        },
        {
          "row_index": 150,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the depth reached by the off-axis shallow microseismicity west of the segment axis as an upper bound, matching the projected bound, unit and qualification; the segment is named."
        },
        {
          "row_index": 151,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium enrichment of the segment's samples as a lower bound in the projected unit; the segment is named and scopes the measurement."
        },
        {
          "row_index": 152,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the segment's length with an approximation marker, matching the projected value, unit and qualification, and names the segment."
        },
        {
          "row_index": 153,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the southern segment's length, matching the projected value and unit, and names that segment."
        },
        {
          "row_index": 154,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The introduction block gives the approximate length of the ridge segment between the two transforms, matching the projected value, unit and qualification, and names the segment."
        },
        {
          "row_index": 155,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reads the microseismicity beneath the southern discontinuity as putting the boundary at the projected depth with an approximation marker; the boundary is what the sentence is about and is named."
        },
        {
          "row_index": 156,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block sets out the cold and thick lithosphere explanation, under which the boundary would lie at the projected approximate depth; the hypothesised framing and the boundary as subject both come from that sentence."
        },
        {
          "row_index": 157,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reads the off-axis shallow microseismicity as keeping the boundary above the projected depth, matching the upper bound and its qualification; the boundary is named."
        },
        {
          "row_index": 158,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The background block gives the isotherm the maximum earthquake depth corresponds to, with its uncertainty, matching the projected value and unit; the boundary being defined is named there."
        },
        {
          "row_index": 159,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the melt fraction proposed at the base of the boundary with an approximation marker, matching the projected value, unit and qualification; the boundary is named."
        },
        {
          "row_index": 160,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the water content proposed at the base of the boundary as an upper bound in the projected unit and attributes it to a modelling argument, which supports the modelled determination; the boundary is named."
        },
        {
          "row_index": 161,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the approximate temperature at which melt is present for anhydrous peridotites at the boundary, matching the projected value, unit and qualification; the boundary is named."
        },
        {
          "row_index": 162,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the thickness of the older crust on the western ridge flank with its uncertainty, matching the projected value and unit; the crust is what is measured and is named."
        },
        {
          "row_index": 163,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block places the earthquakes produced by continued degassing in the mantle over the projected depth interval, matching bounds and unit, and names the mantle."
        },
        {
          "row_index": 164,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The background block gives the depth interval at which extensive dry melting begins under mantle upwelling, matching the projected bounds and unit; the mantle is named."
        },
        {
          "row_index": 165,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the age of the cold lithosphere behind the cold-edge effect near the intersection, matching the projected value and unit, and names the lithosphere."
        },
        {
          "row_index": 166,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the lower bound on the temperature of the hot mantle in which these earthquakes occur, matching the projected bound, unit and qualification, and names the mantle."
        },
        {
          "row_index": 167,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the modelled temperature interval at the relevant depths beneath the segment axis, matching the projected bounds, unit and modelled determination, and names the mantle."
        },
        {
          "row_index": 168,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the age below which a magmatically accreted crust counts as young, matching the projected upper bound and unit, and names the crust."
        },
        {
          "row_index": 169,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states how many one-dimensional P-wave models were constructed, matching the projected count and its scope; the models are what is counted and are named there."
        },
        {
          "row_index": 170,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The figure-caption block gives the crustal thickness beneath the segment with its uncertainty and an approximation marker, matching the projected bounds, unit and qualification; the segment is named and is where the thickness is measured."
        },
        {
          "row_index": 171,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the depth of the deep earthquakes observed beneath the segment axis as an interval, matching the projected bounds and unit; the segment is named and is where the events lie."
        },
        {
          "row_index": 172,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The observations block places the deep microseismicity beneath the segment ridge axis over an approximate depth interval, matching the projected bounds, unit and qualification; the segment is named."
        },
        {
          "row_index": 173,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block describes the depth-test subset and the interval its events span, matching the projected bounds and unit; the segment is named and is where those events lie."
        },
        {
          "row_index": 174,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the depth reached by the off-axis shallow microseismicity west of the segment axis as an upper bound, matching the projected bound, unit and qualification; the segment is named."
        },
        {
          "row_index": 175,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the thickness of the older crust on the western ridge flank with its uncertainty, matching the projected value and unit; the crust is what is measured and is named."
        }
      ]
    },
    {
      "question_id": "CQ-04",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "Rows carry the preferred explanation explicitly as a hypothesis and explicitly as preferred, tying the deep microseismicity beneath the central segment to CO2 degassing from ascending melt. Further rows carry the volume change the degassing produces, the extensional stress it acts under, the small pressure rise offered as the immediate trigger, and the triggering of deep earthquakes in the mantle; ascending melt is also present as a record of its own. Every part the question asks for is addressed, and the epistemic status is carried on the rows rather than left to inference. Two qualifications: the chain from degassing through volume change to trigger is spread over separate rows with no link joining them, and the answer-bearing rows sit among many rows on unrelated matters.",
      "source_locators": [
        "page:5:block:002",
        "page:5:block:003",
        "page:1:block:001",
        "page:5:block:009",
        "page:6:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The introduction block names this transform as one of the two bounding the studied ridge portion, carrying the name and the transform kind."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The introduction block names the detachment fault that dips to the west and limits the intersection subsection on its eastern side, carrying name and fault kind."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block describing the core-complex surface names the normal faults cutting it, carrying name and fault kind."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block on the axial valley names the inward dipping faults that bound the segment, which is the projected name."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:1:block:005",
            "page:3:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The blocks cited name this transform and treat it as one of the transform faults bounding the studied ridge, which carries the name and the fault kind."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first figure's caption block names the inactive hydrothermal mound, carrying the name and the inactive status."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block on the maximum-depth compilation names the Rainbow massif, the projected name."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block on hydrothermal cooling names an extinct hydrothermal vent field off the first discontinuity, carrying the name and the extinct status."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block stating the authors' preferred explanation names ascending melt, which carries the projected name."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block that estimates CO2 for the two segments names pre-eruptive melts and separates them from melts in equilibrium with the mantle source, which carries the name and the stage."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block on the corrected element concentrations names primary melts and describes them as being in equilibrium with the mantle source, which carries the name and the stage."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The discussion block applies a CO2 solubility model to the melt, which carries the projected name."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block names the Iacono-Marziano model used for the theoretical solubility calculation."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:7:block:012"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The discussion block attributes the temperature estimate beneath the segment axis to thermal modelling, which carries the projected name."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block names the one-dimensional velocity model chosen for the travel-time calculation, which carries the projected name."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The depth-resolution block identifies the fastest of the tested models by this label, which is the projected name."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block identifies the selected average velocity model by this label, which is the projected name."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The introduction block names the ridge segment between the two transforms, which carries the projected name."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The introduction block names the ridge-transform-intersection subsection and calls it amagmatic, which carries both projected values."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001",
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The introduction block names the segment and the discussion block reading its axial morphology calls it magmatic, so name and character both hold."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001",
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The introduction block names the segment south of the second discontinuity and the following block calls it magmatic, so name and character both hold."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The discussion block applies a CO2 solubility model to the melt, which carries the projected name."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block names the Iacono-Marziano model used for the theoretical solubility calculation."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The background block that defines the brittle-ductile boundary gives both the abbreviation and the boundary kind as projected."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure-caption block identifies the dashed line as an isotherm at the projected temperature, which carries the name and the boundary kind."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The discussion block naming the lithosphere-asthenosphere boundary gives the abbreviation and the boundary kind as projected."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure-caption block names the expected Moho interface, which carries the name and the discontinuity kind."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The opening background block names the oceanic crust as a layer distinct from the mantle, which carries name and layer kind."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The background block on the brittle-ductile boundary names the lithosphere as the layer above the partially molten material, carrying name and layer kind."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The opening background block names the mantle as the layer the melt derives from, carrying name and layer kind."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:7:block:012"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The discussion block attributes the temperature estimate beneath the segment axis to thermal modelling, which carries the projected name."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The results block names the one-dimensional velocity model chosen for the travel-time calculation, which carries the projected name."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The depth-resolution block identifies the fastest of the tested models by this label, which is the projected name."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block identifies the selected average velocity model by this label, which is the projected name."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block setting out the magmatic-tectonic possibility names Askja Volcano, the projected name."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The same block names the Fagradalsfjall Peninsula, the projected name."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block on the depth compilation names the Logachev Seamount, the projected name."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block describing the segment's median valley names the neo-volcanic ridge, the projected name."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The discussion block reading the axial morphology names volcanic cones, the projected name."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL One introduction block formalises the relation and both endpoints. That block calls the intersection subsection amagmatic and gives its eastern limit as a detachment fault dipping to the west, which carries the relation type and both endpoint projections."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001",
            "page:1:block:005",
            "page:3:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The block that formalises the relation is also where the fault record takes its name, and it states that the segment is bounded by inward dipping high-angle faults. The segment's magmatic character comes from the discussion block cited with it."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:1:block:004"
          ],
          "rationale": "DERIVATION_LOCAL The introduction block that formalises the relation also names the ridge segment and the bounding transform, placing the segment between the two transforms. The background block cited with it carries the transform kind."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:1:block:004",
            "page:3:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The same introduction block formalises the relation and names both endpoints, placing the ridge segment between the two transforms. The blocks cited with it carry the transform's name as used elsewhere and its fault kind."
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:005",
            "page:1:block:005",
            "page:2:block:001",
            "page:3:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL The assertion that formalises the adjacency sits in a methods block on the sample compilation, and neither endpoint draws its name or its character from that block. The adjacency of the two segments is stated there all the same, and the introduction and segment-description blocks cited with it carry the projected names and magmatic characters."
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reasons from the absence of deep microseismicity near the core-complex termination to this fault being inactive; the fault is named there and is what the sentence is about. The captured statement stops short of the sentence's last word and matches the block as captured."
        },
        {
          "row_index": 45,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block does state that the enriched basalts and their high volatile contents were read as low-degree melting of an enriched mantle source, so the statement holds. The transform is named there only as the place that source lies near, not as what the sentence is about, so its attachment as the record's subject is only partly supported."
        },
        {
          "row_index": 46,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The figure-caption block does say three segments are drawn southward from the transform, so the statement holds. The transform serves as the direction marker in that sentence rather than as what it is about, so its attachment as the record's subject is only partly supported."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block places the massif at a non-transform discontinuity and says it is plotted for reference; the massif is what the sentence is about and is named in it."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states that the two corrected element concentrations were computed for melts in equilibrium with a magnesian olivine and used to estimate CO2 in primary melts, and it names those melts."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reads the depth of the microseismicity as evidence that ascending melt sits, fractionates and evolves at those depths; the ascending melt is named there and is what the sentence is about."
        },
        {
          "row_index": 50,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block supports the statement itself: the dashed lines in the schematic carry isotherms taken from a simulated thermal model. The model is named there only as where those lines came from, not as what the sentence is about, so the record's attachment to the thermal model as its subject is only partly supported."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block describes choosing among the constructed one-dimensional models on located-event count and residual, so both the statement and its attachment to the velocity model hold."
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block compares the selected model against the minimum model and reports the selected one locating more events; the velocity model is what the sentence is about."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the orientation of the deep events beneath the segment axis and their parallelism to the axial normal faults; the segment is named and is where the events lie."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block concludes from the location tests that these deep events below the segment's ridge axis are required by the data rather than artifacts; the segment is named there."
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the fourth and preferred possibility, tying the deep microseismicity beneath the segment to degassing from the ascending melt. The hypothesised modality, the preferred disposition and the projected description all come from that sentence, and the segment is named in it."
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states that no active vents have been observed on the segment axis, which is the negated content the record carries, and it names the segment."
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states that no events are seen below the stated depth beneath the segment ridge axis, matching the negated content, and it names the segment."
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block puts forward the small pressure rise from degassing of the ascending melt as inducing the events beneath the segment axis, which is the hypothesised content, and it names the segment."
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block cautions that the microseismicity record is a brief snapshot and speaks of the processes along this supersegment, which is the subject as named."
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports normal velocity ratios from tomography in the present segment, and names it."
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The background block states how the boundary is defined from the maximum earthquake depth at slow and ultraslow ridges, so the boundary is what the sentence is about and is named in it."
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The figure-caption block says the thick line stands for the boundary constrained by the maximum earthquake depth, so the sentence is about the boundary and names it."
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the expectation that the boundary shallows southward away from the intersection, which is a claim about the boundary and names it."
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block suggests that melt present at the lithosphere-asthenosphere boundary may owe to a combination of the two volatiles; the boundary is named and is where the claim is located."
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The abstract block carries the suggestion that deep mantle earthquakes follow from CO2 degassing and the volume change it produces, and the discussion block cited with it is where the explanation is called the preferred one, which supports the projected disposition. The mantle is named in the abstract block and is where the earthquakes are placed."
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states that the migrating melt keeps degassing and produces earthquakes in the mantle over a depth interval; the mantle is named and is where the claim is located."
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The opening background block states that oceanic crust forms from mantle-derived melt, which is a claim about the crust and names it."
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states that the volume change from degassing, under extensional stress, raises strain rates locally and sets off deep earthquakes within the mantle; the mantle is named and is where the triggering is placed."
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reads the crustal thickness as placing most of these events in the mantle with a few scattered in the crust; the mantle is named and is where the events are placed."
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports a modelled temperature at the relevant depths and concludes the mantle beneath the segment axis is hot; the mantle is named and is the subject of that conclusion."
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states that how these melts reach the surface through the mantle's upper part is not understood; the mantle is named and bounds the claim."
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reads the sea-floor observations as showing exhumed mantle and supporting a tectonic origin for the subsection; the mantle is named and its presence is what the sentence asserts."
        },
        {
          "row_index": 73,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block supports the statement itself: the dashed lines in the schematic carry isotherms taken from a simulated thermal model. The model is named there only as where those lines came from, not as what the sentence is about, so the record's attachment to the thermal model as its subject is only partly supported."
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block describes choosing among the constructed one-dimensional models on located-event count and residual, so both the statement and its attachment to the velocity model hold."
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block compares the selected model against the minimum model and reports the selected one locating more events; the velocity model is what the sentence is about."
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The figure-caption block says how the hummocky sea floor and the volcanic cones are shaded, so the cones are among the things the sentence is about and are named there."
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives how many events were located along the transform, matching the projected count and scope; the transform is named and is where those events lie."
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states how many one-dimensional P-wave models were constructed, matching the projected count and its scope; the models are what is counted and are named there."
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The figure-caption block gives the crustal thickness beneath the segment with its uncertainty and an approximation marker, matching the projected bounds, unit and qualification; the segment is named and is where the thickness is measured."
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the depth of the deep earthquakes observed beneath the segment axis as an interval, matching the projected bounds and unit; the segment is named and is where the events lie."
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The observations block places the deep microseismicity beneath the segment ridge axis over an approximate depth interval, matching the projected bounds, unit and qualification; the segment is named."
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block describes the depth-test subset and the interval its events span, matching the projected bounds and unit; the segment is named and is where those events lie."
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same methods block gives the size of that subset and the cross-section it was drawn along, matching the projected count and scope; the segment is named."
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the depth reached by the off-axis shallow microseismicity west of the segment axis as an upper bound, matching the projected bound, unit and qualification; the segment is named."
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the thickness of the older crust on the western ridge flank with its uncertainty, matching the projected value and unit; the crust is what is measured and is named."
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states how many one-dimensional P-wave models were constructed, matching the projected count and its scope; the models are what is counted and are named there."
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the barium enrichment of the segment's samples as a lower bound in the projected unit; the segment is named and scopes the measurement."
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the calculated CO2 content of the melts generated along the segment as an interval in the projected unit and marks it calculated; the segment is named."
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the calculated CO2 interval for the southern segment in the projected unit; that segment is named there."
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the estimated pre-eruptive CO2 range for the segment after fractional crystallisation, matching the projected bounds and unit; the segment is named."
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states the minimum CO2 concentration in the primary melts along the segment, matching the projected lower bound, unit and open-bound qualification; the segment is named."
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the barium-based pre-eruptive CO2 range for the segment, matching the projected bounds, unit and estimation basis; the segment is named."
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the barium-based pre-eruptive CO2 range for the southern segment, matching the projected bounds, unit and basis; that segment is named."
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the barium-corrected primary-melt CO2 range for the segment, matching the projected bounds, unit and estimation basis and marking the values estimated; the segment is named."
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the barium-corrected primary-melt range for the southern segment, matching the projected bounds, unit and basis; that segment is named."
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium-based pre-eruptive CO2 range for the segment, matching the projected bounds, unit and basis; the segment is named."
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium-based pre-eruptive range for the southern segment, matching the projected bounds, unit and basis; that segment is named."
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium-corrected primary-melt range for the segment, matching the projected bounds, unit and basis; the segment is named."
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium-corrected primary-melt range for the southern segment, matching the projected bounds, unit and basis; that segment is named."
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium enrichment of the segment's samples as a lower bound in the projected unit; the segment is named and scopes the measurement."
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the water content proposed at the base of the boundary as an upper bound in the projected unit and attributes it to a modelling argument, which supports the modelled determination; the boundary is named."
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The results block gives the length of the transform's eastern part covered by the network, matching the projected value and unit; the transform is what is measured and is named."
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives how many events were located along the transform, matching the projected count and scope; the transform is named and is where those events lie."
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states how many one-dimensional P-wave models were constructed, matching the projected count and its scope; the models are what is counted and are named there."
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the barium enrichment of the segment's samples as a lower bound in the projected unit; the segment is named and scopes the measurement."
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the calculated CO2 content of the melts generated along the segment as an interval in the projected unit and marks it calculated; the segment is named."
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the calculated CO2 interval for the southern segment in the projected unit; that segment is named there."
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the estimated pre-eruptive CO2 range for the segment after fractional crystallisation, matching the projected bounds and unit; the segment is named."
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states the minimum CO2 concentration in the primary melts along the segment, matching the projected lower bound, unit and open-bound qualification; the segment is named."
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the barium-based pre-eruptive CO2 range for the segment, matching the projected bounds, unit and estimation basis; the segment is named."
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the barium-based pre-eruptive CO2 range for the southern segment, matching the projected bounds, unit and basis; that segment is named."
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block gives the barium-corrected primary-melt CO2 range for the segment, matching the projected bounds, unit and estimation basis and marking the values estimated; the segment is named."
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the barium-corrected primary-melt range for the southern segment, matching the projected bounds, unit and basis; that segment is named."
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium-based pre-eruptive CO2 range for the segment, matching the projected bounds, unit and basis; the segment is named."
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium-based pre-eruptive range for the southern segment, matching the projected bounds, unit and basis; that segment is named."
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium-corrected primary-melt range for the segment, matching the projected bounds, unit and basis; the segment is named."
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium-corrected primary-melt range for the southern segment, matching the projected bounds, unit and basis; that segment is named."
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The figure-caption block gives the crustal thickness beneath the segment with its uncertainty and an approximation marker, matching the projected bounds, unit and qualification; the segment is named and is where the thickness is measured."
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the depth of the deep earthquakes observed beneath the segment axis as an interval, matching the projected bounds and unit; the segment is named and is where the events lie."
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The observations block places the deep microseismicity beneath the segment ridge axis over an approximate depth interval, matching the projected bounds, unit and qualification; the segment is named."
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block describes the depth-test subset and the interval its events span, matching the projected bounds and unit; the segment is named and is where those events lie."
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same methods block gives the size of that subset and the cross-section it was drawn along, matching the projected count and scope; the segment is named."
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the depth reached by the off-axis shallow microseismicity west of the segment axis as an upper bound, matching the projected bound, unit and qualification; the segment is named."
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the rubidium enrichment of the segment's samples as a lower bound in the projected unit; the segment is named and scopes the measurement."
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the segment's length with an approximation marker, matching the projected value, unit and qualification, and names the segment."
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the southern segment's length, matching the projected value and unit, and names that segment."
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The introduction block gives the approximate length of the ridge segment between the two transforms, matching the projected value, unit and qualification, and names the segment."
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reads the microseismicity beneath the southern discontinuity as putting the boundary at the projected depth with an approximation marker; the boundary is what the sentence is about and is named."
        },
        {
          "row_index": 129,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block sets out the cold and thick lithosphere explanation, under which the boundary would lie at the projected approximate depth; the hypothesised framing and the boundary as subject both come from that sentence."
        },
        {
          "row_index": 130,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reads the off-axis shallow microseismicity as keeping the boundary above the projected depth, matching the upper bound and its qualification; the boundary is named."
        },
        {
          "row_index": 131,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The background block gives the isotherm the maximum earthquake depth corresponds to, with its uncertainty, matching the projected value and unit; the boundary being defined is named there."
        },
        {
          "row_index": 132,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same block gives the melt fraction proposed at the base of the boundary with an approximation marker, matching the projected value, unit and qualification; the boundary is named."
        },
        {
          "row_index": 133,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the water content proposed at the base of the boundary as an upper bound in the projected unit and attributes it to a modelling argument, which supports the modelled determination; the boundary is named."
        },
        {
          "row_index": 134,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the approximate temperature at which melt is present for anhydrous peridotites at the boundary, matching the projected value, unit and qualification; the boundary is named."
        },
        {
          "row_index": 135,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the thickness of the older crust on the western ridge flank with its uncertainty, matching the projected value and unit; the crust is what is measured and is named."
        },
        {
          "row_index": 136,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block places the earthquakes produced by continued degassing in the mantle over the projected depth interval, matching bounds and unit, and names the mantle."
        },
        {
          "row_index": 137,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The background block gives the depth interval at which extensive dry melting begins under mantle upwelling, matching the projected bounds and unit; the mantle is named."
        },
        {
          "row_index": 138,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the age of the cold lithosphere behind the cold-edge effect near the intersection, matching the projected value and unit, and names the lithosphere."
        },
        {
          "row_index": 139,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block states the lower bound on the temperature of the hot mantle in which these earthquakes occur, matching the projected bound, unit and qualification, and names the mantle."
        },
        {
          "row_index": 140,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the modelled temperature interval at the relevant depths beneath the segment axis, matching the projected bounds, unit and modelled determination, and names the mantle."
        },
        {
          "row_index": 141,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the age below which a magmatically accreted crust counts as young, matching the projected upper bound and unit, and names the crust."
        },
        {
          "row_index": 142,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block states how many one-dimensional P-wave models were constructed, matching the projected count and its scope; the models are what is counted and are named there."
        },
        {
          "row_index": 143,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The figure-caption block gives the crustal thickness beneath the segment with its uncertainty and an approximation marker, matching the projected bounds, unit and qualification; the segment is named and is where the thickness is measured."
        },
        {
          "row_index": 144,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the depth of the deep earthquakes observed beneath the segment axis as an interval, matching the projected bounds and unit; the segment is named and is where the events lie."
        },
        {
          "row_index": 145,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The observations block places the deep microseismicity beneath the segment ridge axis over an approximate depth interval, matching the projected bounds, unit and qualification; the segment is named."
        },
        {
          "row_index": 146,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block describes the depth-test subset and the interval its events span, matching the projected bounds and unit; the segment is named and is where those events lie."
        },
        {
          "row_index": 147,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the depth reached by the off-axis shallow microseismicity west of the segment axis as an upper bound, matching the projected bound, unit and qualification; the segment is named."
        },
        {
          "row_index": 148,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block reports the thickness of the older crust on the western ridge flank with its uncertainty, matching the projected value and unit; the crust is what is measured and is named."
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
