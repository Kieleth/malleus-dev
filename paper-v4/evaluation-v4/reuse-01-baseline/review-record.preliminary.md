# Malleus paper v4 source-grounded review record, protocol v3.2, reuse-01-baseline

Assembled by `paper-v4/evaluation-v4/reuse-01-baseline/assemble_record.py` from the
preliminary reviewer's `review-witnesses.json` and its thirty filled review blocks.
The rows are rebuilt from the answer file, not copied from the blocks.
`PRELIMINARY_COMPLETE` is not paper evidence; Luis ratifies.

```json
{
  "schema": "malleus.paper-v4.source-grounded-review/v3.2",
  "status": "PRELIMINARY_COMPLETE",
  "inputs": {
    "review_protocol_sha256": "sha256:5dfd59f4aa479dd72738e2eb55653ee3e84e60886de4cccbcc0a8e66d06e55cd",
    "review_input_manifest_sha256": "sha256:8d226c07ba1a454dcdb9213f47243ce0fe3bdcac8c43925d1f988f28b942cc2f"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-preliminary-reuse-01-baseline",
    "completed_at": "2026-09-12T06:59:06Z"
  },
  "witnesses": [
    {
      "witness_key": "CQ-B-T1-01:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rationale": "Both cited blocks name the cruise as the source of the recordings: the results block ties the seismometer network to it and the methods block repeats the tie for the passive experiment. The claim asserts nothing more."
    },
    {
      "witness_key": "CQ-B-T1-01:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:002",
        "page:2:block:002"
      ],
      "rationale": "The methods block dates the experiment to July and August of 2019 and the results block gives the same year for the cruise, so both the year and the two months the claim names are carried."
    },
    {
      "witness_key": "CQ-B-T1-01:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rationale": "Each cited block puts the network at nineteen ocean-bottom instruments, one calling it the acquiring network and the other saying that many were deployed. Nineteen on the bottom is exactly what the claim states."
    },
    {
      "witness_key": "CQ-B-T1-02:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:001"
      ],
      "rationale": "The block's first line carries the article identifier in full, digit for digit as the claim writes it, so the identifier is directly on the cited surface."
    },
    {
      "witness_key": "CQ-B-T1-02:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:006"
      ],
      "rationale": "The block carries a dated receipt line for 23 February 2023 in the article header material, which is the date the claim gives."
    },
    {
      "witness_key": "CQ-B-T1-02:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:006"
      ],
      "rationale": "The same header block carries an acceptance line dated 30 December 2024, matching the claim."
    },
    {
      "witness_key": "CQ-B-T1-03:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "The block opens by placing the microseismicity study on the Mid-Atlantic Ridge in the equatorial Atlantic, which is both halves of the claim."
    },
    {
      "witness_key": "CQ-B-T1-03:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "The block gives the studied ridge portion a length of about 120 km and says two non-transform discontinuities offset it, so both the length and the count of discontinuities are carried."
    },
    {
      "witness_key": "CQ-B-T1-03:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "The block names the four subsections one by one in the order the claim lists them, attaching each label to its feature."
    },
    {
      "witness_key": "CQ-B-T1-03:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "The block's closing sentence assigns the label to the ridge segment lying south of the second discontinuity, which is the claim exactly."
    },
    {
      "witness_key": "CQ-B-T1-04:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:002",
        "page:8:block:010"
      ],
      "rationale": "The methods block puts the automatic arrival detection inside the named package and the code block says that package was the one used to pick phases, so the picking tool is carried twice over."
    },
    {
      "witness_key": "CQ-B-T1-04:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:004",
        "page:8:block:010"
      ],
      "rationale": "The location block says the initial hypocentres came from the program's non-linear oct-tree search, and the code block confirms the same program was used for earthquake location."
    },
    {
      "witness_key": "CQ-B-T1-04:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:006",
        "page:8:block:010"
      ],
      "rationale": "The methods block attributes the double-difference relocations to the program and the code block adds the version number the claim gives, so the two together carry name, version and method."
    },
    {
      "witness_key": "CQ-B-T1-04:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:010"
      ],
      "rationale": "The code availability block lists a download address beside each of the three programs the question is about, which is what the claim asserts about that statement."
    },
    {
      "witness_key": "CQ-B-T1-05:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:008"
      ],
      "rationale": "The data availability block says the event catalogue and the manually picked P and S arrivals were deposited in the named repository, which is the whole of the claim."
    },
    {
      "witness_key": "CQ-B-T1-05:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:008",
        "page:8:block:009"
      ],
      "rationale": "The deposit identifier is split by the block boundary: the first block carries the prefix and the second the trailing digits. Read in sequence they give the identifier the claim states."
    },
    {
      "witness_key": "CQ-B-T1-05:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:008"
      ],
      "rationale": "The same block says the raw recordings and the cruise reports sit on a campaign web address of the oceanographic fleet and can be asked for on scientific grounds, both halves of the claim."
    },
    {
      "witness_key": "CQ-B-T2-01:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:045"
      ],
      "rationale": "The contributions block opens with this author's three credited tasks, and the claim repeats them without adding a fourth."
    },
    {
      "witness_key": "CQ-B-T2-01:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:045"
      ],
      "rationale": "The block credits the second author with supervising acquisition, processing and interpretation of the seismic data, with developing the idea and with writing, which is the claim item for item."
    },
    {
      "witness_key": "CQ-B-T2-01:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:045"
      ],
      "rationale": "The block splits the geochemistry the same way the claim does: two authors collected and analysed the data, one of them alone did the interpretation and the calculation."
    },
    {
      "witness_key": "CQ-B-T2-01:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:045"
      ],
      "rationale": "The block names the same three initials for the structural analysis, and the claim only reverses the sentence order."
    },
    {
      "witness_key": "CQ-B-T2-01:c5",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:045",
        "page:10:block:046"
      ],
      "rationale": "The sentence crediting the project design runs across the block boundary: the cited block ends on the two sets of initials and the next block carries the verb and the project name. I cite the continuation because it is what completes the assertion; together they state the claim."
    },
    {
      "witness_key": "CQ-B-T2-01:c6",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:046"
      ],
      "rationale": "The cited block names the same four sets of initials as having taken part in collecting data during the cruise, which is the claim."
    },
    {
      "witness_key": "CQ-B-T2-02:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "The acknowledgements block names the Chinese national funder for this author and lists both grant numbers the claim gives, in parentheses after the funder."
    },
    {
      "witness_key": "CQ-B-T2-02:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "The same sentence adds the Zhejiang provincial funder and its single grant reference for the same author, matching the claim."
    },
    {
      "witness_key": "CQ-B-T2-02:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "The block lists the graduate school project with its grant reference, the French state programme and the Brittany regional council's scheme as funders of the research, which is the three-part claim."
    },
    {
      "witness_key": "CQ-B-T2-02:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "The block names the European funder twice for the same author, once under the framework programme and once as an advanced grant with the agreement number the claim quotes."
    },
    {
      "witness_key": "CQ-B-T2-02:c5",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "The block's penultimate sentence says the cruise's shipping time was funded through the national oceanographic fleet infrastructure, which is what the claim says about time at sea."
    },
    {
      "witness_key": "CQ-B-T2-03:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "The block places the study area inside a roughly 200 km ridge segment lying between the two named transform faults, so both the bounding names and the length are carried."
    },
    {
      "witness_key": "CQ-B-T2-03:c2",
      "source_support": "PARTIAL",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "The cited block carries three of the claim's four parts: the core complex on the eastern side of the ridge axis, its setting in the intersection subsection, and a detachment fault bounding that subsection to the east and dipping westward. It says nothing about an outside corner, and that position descriptor is where the claim runs past its block."
    },
    {
      "witness_key": "CQ-B-T2-03:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:001",
        "page:1:block:006"
      ],
      "rationale": "The sentence is split by the page boundary: the cited block carries the inference to exhumed mantle but its subject, the widespread observation of peridotite on the sea floor, sits at the head of the preceding block. I cite that block because it is what supplies the rock the claim names; the two together state the claim."
    },
    {
      "witness_key": "CQ-B-T2-03:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "The cited block draws exactly this inference: no deep microseismicity beneath the axial valley floor near the termination, therefore the detachment is taken to be inactive."
    },
    {
      "witness_key": "CQ-B-T2-04:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "The block attributes the thickness of the 8 Ma crust on the western flank to seismic refraction work and gives the value and its error as the claim writes them."
    },
    {
      "witness_key": "CQ-B-T2-04:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006",
        "page:9:block:036"
      ],
      "rationale": "The thickness sentence carries a reference marker and the cited reference entry resolves it to the two authors and the year the claim names, so the attribution rests on both blocks together."
    },
    {
      "witness_key": "CQ-B-T2-04:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "The block draws the depth inference itself, putting the events below 10 km in the mantle and allowing a scatter of events inside the crust. The claim's firmer wording does not change the content the block carries."
    },
    {
      "witness_key": "CQ-B-T2-04:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:011"
      ],
      "rationale": "The schematic's caption block repeats the same thickness and error for the crust under that segment and says the expected crust-mantle boundary is drawn as a dashed line, both parts of the claim."
    },
    {
      "witness_key": "CQ-B-T2-05:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004",
        "page:8:block:006"
      ],
      "rationale": "Both cited blocks give the two constant ratios with the same central values and the same errors the claim quotes."
    },
    {
      "witness_key": "CQ-B-T2-05:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004",
        "page:10:block:004"
      ],
      "rationale": "The ratios in the discussion block carry a reference marker, and the cited reference entry resolves it to the global mid-ocean ridge compilation by the lead author the claim names."
    },
    {
      "witness_key": "CQ-B-T2-05:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:005"
      ],
      "rationale": "The methods block says the rock analyses were compiled from the named database and restricted to samples falling within the bounds of the instrument network, which is both halves of the claim."
    },
    {
      "witness_key": "CQ-B-T2-05:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:006",
        "page:8:block:007"
      ],
      "rationale": "The first cited block uses the ratios to estimate pre-eruptive melt content for the two segments and the second carries the same step through to primary melts, so the stated purpose and both segments are carried."
    },
    {
      "witness_key": "CQ-B-T3-01:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "The block states the half-spreading rate for this part of the ridge as the claim's figure and unit."
    },
    {
      "witness_key": "CQ-B-T3-01:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "The block opens on the full spreading rate, giving the approximate value and unit the claim repeats."
    },
    {
      "witness_key": "CQ-B-T3-01:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:005",
        "page:9:block:019"
      ],
      "rationale": "Both rate figures carry the same reference marker in their own blocks, and the cited reference entry resolves that marker to the three-author plate motion paper the claim names."
    },
    {
      "witness_key": "CQ-B-T3-02:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "The block says the seismic data were recorded continuously for about 21 days, which is the claim."
    },
    {
      "witness_key": "CQ-B-T3-02:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rationale": "Both cited blocks give the instrument spacing as about 30 km."
    },
    {
      "witness_key": "CQ-B-T3-02:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rationale": "Each cited block gives nineteen instruments deployed and seventeen useful ones whose traces were analysed, so the claim's ratio is carried on both."
    },
    {
      "witness_key": "CQ-B-T3-03:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:003",
        "page:6:block:005"
      ],
      "rationale": "Both cited blocks give the same total of located earthquakes, the results block for the intersection region and the methods block as the final count."
    },
    {
      "witness_key": "CQ-B-T3-03:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:006",
        "page:7:block:007"
      ],
      "rationale": "The first cited block says the double-difference relocation was run on 364 well-constrained events and the second reports that 276 came out well relocated, which is the claim's pair of counts."
    },
    {
      "witness_key": "CQ-B-T3-03:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:007"
      ],
      "rationale": "The block closes on an updated average horizontal uncertainty of about 2.1 km after relocation, the figure and the qualifier the claim gives."
    },
    {
      "witness_key": "CQ-B-T3-03:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:007"
      ],
      "rationale": "The same block splits the final catalogue into 317 events along the ridge and 197 along the transform, exactly the claim's split."
    },
    {
      "witness_key": "CQ-B-T3-04:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:005",
        "page:1:block:001"
      ],
      "rationale": "The discussion block gives the calculated range for melts generated along that segment and the abstract block repeats the same range for the primary melts, so the figure is carried twice."
    },
    {
      "witness_key": "CQ-B-T3-04:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:005"
      ],
      "rationale": "The same sentence sets the southern segment's calculated range against it, and the claim quotes that range unchanged."
    },
    {
      "witness_key": "CQ-B-T3-04:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004",
        "page:8:block:007"
      ],
      "rationale": "The first cited block says the concentrations were computed from the two trace elements in their corrected forms and the second defines those forms as the elements in melts in equilibrium with forsterite-rich olivine, which is the claim."
    },
    {
      "witness_key": "CQ-B-T3-04:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:005",
        "page:8:block:007"
      ],
      "rationale": "The discussion block labels both ranges as calculated and the methods block describes them as estimated from the corrected element concentrations, so the figures are worked out and not measured, as the claim says."
    },
    {
      "witness_key": "CQ-B-T3-05:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "The block puts saturation at about 0.7 GPa for a melt above the stated carbon dioxide content, which is the claim's pressure."
    },
    {
      "witness_key": "CQ-B-T3-05:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "The same sentence gives the equivalent depth in parentheses beside the pressure, about 25 km, as the claim states."
    },
    {
      "witness_key": "CQ-B-T3-05:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "The same sentence gives the temperature at saturation, which the claim repeats."
    },
    {
      "witness_key": "CQ-B-T3-05:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006",
        "page:10:block:013"
      ],
      "rationale": "The saturation sentence attributes the figures to a solubility model by reference marker, and the cited reference entry resolves that marker to the two authors the claim names."
    },
    {
      "witness_key": "CQ-B-T4-01:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:002"
      ],
      "rationale": "The block states the preferred account in its first sentence: the deep microseismicity under that segment is tied to carbon dioxide leaving the ascending melt."
    },
    {
      "witness_key": "CQ-B-T4-01:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:002"
      ],
      "rationale": "The same sentence numbers the account as the fourth possibility and marks it as the authors' preferred one, which is both halves of the claim."
    },
    {
      "witness_key": "CQ-B-T4-01:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001",
        "page:3:block:002",
        "page:3:block:003",
        "page:4:block:002"
      ],
      "rationale": "Each of the four cited blocks opens a different rival account and then sets it aside: a very cold thick lithosphere, cooling by hydrothermal circulation, strain in high-temperature mylonite shear zones, and magmatic-tectonic activity. Four blocks, four accounts, which is the count and the list the claim gives."
    },
    {
      "witness_key": "CQ-B-T4-01:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:003"
      ],
      "rationale": "The block supplies the whole physical chain the claim states: degassing changes volume, extensional stress turns that into locally high strain rates, and a rise in pore pressure of two to three bars is enough to set an event off."
    },
    {
      "witness_key": "CQ-B-T4-02:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "The block opens on the explanation being declined and puts the brittle-ductile boundary at about 20 km under it, which is the claim."
    },
    {
      "witness_key": "CQ-B-T4-02:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "The same block lists the three morphological observations the claim names and draws the magmatic origin of the segment from them."
    },
    {
      "witness_key": "CQ-B-T4-02:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "The block sets the segment against the other ridge by name, whose smooth shape goes with amagmatic spreading over a cold thick lithosphere, which is the contrast the claim reports."
    },
    {
      "witness_key": "CQ-B-T4-02:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "The block's last sentence gives the modelled temperature band for that depth interval and concludes the mantle under the segment axis is hot, both parts of the claim."
    },
    {
      "witness_key": "CQ-B-T4-03:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:002"
      ],
      "rationale": "The block states the cooling hypothesis and then says no active vents have been seen on that segment's axis, which is the ground the claim reports."
    },
    {
      "witness_key": "CQ-B-T4-03:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:002"
      ],
      "rationale": "The same block concedes an extinct vent field on the eastern flank of the first discontinuity, as the claim says."
    },
    {
      "witness_key": "CQ-B-T4-03:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:002"
      ],
      "rationale": "The block adds that the field's position is relatively far from the present-day axial valley and would therefore not affect the lithosphere beneath that segment's axis, which is the claim."
    },
    {
      "witness_key": "CQ-B-T4-04:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:008"
      ],
      "rationale": "The block puts the long-period character as what the spectra imply the events may be, so the hedge the claim reports is the block's own."
    },
    {
      "witness_key": "CQ-B-T4-04:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:008"
      ],
      "rationale": "The same block names the spectral analysis and says it shows some deep events lacking energy above the frequency the claim quotes."
    },
    {
      "witness_key": "CQ-B-T4-04:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:008"
      ],
      "rationale": "The block states the limitation directly: not every event carries the low-frequency character."
    },
    {
      "witness_key": "CQ-B-T4-04:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:008"
      ],
      "rationale": "The block closes by saying more earthquakes would be needed to study the sources, which is the claim's missing requirement."
    },
    {
      "witness_key": "CQ-B-T4-05:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "The block flags the assumption in its own words: deriving the concentrations from trace elements rests on those elements reflecting the mantle source and not having been touched by later processes."
    },
    {
      "witness_key": "CQ-B-T4-05:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "The methods block states the floor for the primary melts along that segment as at least the value the claim gives. The block frames it as what the results suggest, which does not change the minimum it asserts."
    },
    {
      "witness_key": "CQ-B-T5-01:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "The block ties the expected maximum event depth of under 10 km to a full spreading rate near the claim's figure, which is the bound the claim states."
    },
    {
      "witness_key": "CQ-B-T5-01:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006",
        "page:2:block:004"
      ],
      "rationale": "The first cited block gives the 16 to 19 km depths under that segment's axis and the second gives the wider band of about 10 to 20 km for the deep microseismicity there, so both figures in the claim are carried."
    },
    {
      "witness_key": "CQ-B-T5-01:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005",
        "page:2:block:006"
      ],
      "rationale": "Both operands sit in the cited blocks, the expected limit in one and the observed depths in the other, and the second block itself says the observations far exceed the suggested maximum. The margin the claim states is the difference between those two figures."
    },
    {
      "witness_key": "CQ-B-T5-01:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "The block calls the events the deepest documented to date at a slow-spreading centre, which is the claim's attribution of that wording to the authors."
    },
    {
      "witness_key": "CQ-B-T5-02:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "The block gives the flank crust's thickness and its error as the claim writes them."
    },
    {
      "witness_key": "CQ-B-T5-02:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "The same block gives the axial event depths of 16 to 19 km, which against the crustal figure in the same sentence is the comparison the claim makes."
    },
    {
      "witness_key": "CQ-B-T5-02:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "The block draws the inference itself: the events mostly sit in the mantle below 10 km with some scattered ones in the crust, which is the claim."
    },
    {
      "witness_key": "CQ-B-T5-02:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:011",
        "page:7:block:012"
      ],
      "rationale": "The schematic's caption blocks place the expected crust-mantle boundary as a dashed line and put the deep axial events in hot ductile mantle, which is what the claim says the diagram shows."
    },
    {
      "witness_key": "CQ-B-T5-03:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:005"
      ],
      "rationale": "The block gives the calculated range for melts along that segment, the figures the claim quotes."
    },
    {
      "witness_key": "CQ-B-T5-03:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:009"
      ],
      "rationale": "The block states the previous maximum melt content reported at any ridge and names the ridge it came from, both parts of the claim. The claim writes out the ridge name the block abbreviates."
    },
    {
      "witness_key": "CQ-B-T5-03:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:009",
        "page:10:block:004"
      ],
      "rationale": "The earlier maximum carries a reference marker in its block and the cited reference entry resolves it to the global ridge compilation by the lead author the claim names."
    },
    {
      "witness_key": "CQ-B-T5-03:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:005",
        "page:5:block:009"
      ],
      "rationale": "Both figures being compared sit in the cited blocks, the new range in one and the previous maximum in the other, and the upper end of the first is plainly the larger. The comparison the claim makes needs nothing beyond those two blocks."
    },
    {
      "witness_key": "CQ-B-T5-04:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "The block gives the modelled temperature band for the 10 to 20 km interval, the figures the claim states."
    },
    {
      "witness_key": "CQ-B-T5-04:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:007"
      ],
      "rationale": "The block opens by saying no earthquakes are seen deeper than 20 km beneath that segment's axis, which is the claim."
    },
    {
      "witness_key": "CQ-B-T5-04:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:007"
      ],
      "rationale": "The same sentence offers higher temperatures below 20 km as what would hinder nucleation there, which is the explanation the claim reports."
    },
    {
      "witness_key": "CQ-B-T5-04:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:012",
        "page:9:block:035"
      ],
      "rationale": "The caption block attributes the isotherms to a simulated thermal model by reference marker and the cited reference entry resolves it to the lead author the claim names."
    },
    {
      "witness_key": "CQ-B-T5-05:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "The block says every sample from that segment is enriched in incompatible trace elements, gives the two element thresholds the claim quotes, and sets them against the southern segment's samples and ordinary ridge basalt."
    },
    {
      "witness_key": "CQ-B-T5-05:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:005"
      ],
      "rationale": "The block gives both calculated ranges in one sentence, the segment with the deep events against its southern neighbour, as the claim states them."
    },
    {
      "witness_key": "CQ-B-T5-05:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "The methods block gives all four proxy-by-proxy ranges, two per segment, and the claim reproduces them in the same pairing."
    },
    {
      "witness_key": "CQ-B-T5-05:c4",
      "source_support": "PARTIAL",
      "source_locators": [
        "page:5:block:005",
        "page:8:block:007"
      ],
      "rationale": "The cited blocks give both segments' ranges and say the southern segment's values are the lower, but neither states the size of the gap. Taking the figures as they stand, the factor is tenfold at the bottom of the two ranges and roughly four at the top, so the block supports a clear separation and not the order-of-magnitude figure the claim puts on it."
    },
    {
      "witness_key": "CQ-B-C-04:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rationale": "Both cited blocks tie the seismic recordings to the named cruise, one as the acquiring experiment and the other as the passive experiment conducted during it."
    },
    {
      "witness_key": "CQ-B-C-04:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:002",
        "page:2:block:002"
      ],
      "rationale": "The methods block dates the experiment to July and August of 2019 and the results block gives the same year, so both the year and the months the claim names are carried."
    },
    {
      "witness_key": "CQ-B-C-04:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rationale": "Each cited block puts nineteen ocean-bottom instruments in the network placed on the bottom, which is the count the claim gives."
    },
    {
      "witness_key": "CQ-B-C-05:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:002"
      ],
      "rationale": "The block names the settled account in its first sentence: carbon dioxide leaving the ascending melt beneath that segment."
    },
    {
      "witness_key": "CQ-B-C-05:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:002"
      ],
      "rationale": "The same sentence numbers it the fourth possibility and marks it the authors' preferred one, both halves of the claim."
    },
    {
      "witness_key": "CQ-B-C-05:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001",
        "page:3:block:002",
        "page:3:block:003",
        "page:4:block:002"
      ],
      "rationale": "Each cited block raises and then sets aside one rival account: a cold thick lithosphere, cooling by hydrothermal circulation, strain in mylonite shear zones, and magmatic-tectonic activity. Four blocks, four accounts, which is the count and the list the claim gives."
    },
    {
      "witness_key": "CQ-B-C-05:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:003"
      ],
      "rationale": "The block carries the whole chain the claim states: the volume change of degassing, locally high strain rates under extensional stress, and two to three bars of added pore pressure being enough to nucleate an event."
    }
  ],
  "questions": [
    {
      "question_id": "CQ-B-T1-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every required element names a supported claim: the cruise, the year and the count each have their own claim and each rests on a block that carries it.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "cruise_name",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "deployment_year",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "instrument_count",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T1-01:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T1-01:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T1-01:c3"
        }
      ]
    },
    {
      "question_id": "CQ-B-T1-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "All three elements name supported claims, the identifier from the article head and the two dates from the header block.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "article_doi",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "received_date",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "accepted_date",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:1:block:001",
        "page:1:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T1-02:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T1-02:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T1-02:c3"
        }
      ]
    },
    {
      "question_id": "CQ-B-T1-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "All four elements name supported claims. The first claim carries both the ridge and the ocean region in one sentence; the subsection labels and the southern neighbour's label have a claim each.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "study_area_name",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "ocean_region",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "subsection_labels",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "adjacent_segment_label",
          "row_index": 3,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:1:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T1-03:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T1-03:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T1-03:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-B-T1-03:c4"
        }
      ]
    },
    {
      "question_id": "CQ-B-T1-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Each of the three programs has its own supported claim and a fourth claim carries the download statement, so every element names a row.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "phase_picking_software",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "location_software",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "relocation_software",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "software_availability_source",
          "row_index": 3,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:6:block:002",
        "page:8:block:010",
        "page:7:block:004",
        "page:7:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T1-04:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T1-04:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T1-04:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-B-T1-04:c4"
        }
      ]
    },
    {
      "question_id": "CQ-B-T1-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "All four elements name supported claims. The first claim carries both the repository and what was put in it; the identifier and the route to the raw recordings have a claim each.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "repository_name",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "dataset_identifier",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "deposited_data_description",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "raw_data_access_route",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:8:block:008",
        "page:8:block:009"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T1-05:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T1-05:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T1-05:c3"
        }
      ]
    },
    {
      "question_id": "CQ-B-T2-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every element names a supported claim. The first claim carries an author and the tasks credited to them, the second the supervision, and the fifth the project design, which rests on a sentence running across the block boundary.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "author_name",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "contribution_role",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "supervision_relation",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "project_design_credit",
          "row_index": 4,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:10:block:045",
        "page:10:block:046"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T2-01:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T2-01:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T2-01:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-B-T2-01:c4"
        },
        {
          "row_index": 4,
          "witness_key": "CQ-B-T2-01:c5"
        },
        {
          "row_index": 5,
          "witness_key": "CQ-B-T2-01:c6"
        }
      ]
    },
    {
      "question_id": "CQ-B-T2-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every element names a supported claim. The first claim carries funder, grant references and the funded person together; the ship time has its own claim.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "funder_name",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "grant_identifier",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "funded_party",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "ship_time_funder",
          "row_index": 4,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:10:block:044"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T2-02:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T2-02:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T2-02:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-B-T2-02:c4"
        },
        {
          "row_index": 4,
          "witness_key": "CQ-B-T2-02:c5"
        }
      ]
    },
    {
      "question_id": "CQ-B-T2-03",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "Three elements name supported claims and one does not. The claim that places the core complex is the only one carrying that element and it is PARTIAL: its cited block puts the dome on the eastern side of the axis in the intersection subsection but says nothing about an outside corner, so on the protocol's rule it cannot name a semantic. The other three elements are carried by the opening claim and by the claim about the detachment's termination and inactivity.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "bounding_transform_names",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "segment_position",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "core_complex_location",
          "row_index": null,
          "absent_reason": "NOT_CAPTURED",
          "note": "The answer set states the dome's position, but the only claim carrying it is PARTIAL because its cited block does not carry the outside-corner descriptor, and no other claim of this question states where the dome sits. The answer declares no gap for this element."
        },
        {
          "semantic": "fault_relation",
          "row_index": 3,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001",
        "page:1:block:006",
        "page:2:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T2-03:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T2-03:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T2-03:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-B-T2-03:c4"
        }
      ]
    },
    {
      "question_id": "CQ-B-T2-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every element names a supported claim: the flank and the value in the first, the published source in the second, and the inference and the hosting layer together in the third.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "crustal_thickness_source",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "flank_identification",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "depth_inference",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "hosting_layer",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:2:block:006",
        "page:9:block:036",
        "page:7:block:011"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T2-04:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T2-04:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T2-04:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-B-T2-04:c4"
        }
      ]
    },
    {
      "question_id": "CQ-B-T2-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every element names a supported claim, the last two both resting on the claim that states what the ratios were used to work out and for which segments.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "ratio_pair_identity",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "ratio_source_study",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "sample_database_name",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "computation_purpose",
          "row_index": 3,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "target_segment_label",
          "row_index": 3,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:5:block:004",
        "page:8:block:006",
        "page:10:block:004",
        "page:8:block:005",
        "page:8:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T2-05:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T2-05:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T2-05:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-B-T2-05:c4"
        }
      ]
    },
    {
      "question_id": "CQ-B-T3-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every element names a supported claim. The half-rate claim carries the unit as well, and the attribution has its own claim resting on the reference entry.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "half_rate_value",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "full_rate_value",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "rate_unit",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "rate_source_attribution",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:1:block:005",
        "page:2:block:005",
        "page:9:block:019"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T3-01:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T3-01:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T3-01:c3"
        }
      ]
    },
    {
      "question_id": "CQ-B-T3-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every element names a supported claim. The third claim carries both counts, the seventeen that worked and the nineteen that were put down.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "recording_duration",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "instrument_spacing",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "usable_instrument_count",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "instrument_count",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T3-02:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T3-02:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T3-02:c3"
        }
      ]
    },
    {
      "question_id": "CQ-B-T3-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every element names a supported claim, the uncertainty value and its unit both coming from the claim that reports the average horizontal error after relocation.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "located_event_count",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "relocated_event_count",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "horizontal_uncertainty_value",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "uncertainty_unit",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:2:block:003",
        "page:6:block:005",
        "page:7:block:006",
        "page:7:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T3-03:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T3-03:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T3-03:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-B-T3-03:c4"
        }
      ]
    },
    {
      "question_id": "CQ-B-T3-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every element names a supported claim. The opening claim carries the range, its unit and the segment it belongs to; the proxy elements and the calculated status have a claim each.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "concentration_range",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "concentration_unit",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "segment_label",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "proxy_element",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "calculation_status",
          "row_index": 3,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:5:block:005",
        "page:1:block:001",
        "page:5:block:004",
        "page:8:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T3-04:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T3-04:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T3-04:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-B-T3-04:c4"
        }
      ]
    },
    {
      "question_id": "CQ-B-T3-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every element names a supported claim; the pressure, depth and temperature come from one sentence of the cited block and the model attribution from the reference entry.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "saturation_pressure",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "saturation_depth",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "saturation_temperature",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "solubility_model_source",
          "row_index": 3,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:5:block:006",
        "page:10:block:013"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T3-05:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T3-05:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T3-05:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-B-T3-05:c4"
        }
      ]
    },
    {
      "question_id": "CQ-B-T4-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every element names a supported claim. The count of rivals rests on the claim whose four cited blocks each raise and set aside one account.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "preferred_mechanism",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "alternative_count",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "preference_wording",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "mechanism_physical_basis",
          "row_index": 3,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:5:block:002",
        "page:3:block:001",
        "page:3:block:002",
        "page:3:block:003",
        "page:4:block:002",
        "page:5:block:003"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T4-01:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T4-01:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T4-01:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-B-T4-01:c4"
        }
      ]
    },
    {
      "question_id": "CQ-B-T4-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every element names a supported claim, all four resting on the same block. The morphological observations and the ground for declining the account are the same claim, because the block makes them one sentence.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "declined_explanation",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "rejection_evidence",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "comparison_setting",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "morphology_observation",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:3:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T4-02:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T4-02:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T4-02:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-B-T4-02:c4"
        }
      ]
    },
    {
      "question_id": "CQ-B-T4-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every element names a supported claim. The first claim carries both the declined account and the absence of active vents that is the ground for declining it.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "declined_explanation",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "rejection_evidence",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "conceded_observation",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "spatial_qualification",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:3:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T4-03:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T4-03:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T4-03:c3"
        }
      ]
    },
    {
      "question_id": "CQ-B-T4-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every element names a supported claim, all four drawn from the one block that carries the hedge, the spectral observation, the limitation and the stated need for more events.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "hedged_claim",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "supporting_observation",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "stated_limitation",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "future_requirement",
          "row_index": 3,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:5:block:008"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T4-04:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T4-04:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T4-04:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-B-T4-04:c4"
        }
      ]
    },
    {
      "question_id": "CQ-B-T4-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Both claims are supported and between them carry all five elements: the first the assumption and the way the authors flag it, the second the floor with its unit and the segment it applies to.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "method_assumption",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "caveat_wording",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "asserted_minimum",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "concentration_unit",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "segment_label",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:5:block:004",
        "page:8:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T4-05:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T4-05:c2"
        }
      ]
    },
    {
      "question_id": "CQ-B-T5-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every element names a supported claim. The first claim carries both the expected bound and the spreading rate it is read off; the observed depths and the segment come from the second.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "expected_depth_bound",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "observed_depth_range",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "spreading_rate_basis",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "segment_label",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:2:block:005",
        "page:2:block:006",
        "page:2:block:004"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T5-01:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T5-01:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T5-01:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-B-T5-01:c4"
        }
      ]
    },
    {
      "question_id": "CQ-B-T5-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every element names a supported claim. The value and its error are one claim, the observed depths another, and the inference and the hosting layer a third.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "crustal_thickness_value",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "thickness_uncertainty",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "observed_depth_range",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "depth_inference",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "hosting_layer",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:2:block:006",
        "page:7:block:011",
        "page:7:block:012"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T5-02:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T5-02:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T5-02:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-B-T5-02:c4"
        }
      ]
    },
    {
      "question_id": "CQ-B-T5-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every element names a supported claim. The new range and its unit come from the first claim, the previous maximum and the ridge it was reported at from the second.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "concentration_range",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "prior_maximum_value",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "prior_maximum_location",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "concentration_unit",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:5:block:005",
        "page:5:block:009",
        "page:10:block:004"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T5-03:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T5-03:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T5-03:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-B-T5-03:c4"
        }
      ]
    },
    {
      "question_id": "CQ-B-T5-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every element names a supported claim: the modelled band, the depth below which nothing is recorded, the temperature explanation for that silence, and the model's authorship.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "modelled_temperature_range",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "depth_cutoff",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "absence_explanation",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "thermal_model_source",
          "row_index": 3,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:3:block:001",
        "page:5:block:007",
        "page:7:block:012",
        "page:9:block:035"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T5-04:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T5-04:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T5-04:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-B-T5-04:c4"
        }
      ]
    },
    {
      "question_id": "CQ-B-T5-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every element names a supported claim. The first claim carries the two element thresholds, the segment they belong to and the segment they are set against; the concentration range comes from the second. The fourth claim, which puts an order of magnitude on the gap, is PARTIAL and names nothing, but no element depends on it.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "trace_element_threshold",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "concentration_range",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "segment_label",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "comparison_segment_label",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:5:block:004",
        "page:5:block:005",
        "page:8:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-T5-05:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-T5-05:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-T5-05:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-B-T5-05:c4"
        }
      ]
    },
    {
      "question_id": "CQ-B-C-01",
      "question_responsiveness": "NONE",
      "responsiveness_rationale": "The answer declares the reading has no answer here and makes no claim, so nothing names a semantic. Two of the four elements are genuinely absent from the reading and a third, the configuration detail the question asks for, is absent with them; the instrument count is a different case, since the reading does state it and this answer simply does not.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "sampling_rate_value",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading nowhere gives a sampling rate for the seafloor instruments."
        },
        {
          "semantic": "sensor_type",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading never describes the sensors inside the instruments, only that vertical components were analysed."
        },
        {
          "semantic": "instrument_configuration_detail",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading gives deployment facts such as count, spacing and duration but no detail of how the instruments were configured."
        },
        {
          "semantic": "instrument_count",
          "row_index": null,
          "absent_reason": "NOT_CAPTURED",
          "note": "The reading does state how many instruments were deployed, but this answer carries no claim at all, so no claim of this question states the count."
        }
      ],
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rows": []
    },
    {
      "question_id": "CQ-B-C-02",
      "question_responsiveness": "NONE",
      "responsiveness_rationale": "The answer declares the reading has no answer here and makes no claim, so nothing names a semantic. The largest magnitude and any identification of such an event are absent from the reading; the magnitude scale and the recording period are in the reading and are simply not stated by this answer.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "maximum_magnitude_value",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading gives the magnitude formula, the completeness magnitude and b values, but never the largest magnitude recorded during the deployment."
        },
        {
          "semantic": "magnitude_scale",
          "row_index": null,
          "absent_reason": "NOT_CAPTURED",
          "note": "The reading names the local magnitude scale used, but this answer carries no claim, so no claim of this question states it."
        },
        {
          "semantic": "event_identification",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading identifies no individual event of the deployment as the largest one."
        },
        {
          "semantic": "recording_period",
          "row_index": null,
          "absent_reason": "NOT_CAPTURED",
          "note": "The reading states the recording period, but this answer carries no claim, so no claim of this question states it."
        }
      ],
      "source_locators": [
        "page:8:block:002"
      ],
      "rows": []
    },
    {
      "question_id": "CQ-B-C-03",
      "question_responsiveness": "NONE",
      "responsiveness_rationale": "The answer declares the reading has no answer here and makes no claim, so nothing names a semantic. The running text says the worldwide compilation was assembled and points to a figure and a supplementary table for it, and the per-site depths and rates live only there; the site names are the exception, since the text does name several compiled sites and this answer states none.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "site_name",
          "row_index": null,
          "absent_reason": "NOT_CAPTURED",
          "note": "The methods text names several of the compiled sites, so the reading carries the element, but this answer carries no claim and states none of them."
        },
        {
          "semantic": "maximum_depth_value",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading states no maximum depth for any compiled site; the compiled depths are only in the figure and the supplementary table, which the question file's scope excludes."
        },
        {
          "semantic": "full_rate_value",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading states no opening rate for any compiled site, only the rate of its own study area, which is a different subject."
        },
        {
          "semantic": "depth_unit",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "With no per-site depth stated in the reading, no unit for one is stated either."
        }
      ],
      "source_locators": [
        "page:8:block:004"
      ],
      "rows": []
    },
    {
      "question_id": "CQ-B-C-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every required element names a supported claim: the expedition, the year and the count of recording units each have their own claim resting on a block that carries it.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "cruise_name",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "deployment_year",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "instrument_count",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-C-04:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-C-04:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-C-04:c3"
        }
      ]
    },
    {
      "question_id": "CQ-B-C-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Every element names a supported claim. The count of competitors rests on the claim whose four cited blocks each raise and set aside one account.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "preferred_mechanism",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "alternative_count",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "preference_wording",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "mechanism_physical_basis",
          "row_index": 3,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:5:block:002",
        "page:3:block:001",
        "page:3:block:002",
        "page:3:block:003",
        "page:4:block:002",
        "page:5:block:003"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-B-C-05:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-B-C-05:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-B-C-05:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-B-C-05:c4"
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
