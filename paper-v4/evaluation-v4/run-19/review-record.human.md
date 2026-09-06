# Malleus paper v4 run-19 source-grounded review record

Template. The row counts are substituted at freeze, from the frozen cell's own
query result, at the same time as `paper-v4/evaluation-v4/review-task-v4.template.md`.
No placeholder may survive instantiation.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

Fill one `rows` entry per returned row, in order, zero-based: 15 for
CQ-01, 37 for CQ-02, 52 for CQ-03, 50 for
CQ-04, 154 in all. Cite reading block ids only. Write the reasons in
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
    "review_input_manifest_sha256": "sha256:9eba71ed0582c12653b71aeb7417a4be5509933e4cbf1bbd928c033fe6de35d6"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-preliminary-run-19",
    "completed_at": "2026-09-06T05:24:34Z"
  },
  "questions": [
    {
      "question_id": "CQ-01",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "The campaign row names the cruise and carries the instrument count together with the scope that says those instruments were deployed, and the instrument row names the seafloor seismometers that acquired the microseismicity data, so the observing system, the campaign, the instrument count and the acquisition are each addressed directly by a returned row and by the reading blocks those rows derive from. The remaining rows are method records describing how the data were detected, located, relocated, magnitude-scaled and compiled; they bear on processing rather than on who acquired the data, so they dilute the answer without leaving any requested part of the question unanswered.",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The two cited blocks name the cruise and state that the seismometer network deployed for it held nineteen instruments, so the name, the count and the count scope all hold on the reading. The duration the row carries is the length of the continuous seismic recording, which the results block gives as a property of the data, not of the cruise; the methods block places the cruise in two summer months without giving its length. The row attributes a recording window to the campaign itself, and neither block makes that attribution."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the ocean-bottom seismometers that acquired the microseismicity data, which is the only field this instrument record projects."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006",
            "page:8:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first block names the solubility model and uses it to argue about the depth at which the melt saturates; the methods block gives the model's published author, the three input parameters the row lists and the degassing question the calculation was run to settle. Both projected fields hold."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The code availability block names the mapping software and states that it was used for structural analysis, which is exactly what the record's name asserts."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block describes the worldwide compilation of maximum earthquake depths at slow- and ultraslow-spreading ridges, the deliberate choice of depths constrained by more than one event to avoid location bias, and the additional factors the authors folded in. Name and description both hold."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block states that focal mechanisms were determined from first-motion polarities of the P phase using the named package, which is the whole of the record's projected name."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block states that the well-constrained events were relocated by the double-difference method using the named program, matching the record's name."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The magnitude block gives the local magnitude scale, the expression itself and the meaning of the amplitude and hypocentral-distance terms, including the simulated instrument response used to measure the amplitude. The text layer renders the sign and decimal glyphs of the expression oddly, but a reader resolves it to the same formula the record carries."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:008",
            "page:2:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block lists the three reliability criteria and states how many of them each of the four categories has to meet; the results block states that the locations were classified into those four categories. Name and description hold on the pair."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block states that published geochemical analyses of basalt samples collected inside the seismometer network's footprint were compiled, which is the record's name."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004",
            "page:7:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first block names the non-linear search algorithm and the program used for initial hypocenters; the next block gives the confidence-level error ellipsoid drawn from the posterior samples and the iterative station corrections chosen by minimising the average residual. Name and description hold."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block states that arrivals were detected automatically with the short-term over long-term average trigger inside the named package, which is the record's name."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block states that the named program was used to search for a minimum one-dimensional velocity model as a check on the selected model, matching the record's name."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block states that five one-dimensional velocity models were built from an active-source wide-angle refraction profile, gives the depth to which that profile constrains velocity, and states that the average model was found best-fitting and kept for locating earthquakes and computing focal mechanisms. Name and description both hold."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The magnitude block states that the completeness magnitude and the b value were calculated with the named software, which is the use the record's name gives it."
        }
      ]
    },
    {
      "question_id": "CQ-02",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "The catalog-subset row for the deep events names the ridge subsection and places those events beneath its ridge axis, which is both halves of the question in one row, and the block it derives from states the same association among the study's key observations. A feature row independently carries that subsection as a named ridge segment, and a claim row carries the paper's own report of deep earthquakes beneath the ridge axis. Most other rows describe neighbouring features, segment dimensions, orientations and melt chemistry that the question does not ask about; they dilute the answer without leaving the named region, the earthquake population or the spatial relation unaddressed, and no returned row associates the deep events with a competing subsection.",
      "source_locators": [
        "page:2:block:004",
        "page:1:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this transform fault as one of the two bounding the ridge segment the study sits on. It appears in the abbreviated form the paper uses throughout, which a reader resolves to the name the row carries, and the name is the only field this record projects."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the ridge in full, which is the record's only projected field."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block subdivides the studied ridge portion and gives this discontinuity its short name in the same sentence that calls the two offsets non-transform discontinuities, so both the name and the feature type hold."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports an extinct hydrothermal vent field on the flank of the first discontinuity. Its extinction is stated as an observation, not inferred, so the feature type and the inactive status both hold."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The same subdivision sentence names the second discontinuity and identifies the class it belongs to, covering both projected fields."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the core complex that sits east of the ridge axis, on the far side of the bounding detachment fault, and identifies it as such, which is what the record's name and feature type say."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this subsection as the ridge-transform intersection segment and, two sentences later, calls that segment amagmatic, so the compound feature type the row carries is assembled from statements in the one cited block."
        },
        {
          "row_index": 7,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first block names the westward-dipping detachment fault bounding the intersection segment, so the name and feature type hold squarely. The inactive status rests on the second block, where inactivity is the authors' inference from an absence of deep seismicity beneath the valley floor and is written as a suggestion. The row states the status flat and drops that hedge."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The subdivision sentence names this subsection and calls it a short ridge segment, covering the name and the feature type the row carries."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block refers to the axial valley in the cross-sections through this segment when it places a shallow cluster on the valley's western side. Name and feature type are the only projected fields and the block carries both; the record's identifier ties it to the segment, but no projected field asserts that tie."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the ridge segment south of the second discontinuity and calls it a ridge segment, covering both projected fields."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this transform fault as the northern bound of the study area and as the intersection the study area sits next to. It is abbreviated in the prose, and the record's name is the ordinary expansion of that abbreviation."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block is the paper's own report of deep mantle earthquakes along the ridge axis, and the subject's name appears in that sentence and in the title above it. The row projects only the modality and the subject reference, and both hold: the sentence is an unhedged first-person report about that ridge. The row carries neither the claim's wording nor a locator, so there was nothing on this row to check a statement digest against."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block denies that active hydrothermal vents have been observed on this segment's axis, and the segment is named in that sentence. A negated modality is the right reading of a sentence whose content is the absence of the observation."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block concludes that magmatism dominates crustal accretion at this segment, naming the segment in the same sentence, and states it as a conclusion drawn rather than a possibility, which matches the stated modality the row carries."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block names the segment and denies any evidence for detachment faults there, so both the subject reference and the negated modality hold."
        },
        {
          "row_index": 16,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK The segment is named in the cited block, but the degassing statement there is general: it explains why measured contents in samples from two neighbouring segments sit close to the calculated solubility, and it speaks of seafloor basalts as a class. Making one of those two segments the record's subject drops the other and narrows a general statement to a place the prose does not confine it to."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block reports how many relocated events ended up along the ridge, using the subject's short form, and the row's count and count scope repeat that split without changing it."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block's third key observation places normal-depth earthquakes beneath the southern part of this discontinuity and names it there. The row projects no count, and its count scope is that observation."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block's first key observation puts shallow earthquakes on the outside corner of the intersection, beneath the core complex dome and off-axis west of this segment, and names the segment there. The block qualifies that population as a majority of the shallow events; the row projects no count, so it claims no proportion the qualifier would have to carry."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block's second key observation places the deep microseismicity beneath the ridge axis of this segment and names the segment in the same clause, which is exactly the subset scope and the subject the row carries."
        },
        {
          "row_index": 21,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK The count and the count scope are stated outright in the first block, and the subject's name appears there too. The subject attribution is what fails: the located events are the whole intersection region's catalogue, and the very next sentence of that block separates the region into four subsections, of which the row's subject is one. The prose gives no ground for treating a region-wide catalogue subset as belonging to a single subsection."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block reports how many relocated events fell along this transform fault and names it in the short form the subject carries as a tag. Count and scope match."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives the ridge's half-spreading rate in the study area with the subject named in the same sentence, and the value, unit and exact qualification match what is written. The block localises the rate to the study area, and that is the ridge portion this subject record stands for in the reading."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block names the discontinuity and gives its length with the tilde the row records as an approximate qualification. Quantity kind, value, unit and subject all hold."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block names the discontinuity and states that seismicity down to that depth shows the brittle-ductile boundary sits at about it, matching the row's quantity kind, value, unit and approximate qualification."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block names the discontinuity and gives its ridge offset with a tilde, which is the quantity kind, value, unit and qualification the row carries."
        },
        {
          "row_index": 27,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK The pressure range and its unit are in the cited block and the subject is named in the same sentence, but the block gives that range as a general triggering threshold taken from earlier work and then uses it to argue that degassing could induce the earthquakes seen beneath this segment's axis. The prose does not report the threshold as a quantity measured or derived for the segment, so the value holds while its attachment to this subject does not."
        },
        {
          "row_index": 28,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block names the segment and does give the shallow bound on the brittle-ductile boundary with the open lower end the row records. The bound is stated for the off-axis area west of the segment axis and out to a young crustal age only; the row carries neither restriction, and the same reading places this segment's axial seismicity far deeper, so an unqualified bound on the segment overstates the block."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block names the segment and gives its along-strike length with a tilde, matching the row's quantity kind, value, unit and approximate qualification."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The same sentence gives the width of the segment's median valley as a round figure, which is the row's quantity kind, value and unit. The block calls that width typical for such a valley; the figure itself is stated without hedging."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives the orientation of the segment's neo-volcanic ridge as a bearing east of north, and the row's angle, unit and subject are that bearing read as degrees from north."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives the pre-eruptive concentration range for this segment, names it, and calls the figures estimated, which matches the row's quantity kind, bounds, unit and determination."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005",
            "page:8:block:007",
            "page:1:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The two later blocks tie the same primary-melt concentration range to this segment by name and describe it as calculated and estimated, which covers the quantity kind, bounds, unit, determination and subject. The abstract block that the value derivation also reaches gives the same range with the approximate marker the row keeps but does not name the segment, so the subject rests on the other two."
        },
        {
          "row_index": 34,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK The segment is named in the cited block and the temperature figure, its unit and its open lower bound appear there. They appear inside a conditional: the block offers higher temperatures below that depth as something that could account for the absence of deeper earthquakes. The row states the temperature as a modelled value about the segment without that conditional, and the thermal-modelling figures stated outright elsewhere in the reading are for a shallower depth interval."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block names the segment and gives its length as a round figure with no hedge, matching the row's quantity kind, value, unit and exact qualification."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block names this segment and gives the calculated primary-melt concentration range for it, which is the row's quantity kind, bounds, unit, determination and subject."
        }
      ]
    },
    {
      "question_id": "CQ-03",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "One half of the question is answered squarely. Rows carry the primary-melt carbon dioxide range for the central segment with its unit and an explicit estimate status, and the neighbouring segment's range beside it for contrast. The other half is not answered. No returned row carries an earthquake depth range as a bounded quantity: the rows that reach the deep seismicity give a scope phrase or a modality and no bounds, and the depth quantities that do come back are brittle-ductile boundary depths at other features, which is a different quantity. The requested depth range is therefore present only as description, so the rows address part of the question.",
      "source_locators": [
        "page:2:block:004",
        "page:5:block:005",
        "page:8:block:007",
        "page:1:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this transform fault in its abbreviated form while placing the studied ridge between it and the northern one, and the name is the only thing this row asserts."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the ridge in full in its title and again in the reported finding, which is all the row carries."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block introduces the first discontinuity under this name and calls the pair of them non-transform discontinuities, so the name and the feature kind both hold."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports an extinct vent field on the eastern flank of the first discontinuity, stated flatly, which carries the name, the feature kind and the inactive status."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block introduces the second discontinuity under this name within the same enumeration of subsections, and calls them non-transform discontinuities."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block describes the core complex sitting east of the ridge axis, which supplies both the name and the feature kind."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this subsection and, in the following sentence, calls the intersection segment amagmatic, so the compound feature kind is covered as well as the name."
        },
        {
          "row_index": 7,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first block gives the fault and its kind directly. The second infers inactivity from an absence of deep seismicity and states it as a suggestion, whereas the row records the status flatly, so that qualifier is missing."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this short ridge segment in the enumeration of subsections and gives its kind."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block treats the axial valley as an existing feature while locating a shallow cluster on its western side, which covers the name and the kind the row projects."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the segment lying south of the second discontinuity and identifies it as a ridge segment."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this transform fault, abbreviated, as the northern bound of the studied ridge and again at the intersection it forms with it."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006",
            "page:8:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One block names the solubility model as the thing applied to the melt; the other gives the published model it comes from, the three input parameters, and the degassing question it was run to settle, which is what the description states."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block names this tool and the structural analysis it was used for, which is the whole of the row."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block describes the worldwide maximum-depth compilation, the rule of accepting a depth only when several events constrain it so as to avoid location bias, and the accompanying factors the description lists."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block states that first-motion polarities picked on the vertical component were used with this package to obtain focal mechanisms."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the double-difference program and the relocation step it performed, which is what the row calls it."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block gives the local magnitude scale, the same expression term by term, the simulated Wood-Anderson amplitude and the hypocentral distance in kilometres. The extractor mangles the minus glyph but the formula is recoverable from the block."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:7:block:008"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One block records the four-way classification of locations; the other lists the three criteria and states which category meets all of them and which meet fewer, matching the description."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block states that published geochemical analyses of basalt samples collected inside the instrument network footprint were compiled."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004",
            "page:7:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One block names the search algorithm used for the initial hypocentres; the other gives the confidence ellipsoid from the posterior samples and the iterative station corrections that the description repeats."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the trigger algorithm and the package containing it as the automatic detection step."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block states that this program was used to search for the minimum one-dimensional model as a check on the model already chosen."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block covers the construction of the candidate models from the wide-angle refraction profile, the depth to which they are constrained, and the selection of the averaged model for locating events and computing mechanisms, which is the description."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block attributes the completeness magnitude and the b-value to this software, which is what the row names it for."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:8:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One block establishes that published analyses inside the network footprint were compiled; the other states that the samples of this segment were among those analysed, which is the sample set the row names."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:8:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One block establishes the compilation inside the network footprint; the other states that the samples of the adjacent southern segment were analysed alongside those of the studied one."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block reports the deep events along the ridge axis in the authors' own declarative voice, which matches the recorded modality, and the ridge it names in that sentence is the subject the row shows."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block denies active venting on this segment's axis, so both the negated modality and the segment as what is being spoken about are supported."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block concludes plainly that magmatic accretion dominates at this segment, which fits the recorded modality and makes the segment the thing the claim is about."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block states that this segment shows no evidence of detachment faulting, which is a negation whose subject is that segment."
        },
        {
          "row_index": 31,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block supports the degassing statement and names the segment, but it makes the point about seafloor basalts in general and rests it on samples from this segment and its southern neighbour alike, so the block does not establish this one segment as what the record is about."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives the count and says those events lie along the ridge, which is both the scope phrase the row carries and the feature the subset is about."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block lists normal-depth seismicity beneath the southern discontinuity as one of its key observations, which is the scope the row records and the feature it belongs to."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block places the shallow events at the intersection corner and off-axis west of this segment, in the wording the row's scope follows, and that segment is what the subset is about."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block records the deep microseismicity beneath this segment's ridge axis, which matches both the scope phrase and the subject."
        },
        {
          "row_index": 36,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK The blocks support the count and the region it covers, and the first names the segment. But the same block says the located events span all four subsections and the transform fault, so it does not support this one subsection as the thing the subset is about."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives the count for events along the transform fault, which is at once the scope and the feature the subset is about."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block states the half-spreading rate for the ridge in this area with its unit and no hedge, and the ridge is the subject."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives this discontinuity's along-strike length with the unit and the approximation marker the row carries."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block reads the brittle-ductile boundary beneath this discontinuity off the seismicity and gives the depth with the same approximation, for that feature."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives the ridge offset for this discontinuity with its unit and approximation."
        },
        {
          "row_index": 42,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block supports the pressure range and names the segment, but the range is a general triggering threshold carried over from earlier work rather than a quantity determined for this segment, and the block ties it to the segment only as a suggestion, so neither the subject attribution nor that framing is carried by the row."
        },
        {
          "row_index": 43,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block supports the upper bound on the boundary depth, but only west of this segment's axis and only out to a stated crustal age, and the same block reports much deeper seismicity beneath the axis itself. The row carries no such restriction, so a needed qualifier is absent."
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives this segment's along-strike length with the unit and the approximation the row records."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives the width of this segment's median valley with its unit, in the same sentence that identifies the segment."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives the strike of the neo-volcanic ridge inside this segment, which reads directly as the angle from north the row records."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives the pre-eruptive concentration range for this segment, its unit, and that the range is an estimate, which covers every field the row carries."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:005",
            "page:8:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK Three blocks carry this. The first gives the approximate range for the primary melts; the other two attach the same range to this segment and label it as calculated from the trace-element proxies, so the bounds, the unit, the estimate status and the subject are all supported."
        },
        {
          "row_index": 49,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block supports the temperature bound, the unit and the segment, but it offers the figure as a possible reason for the absence of deeper events and points to earlier work, rather than presenting it as a model result. The determination the row records is not carried by this block."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives the length of the southern magmatic segment with its unit, and that segment is the subject."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives the calculated melt concentration range for the southern segment with its unit, which matches the bounds, the estimate status and the subject."
        }
      ]
    },
    {
      "question_id": "CQ-04",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "No returned row states the mechanism the authors prefer, and no row carries an epistemic marker for it. The one row whose derivation reaches the mechanism block records a pore-pressure threshold able to trigger earthquakes, which covers the pressure change and the trigger the question asks for, but its projection names neither the degassing nor the ascending melt and carries no modality field. The melt carbon dioxide rows and the rows that rule out the competing explanations supply the surrounding argument without stating the mechanism or marking it as a hypothesis. The rows therefore address part of the question and leave the rest to the derivation trail.",
      "source_locators": [
        "page:5:block:003",
        "page:1:block:001",
        "page:5:block:005",
        "page:3:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this transform fault in its abbreviated form while placing the studied ridge between it and the northern one, and the name is the only thing this row asserts."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the ridge in full in its title and again in the reported finding, which is all the row carries."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block introduces the first discontinuity under this name and calls the pair of them non-transform discontinuities, so the name and the feature kind both hold."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports an extinct vent field on the eastern flank of the first discontinuity, stated flatly, which carries the name, the feature kind and the inactive status."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block introduces the second discontinuity under this name within the same enumeration of subsections, and calls them non-transform discontinuities."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block describes the core complex sitting east of the ridge axis, which supplies both the name and the feature kind."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this subsection and, in the following sentence, calls the intersection segment amagmatic, so the compound feature kind is covered as well as the name."
        },
        {
          "row_index": 7,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The first block gives the fault and its kind directly. The second infers inactivity from an absence of deep seismicity and states it as a suggestion, whereas the row records the status flatly, so that qualifier is missing."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this short ridge segment in the enumeration of subsections and gives its kind."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block treats the axial valley as an existing feature while locating a shallow cluster on its western side, which covers the name and the kind the row projects."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the segment lying south of the second discontinuity and identifies it as a ridge segment."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names this transform fault, abbreviated, as the northern bound of the studied ridge and again at the intersection it forms with it."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006",
            "page:8:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One block names the solubility model as the thing applied to the melt; the other gives the published model it comes from, the three input parameters, and the degassing question it was run to settle, which is what the description states."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The code-availability block names this tool and the structural analysis it was used for, which is the whole of the row."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block describes the worldwide maximum-depth compilation, the rule of accepting a depth only when several events constrain it so as to avoid location bias, and the accompanying factors the description lists."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block states that first-motion polarities picked on the vertical component were used with this package to obtain focal mechanisms."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the double-difference program and the relocation step it performed, which is what the row calls it."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block gives the local magnitude scale, the same expression term by term, the simulated Wood-Anderson amplitude and the hypocentral distance in kilometres. The extractor mangles the minus glyph but the formula is recoverable from the block."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:7:block:008"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One block records the four-way classification of locations; the other lists the three criteria and states which category meets all of them and which meet fewer, matching the description."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block states that published geochemical analyses of basalt samples collected inside the instrument network footprint were compiled."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004",
            "page:7:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW One block names the search algorithm used for the initial hypocentres; the other gives the confidence ellipsoid from the posterior samples and the iterative station corrections that the description repeats."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the trigger algorithm and the package containing it as the automatic detection step."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block states that this program was used to search for the minimum one-dimensional model as a check on the model already chosen."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block covers the construction of the candidate models from the wide-angle refraction profile, the depth to which they are constrained, and the selection of the averaged model for locating events and computing mechanisms, which is the description."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block attributes the completeness magnitude and the b-value to this software, which is what the row names it for."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block reports the deep events along the ridge axis in the authors' own declarative voice, which matches the recorded modality, and the ridge it names in that sentence is the subject the row shows."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block denies active venting on this segment's axis, so both the negated modality and the segment as what is being spoken about are supported."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block concludes plainly that magmatic accretion dominates at this segment, which fits the recorded modality and makes the segment the thing the claim is about."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block states that this segment shows no evidence of detachment faulting, which is a negation whose subject is that segment."
        },
        {
          "row_index": 29,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block supports the degassing statement and names the segment, but it makes the point about seafloor basalts in general and rests it on samples from this segment and its southern neighbour alike, so the block does not establish this one segment as what the record is about."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives the count and says those events lie along the ridge, which is both the scope phrase the row carries and the feature the subset is about."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block lists normal-depth seismicity beneath the southern discontinuity as one of its key observations, which is the scope the row records and the feature it belongs to."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block places the shallow events at the intersection corner and off-axis west of this segment, in the wording the row's scope follows, and that segment is what the subset is about."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block records the deep microseismicity beneath this segment's ridge axis, which matches both the scope phrase and the subject."
        },
        {
          "row_index": 34,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK The blocks support the count and the region it covers, and the first names the segment. But the same block says the located events span all four subsections and the transform fault, so it does not support this one subsection as the thing the subset is about."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives the count for events along the transform fault, which is at once the scope and the feature the subset is about."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block states the half-spreading rate for the ridge in this area with its unit and no hedge, and the ridge is the subject."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives this discontinuity's along-strike length with the unit and the approximation marker the row carries."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block reads the brittle-ductile boundary beneath this discontinuity off the seismicity and gives the depth with the same approximation, for that feature."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives the ridge offset for this discontinuity with its unit and approximation."
        },
        {
          "row_index": 40,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block supports the pressure range and names the segment, but the range is a general triggering threshold carried over from earlier work rather than a quantity determined for this segment, and the block ties it to the segment only as a suggestion, so neither the subject attribution nor that framing is carried by the row."
        },
        {
          "row_index": 41,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block supports the upper bound on the boundary depth, but only west of this segment's axis and only out to a stated crustal age, and the same block reports much deeper seismicity beneath the axis itself. The row carries no such restriction, so a needed qualifier is absent."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives this segment's along-strike length with the unit and the approximation the row records."
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives the width of this segment's median valley with its unit, in the same sentence that identifies the segment."
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives the strike of the neo-volcanic ridge inside this segment, which reads directly as the angle from north the row records."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives the pre-eruptive concentration range for this segment, its unit, and that the range is an estimate, which covers every field the row carries."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:005",
            "page:8:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK Three blocks carry this. The first gives the approximate range for the primary melts; the other two attach the same range to this segment and label it as calculated from the trace-element proxies, so the bounds, the unit, the estimate status and the subject are all supported."
        },
        {
          "row_index": 47,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block supports the temperature bound, the unit and the segment, but it offers the figure as a possible reason for the absence of deeper events and points to earlier work, rather than presenting it as a model result. The determination the row records is not carried by this block."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives the length of the southern magmatic segment with its unit, and that segment is the subject."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block gives the calculated melt concentration range for the southern segment with its unit, which matches the bounds, the estimate status and the subject."
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
