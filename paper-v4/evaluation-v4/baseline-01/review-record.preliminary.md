# Malleus paper v4 source-grounded review record, protocol v3.2, in-context answer set

This is baseline-01's blank record, written by
`paper-v4/experiment-v4/baseline-01/build_review_inputs.py` from the frozen v3
template. The question ids are this cell's frozen competency question file's, in
that file's order. The claim counts are the producer's answer file's.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

Write one `witnesses` entry per claim the answer file cites,
135 in all. Claim ids are unique, so no witness is shared and
none is judged twice. Claims: 3 claims for `CQ-T1-01`, 4 for `CQ-T1-02`, 2 for `CQ-T1-03`, 3 for
`CQ-T1-04`, 1 for `CQ-T1-05`, 5 for `CQ-T2-01`, 5 for `CQ-T2-02`, 4 for
`CQ-T2-03`, 5 for `CQ-T2-04`, 5 for `CQ-T2-05`, 6 for `CQ-T3-01`, 6 for
`CQ-T3-02`, 5 for `CQ-T3-03`, 5 for `CQ-T3-04`, 7 for `CQ-T3-05`, 5 for
`CQ-T4-01`, 8 for `CQ-T4-02`, 5 for `CQ-T4-03`, 5 for `CQ-T4-04`, 5 for
`CQ-T4-05`, 6 for `CQ-T5-01`, 6 for `CQ-T5-02`, 7 for `CQ-T5-03`, 5 for
`CQ-T5-04`, 8 for `CQ-T5-05`, 0 for `CQ-C-01`, 0 for `CQ-C-02`, 0 for
`CQ-C-03`, 4 for `CQ-C-04`, 5 for `CQ-C-05`,
135 in all.

Three things the validator derives or forbids, so that writing them wrong is
refused rather than recorded:

- `question_responsiveness` is derived from `coverage`. Write the label the
  derivation produces, `COVERED` when every required semantic names a row,
  `NONE` when none does, `PARTIAL` otherwise. A label the derivation does not
  produce is refused.
- `assembly` is `NOT_APPLICABLE` on this surface, on every question. A prose
  answer always assembles, so the descriptor would be constant, and a constant
  token in a comparison table reads as a grade.
- A witness must cite every block its claim cites in the answer file. Support is
  judged against the cited block, not the article around it.

No witness carries `resolution` on this surface and every locator is a reading
block id. Copy no source passage into this record beyond the locator, and add no
numerical aggregate.

```json
{
  "schema": "malleus.paper-v4.source-grounded-review/v3.2",
  "status": "PRELIMINARY_COMPLETE",
  "inputs": {
    "review_protocol_sha256": "sha256:5dfd59f4aa479dd72738e2eb55653ee3e84e60886de4cccbcc0a8e66d06e55cd",
    "review_input_manifest_sha256": "sha256:86a46ad5de3e0e011a33d49c7fc94bfd71187af103162b06bb71ab09295398e8"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-preliminary-baseline-01",
    "completed_at": "2026-09-12T05:43:12Z"
  },
  "witnesses": [
    {
      "witness_key": "CQ-T1-01:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rationale": "Both blocks name the SMARTIES cruise as the setting in which the seismometer network was put out, and the results block ties that network to the microseismicity data this study works from."
    },
    {
      "witness_key": "CQ-T1-01:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:002"
      ],
      "rationale": "The methods block opens by dating the passive experiment on that cruise to the two months and the year the claim asserts, and nothing more."
    },
    {
      "witness_key": "CQ-T1-01:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "The block lists what the network covered: the eastern stretch of the transform, the intersection, and a length of ridge axis. The claim carries the same three and drops the transform's figure."
    },
    {
      "witness_key": "CQ-T1-02:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rationale": "Nineteen instruments is stated in both blocks, once as the network that acquired the data and once as the network that was put out."
    },
    {
      "witness_key": "CQ-T1-02:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rationale": "Seventeen usable instruments fed the automatic trigger in both blocks, and the methods block is the one that adds the vertical components."
    },
    {
      "witness_key": "CQ-T1-02:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rationale": "Both blocks give the separation between instruments that the claim quotes."
    },
    {
      "witness_key": "CQ-T1-02:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:007"
      ],
      "rationale": "The bathymetric map caption gives its own symbol to the single instrument that yielded no record, which is what the claim reports."
    },
    {
      "witness_key": "CQ-T1-03:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:006"
      ],
      "rationale": "The masthead lines in that block carry the acceptance date the claim gives."
    },
    {
      "witness_key": "CQ-T1-03:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:006"
      ],
      "rationale": "The same pair of lines carries the date of receipt."
    },
    {
      "witness_key": "CQ-T1-04:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:008"
      ],
      "rationale": "The availability block states that the catalogue and the picked arrivals generated by this study went into Zenodo."
    },
    {
      "witness_key": "CQ-T1-04:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:008",
        "page:8:block:009"
      ],
      "rationale": "The identifier is split across the block boundary; read in order the two blocks give exactly the identifier the claim quotes."
    },
    {
      "witness_key": "CQ-T1-04:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:008"
      ],
      "rationale": "The same block routes the raw records and the cruise reports to a campaign website and says they can be requested for scientific purposes."
    },
    {
      "witness_key": "CQ-T1-05:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "The results block states the unbroken recording span, in the figure and the unit the claim gives, and that is the whole of the claim."
    },
    {
      "witness_key": "CQ-T2-01:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "The block names the intersection segment RC1 and says a detachment fault bounds it on its eastern side."
    },
    {
      "witness_key": "CQ-T2-01:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "The same sentence has the fault dipping west and carrying a prominent core complex."
    },
    {
      "witness_key": "CQ-T2-01:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "The block places that core complex on the eastern side of the ridge axis."
    },
    {
      "witness_key": "CQ-T2-01:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:007"
      ],
      "rationale": "The figure caption puts the core complex on the outside corner, which is what the claim attributes to it."
    },
    {
      "witness_key": "CQ-T2-01:c5",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:005"
      ],
      "rationale": "The block calls the intersection segment amagmatic and gives it the name RC1 in the same passage."
    },
    {
      "witness_key": "CQ-T2-02:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:004"
      ],
      "rationale": "The location section names NonLinLoc and its oct-tree search as what produced the first hypocentres."
    },
    {
      "witness_key": "CQ-T2-02:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:004"
      ],
      "rationale": "The same sentence says the maximum likelihood solution was taken as the preferred one."
    },
    {
      "witness_key": "CQ-T2-02:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:006"
      ],
      "rationale": "The block attributes double-difference relocation to hypoDD, and relocation by its own name presupposes an earlier location step."
    },
    {
      "witness_key": "CQ-T2-02:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:002"
      ],
      "rationale": "The results block puts the two steps in sequence: hypocentres obtained first, then relocated."
    },
    {
      "witness_key": "CQ-T2-02:c5",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:006",
        "page:7:block:007"
      ],
      "rationale": "The first block gives the count of well-constrained events entering relocation and the second the count that came out and displaced the earlier positions."
    },
    {
      "witness_key": "CQ-T2-03:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:002"
      ],
      "rationale": "The block reports the extinct field on the eastern flank of the first non-transform discontinuity."
    },
    {
      "witness_key": "CQ-T2-03:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:002"
      ],
      "rationale": "The same sentence calls its position relatively far from the axial valley as it now stands."
    },
    {
      "witness_key": "CQ-T2-03:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:002"
      ],
      "rationale": "The block draws that exact consequence, that the field would not reach the lithosphere under the RC2 axis."
    },
    {
      "witness_key": "CQ-T2-03:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:007"
      ],
      "rationale": "The map caption reports an inactive mound from the Nautile dives and gives it its own marker. The block does not relate it to the extinct field on NTD1, but it identifies it independently, so calling it a further feature asserts nothing the block denies."
    },
    {
      "witness_key": "CQ-T2-04:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "The block credits the crustal thickness to seismic refraction work under a numbered citation."
    },
    {
      "witness_key": "CQ-T2-04:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:9:block:036"
      ],
      "rationale": "The reference list entry under that number gives the author pair, the journal and the subject the claim describes."
    },
    {
      "witness_key": "CQ-T2-04:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "The thickness figure and its error are in the block."
    },
    {
      "witness_key": "CQ-T2-04:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "The same sentence assigns the value to the western flank and to crust of that age."
    },
    {
      "witness_key": "CQ-T2-04:c5",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:011"
      ],
      "rationale": "The schematic caption repeats the same thickness for the crust beneath RC2."
    },
    {
      "witness_key": "CQ-T2-05:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "The funding paragraph names that advanced grant agreement and its number."
    },
    {
      "witness_key": "CQ-T2-05:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "The same clause attaches the agreement to the initials S.C.S."
    },
    {
      "witness_key": "CQ-T2-05:c3",
      "source_support": "PARTIAL",
      "source_locators": [
        "page:10:block:045",
        "page:11:block:002"
      ],
      "rationale": "The contributions block shows those initials among the credited authors and the correspondence block names Satish C. Singh as a corresponding author. Neither block says the initials stand for that name, so the identification the claim makes rests on inference and is not carried by the cited blocks."
    },
    {
      "witness_key": "CQ-T2-05:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "The funding paragraph routes the Seventh Framework Programme support to the same initials."
    },
    {
      "witness_key": "CQ-T2-05:c5",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:10:block:044"
      ],
      "rationale": "The two national grants and the provincial grant are all credited to Z.Y. in the block, with the numbers the claim quotes."
    },
    {
      "witness_key": "CQ-T3-01:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:004"
      ],
      "rationale": "The block's second key observation is deep microseismicity in that band beneath the RC2 axis."
    },
    {
      "witness_key": "CQ-T3-01:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "The block gives the narrower band for the axial events and calls them the deepest so far at a slow-spreading centre."
    },
    {
      "witness_key": "CQ-T3-01:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:012"
      ],
      "rationale": "The schematic caption states the band and refers it to the sea floor."
    },
    {
      "witness_key": "CQ-T3-01:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:012",
        "page:1:block:004"
      ],
      "rationale": "The caption quotes kilometres with the abbreviated reference surface, and the introduction block spells out what that abbreviation means."
    },
    {
      "witness_key": "CQ-T3-01:c5",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:003",
        "page:2:block:006"
      ],
      "rationale": "Both blocks are first person about locating and observing these events, so the depths are this study's own rather than carried in from another catalogue."
    },
    {
      "witness_key": "CQ-T3-01:c6",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:009",
        "page:8:block:001"
      ],
      "rationale": "The first block runs the depths through five velocity models and the second sums the tests up as showing the deep events required by the data and not artifacts, referring back to the run in which depths were not held fixed."
    },
    {
      "witness_key": "CQ-T3-02:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:005",
        "page:1:block:001"
      ],
      "rationale": "The results block gives the calculated range for the melts generated along RC2 and the abstract attaches the same range to the primary melts."
    },
    {
      "witness_key": "CQ-T3-02:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:005"
      ],
      "rationale": "The unit in the block is weight percent."
    },
    {
      "witness_key": "CQ-T3-02:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004",
        "page:8:block:006"
      ],
      "rationale": "Both blocks describe a calculation from trace element abundances through fixed volatile to non-volatile ratios, not a measurement of the melts."
    },
    {
      "witness_key": "CQ-T3-02:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "The methods block gives the two proxy ranges for that segment as the claim states them."
    },
    {
      "witness_key": "CQ-T3-02:c5",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004",
        "page:8:block:007"
      ],
      "rationale": "The correction for fractional crystallisation is in the first block and the reference to melts in equilibrium with that olivine composition in the second."
    },
    {
      "witness_key": "CQ-T3-02:c6",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "The block draws the at-least reading for the primary melts of that segment itself."
    },
    {
      "witness_key": "CQ-T3-03:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "The block gives the pre-eruptive range for that segment."
    },
    {
      "witness_key": "CQ-T3-03:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "Weight percent is the unit the block uses for that range."
    },
    {
      "witness_key": "CQ-T3-03:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006",
        "page:8:block:006"
      ],
      "rationale": "Both blocks call the figure estimated, and the methods block names the ratio calculation behind it, so it is not presented as measured."
    },
    {
      "witness_key": "CQ-T3-03:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:006"
      ],
      "rationale": "The two proxy ranges for that segment are in the block."
    },
    {
      "witness_key": "CQ-T3-03:c5",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:006"
      ],
      "rationale": "The block sets primary melts, in equilibrium with their source, against pre-eruptive melts that have undergone crystallisation."
    },
    {
      "witness_key": "CQ-T3-04:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:007",
        "page:3:block:004"
      ],
      "rationale": "Both the methods block and the map caption give the updated average horizontal uncertainty after relocation."
    },
    {
      "witness_key": "CQ-T3-04:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:007"
      ],
      "rationale": "The figure is quoted in kilometres in that block."
    },
    {
      "witness_key": "CQ-T3-04:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:007"
      ],
      "rationale": "The block states that the relocated events replaced the earlier positions in the final catalogue, which is the set that figure describes."
    },
    {
      "witness_key": "CQ-T3-04:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:007"
      ],
      "rationale": "The counts along the ridge and along the transform are in the same sentence as the uncertainty."
    },
    {
      "witness_key": "CQ-T3-04:c5",
      "source_support": "PARTIAL",
      "source_locators": [
        "page:7:block:001",
        "page:6:block:005"
      ],
      "rationale": "The two blocks give the count of located events and the mean horizontal error, which is the substance of the claim. Neither places that error before the relocation step; relocation is described in a later block, so the ordering the claim asserts is not carried by the evidence it rests on."
    },
    {
      "witness_key": "CQ-T3-05:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "The block puts carbon dioxide saturation of the melt at that pressure."
    },
    {
      "witness_key": "CQ-T3-05:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "The same parenthesis equates that pressure with the depth the claim gives."
    },
    {
      "witness_key": "CQ-T3-05:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "The temperature is stated in the same sentence."
    },
    {
      "witness_key": "CQ-T3-05:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "The block quotes the pressure in gigapascals and the temperature in degrees Celsius."
    },
    {
      "witness_key": "CQ-T3-05:c5",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "The sentence opens by saying a solubility model was used, so the conditions are model output rather than measured values."
    },
    {
      "witness_key": "CQ-T3-05:c6",
      "source_support": "PARTIAL",
      "source_locators": [
        "page:10:block:013",
        "page:10:block:014"
      ],
      "rationale": "The two reference blocks identify that numbered entry as a carbon dioxide solubility model by Eguchi and Dasgupta, which the claim gets right. They do not carry the further point that the saturation calculation is the one citing that entry; the numbered citation sits in the results block, which this witness does not rest on."
    },
    {
      "witness_key": "CQ-T3-05:c7",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "The block conditions the calculation on melt above that concentration and says it would begin to degas from there."
    },
    {
      "witness_key": "CQ-T4-01:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:002"
      ],
      "rationale": "The block states degassing from the ascending melt as the authors' preferred account of the deep microseismicity beneath that segment."
    },
    {
      "witness_key": "CQ-T4-01:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:002"
      ],
      "rationale": "The same sentence numbers it the fourth of the possibilities weighed."
    },
    {
      "witness_key": "CQ-T4-01:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:1:block:001",
        "page:5:block:003"
      ],
      "rationale": "Both blocks put the claim in the suggesting voice rather than asserting it as shown."
    },
    {
      "witness_key": "CQ-T4-01:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:003"
      ],
      "rationale": "The block lays out the chain from volume change through extensional stress and locally high strain rates to deep earthquakes in the mantle."
    },
    {
      "witness_key": "CQ-T4-01:c5",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:003"
      ],
      "rationale": "The pore pressure figure and the triggering point are in the block."
    },
    {
      "witness_key": "CQ-T4-02:c1",
      "source_support": "PARTIAL",
      "source_locators": [
        "page:4:block:002"
      ],
      "rationale": "The block introduces magmatic-tectonic activity as the third possibility and describes melt movement raising strain rates and breaking the ductile lower crust, which the claim gets right. It does not carry the setting aside; that comes later, so the claim's framing of this mechanism as declined is not supported by the block it rests on."
    },
    {
      "witness_key": "CQ-T4-02:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:002"
      ],
      "rationale": "The three analogues are named in the block."
    },
    {
      "witness_key": "CQ-T4-02:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:001"
      ],
      "rationale": "The block closes the argument by stating that the melt movement mechanism does not apply to these earthquakes."
    },
    {
      "witness_key": "CQ-T4-02:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:003"
      ],
      "rationale": "The eruption association and the strain comparison against a normal ridge segment are both in the block."
    },
    {
      "witness_key": "CQ-T4-02:c5",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:003"
      ],
      "rationale": "The block contrasts the thickened crust of one setting and the cold lithosphere of the other with a mid-ocean ridge."
    },
    {
      "witness_key": "CQ-T4-02:c6",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:003"
      ],
      "rationale": "The block denies a current eruption in the axial valley on the two grounds the claim names."
    },
    {
      "witness_key": "CQ-T4-02:c7",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:4:block:003",
        "page:5:block:001"
      ],
      "rationale": "The alignment and its parallelism with the axial faults are in the first block, and the sentence it breaks off in finishes in the second with the comparison the claim makes."
    },
    {
      "witness_key": "CQ-T4-02:c8",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:001"
      ],
      "rationale": "The block puts the shallow off-axis events down to off-axis magmatism in the crust."
    },
    {
      "witness_key": "CQ-T4-03:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "The block states the assumption the method rests on in the terms the claim uses."
    },
    {
      "witness_key": "CQ-T4-03:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004",
        "page:8:block:006"
      ],
      "rationale": "The caveat sits directly beside the ratio calculation of primary melt content in the first block, and the second block carries out that calculation."
    },
    {
      "witness_key": "CQ-T4-03:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004",
        "page:8:block:006"
      ],
      "rationale": "Both blocks give the two ratios with their spreads."
    },
    {
      "witness_key": "CQ-T4-03:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "The block credits the global trends to rare undegassed basalts and olivine melt inclusions."
    },
    {
      "witness_key": "CQ-T4-03:c5",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004",
        "page:5:block:005"
      ],
      "rationale": "The first block calculates the melt content for that segment immediately after stating the caveat and the second gives the enriched result, so the claim the caveat qualifies is the one this witness names."
    },
    {
      "witness_key": "CQ-T4-04:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:002"
      ],
      "rationale": "The block says outright that no active vents have been seen on that segment's axis to date."
    },
    {
      "witness_key": "CQ-T4-04:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:002"
      ],
      "rationale": "What the block states is a denial of observation, not an assertion of presence."
    },
    {
      "witness_key": "CQ-T4-04:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:002"
      ],
      "rationale": "The block fixes the scope of that denial to the axis of that segment."
    },
    {
      "witness_key": "CQ-T4-04:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:002"
      ],
      "rationale": "The only field the block names nearby is extinct and sits on the eastern flank of the first discontinuity."
    },
    {
      "witness_key": "CQ-T4-04:c5",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:002"
      ],
      "rationale": "The block opens with the hydrothermal cooling hypothesis and uses the absence to dispose of it, closing on magmatism and a hot mantle."
    },
    {
      "witness_key": "CQ-T4-05:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:008"
      ],
      "rationale": "The spectral finding and the frequency threshold are both in the block."
    },
    {
      "witness_key": "CQ-T4-05:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:008"
      ],
      "rationale": "The block draws the long-period reading as an implication of that finding."
    },
    {
      "witness_key": "CQ-T4-05:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:008"
      ],
      "rationale": "The block's next sentence is the qualification the claim reports."
    },
    {
      "witness_key": "CQ-T4-05:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:008"
      ],
      "rationale": "The block says more events would be needed to study their source characteristics in future."
    },
    {
      "witness_key": "CQ-T4-05:c5",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:008"
      ],
      "rationale": "The block opens by likening the proposed nucleation to rapid degassing beneath active volcanoes and ties that to deep long-period events."
    },
    {
      "witness_key": "CQ-T5-01:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:005"
      ],
      "rationale": "The block gives the calculated range for the melts generated along that segment, which is the figure the claim quotes for the primary melt."
    },
    {
      "witness_key": "CQ-T5-01:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:005"
      ],
      "rationale": "The same sentence sets that enrichment against the much lower values of the neighbouring segment."
    },
    {
      "witness_key": "CQ-T5-01:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:004"
      ],
      "rationale": "The depth band beneath that axis is the block's second key observation."
    },
    {
      "witness_key": "CQ-T5-01:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005",
        "page:2:block:006"
      ],
      "rationale": "The first block gives the maximum depth expected at this spreading rate and the second says the observed depths far exceed it."
    },
    {
      "witness_key": "CQ-T5-01:c5",
      "source_support": "PARTIAL",
      "source_locators": [
        "page:5:block:006"
      ],
      "rationale": "The block carries the depth at which degassing would start and the authors' own word that this agrees with the observed deep microseismicity. It does not carry the claim's placement of that onset above the earthquake band; the onset depth the block gives is greater than the band's lower limit, so that part of the statement is not supported."
    },
    {
      "witness_key": "CQ-T5-01:c6",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:009"
      ],
      "rationale": "The block says continued degassing during ascent produces earthquakes in the mantle over that depth range."
    },
    {
      "witness_key": "CQ-T5-02:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:005"
      ],
      "rationale": "The block gives the calculated range for the melts of that segment."
    },
    {
      "witness_key": "CQ-T5-02:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:005"
      ],
      "rationale": "The same sentence gives the other segment's range, and the block names that segment, which is the one the claim identifies."
    },
    {
      "witness_key": "CQ-T5-02:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:005",
        "page:8:block:007"
      ],
      "rationale": "The first block calls the melts of the deep-earthquake segment significantly enriched against the other, which is the comparison the claim reports, and the second gives both segments' primary melt figures."
    },
    {
      "witness_key": "CQ-T5-02:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "The rubidium-route values for both segments are in the block."
    },
    {
      "witness_key": "CQ-T5-02:c5",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "The barium-route values for both segments are in the block."
    },
    {
      "witness_key": "CQ-T5-02:c6",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004"
      ],
      "rationale": "The block gives the trace element enrichment of that segment's samples against the southern segment and normal basalts, with both thresholds."
    },
    {
      "witness_key": "CQ-T5-03:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "The block ties the full spreading rate to an expected maximum earthquake depth under that limit."
    },
    {
      "witness_key": "CQ-T5-03:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "The block names the core complex as one of the two places where that range holds, with its own limit."
    },
    {
      "witness_key": "CQ-T5-03:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "The block gives the limit beneath the southern discontinuity and calls it expected for a slow-slipping one."
    },
    {
      "witness_key": "CQ-T5-03:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "The block gives the axial depths for that segment and says they far exceed the suggested maximum."
    },
    {
      "witness_key": "CQ-T5-03:c5",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:006"
      ],
      "rationale": "The block calls them the deepest documented so far at a slow-spreading centre."
    },
    {
      "witness_key": "CQ-T5-03:c6",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "The block's sentence is exclusive: only those two places show the expected range."
    },
    {
      "witness_key": "CQ-T5-03:c7",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:005"
      ],
      "rationale": "The block closes on the brittle lithosphere being at most that thick at the segment boundaries."
    },
    {
      "witness_key": "CQ-T5-04:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:003",
        "page:7:block:008"
      ],
      "rationale": "Both blocks state the four categories and the first gives their labels."
    },
    {
      "witness_key": "CQ-T5-04:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:003"
      ],
      "rationale": "The block says the first two are of good quality and are used for interpretation."
    },
    {
      "witness_key": "CQ-T5-04:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:008"
      ],
      "rationale": "The three criteria are listed in the block in the terms the claim summarises."
    },
    {
      "witness_key": "CQ-T5-04:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:008"
      ],
      "rationale": "The block assigns all the criteria to the first category, two to the middle pair and one to the last."
    },
    {
      "witness_key": "CQ-T5-04:c5",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:7:block:008"
      ],
      "rationale": "The share meeting at least two criteria is stated in the block."
    },
    {
      "witness_key": "CQ-T5-05:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "The block opens with the cold and thick lithosphere explanation, its boundary depth and the ridge it was proposed for, and then turns against it."
    },
    {
      "witness_key": "CQ-T5-05:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "The three morphological features are listed in the block as indicating a magmatic segment."
    },
    {
      "witness_key": "CQ-T5-05:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "The block adds the valley floor highs, the ridge-parallel faults and the basalts observed on the sea floor."
    },
    {
      "witness_key": "CQ-T5-05:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "The block draws the contrast with the smooth amagmatic morphology of the ridge where the lithosphere is cold and thick."
    },
    {
      "witness_key": "CQ-T5-05:c5",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "The off-axis shallow events west of that axis and their depth limit are in the block."
    },
    {
      "witness_key": "CQ-T5-05:c6",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "The block reads those events as keeping the boundary shallow out to the crustal age the claim gives."
    },
    {
      "witness_key": "CQ-T5-05:c7",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "The block cites the events beneath the southern discontinuity as a normal boundary depth, much shallower than beneath the deep-earthquake segment."
    },
    {
      "witness_key": "CQ-T5-05:c8",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:3:block:001"
      ],
      "rationale": "The thermal modelling figures and the hot mantle conclusion close the block."
    },
    {
      "witness_key": "CQ-C-04:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:002",
        "page:2:block:002"
      ],
      "rationale": "Both blocks give the nineteen instruments of the network that was put on the sea floor for this experiment."
    },
    {
      "witness_key": "CQ-C-04:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:002",
        "page:2:block:002"
      ],
      "rationale": "Both blocks give the spacing between instruments."
    },
    {
      "witness_key": "CQ-C-04:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:6:block:002",
        "page:2:block:002"
      ],
      "rationale": "The methods block names the vertical components of the seventeen usable instruments and the results block gives the same count for automatic detection."
    },
    {
      "witness_key": "CQ-C-04:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:2:block:007"
      ],
      "rationale": "The map caption marks the single instrument that produced no record."
    },
    {
      "witness_key": "CQ-C-05:c1",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:005",
        "page:1:block:001"
      ],
      "rationale": "The results block gives the calculated range for the melts of that segment and the abstract attaches the same range to the primary melts."
    },
    {
      "witness_key": "CQ-C-05:c2",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:005"
      ],
      "rationale": "Weight percent is the unit in the block."
    },
    {
      "witness_key": "CQ-C-05:c3",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004",
        "page:8:block:007"
      ],
      "rationale": "Both blocks describe a calculation from trace element abundances rather than a direct measurement of the melts."
    },
    {
      "witness_key": "CQ-C-05:c4",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:8:block:007"
      ],
      "rationale": "The two route values for that segment are in the block."
    },
    {
      "witness_key": "CQ-C-05:c5",
      "source_support": "SUPPORTED",
      "source_locators": [
        "page:5:block:004",
        "page:8:block:007"
      ],
      "rationale": "The correction for fractional crystallisation is in the first block and the reference to melts in equilibrium with that olivine composition in the second."
    }
  ],
  "questions": [
    {
      "question_id": "CQ-T1-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The first claim names the cruise, names the seismometer network and ties that network's records to this study, so all three elements sit in one supported claim about the question's own subject.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "campaign_name",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "observing_system",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "data_acquisition",
          "row_index": 0,
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
          "witness_key": "CQ-T1-01:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T1-01:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T1-01:c3"
        }
      ]
    },
    {
      "question_id": "CQ-T1-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The first claim gives the count, names the instruments and states that the network was put out, which covers the three elements for this experiment.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "instrument_count",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "observing_system",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "deployment_event",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002",
        "page:2:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-T1-02:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T1-02:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T1-02:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-T1-02:c4"
        }
      ]
    },
    {
      "question_id": "CQ-T1-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The first claim names the article, the acceptance and the date in one sentence, all three about this article.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "publication_record",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "acceptance_event",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "calendar_date",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:1:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-T1-03:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T1-03:c2"
        }
      ]
    },
    {
      "question_id": "CQ-T1-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The first claim names the deposited dataset and the repository; the second gives the identifier. Both are supported and both concern this study's deposit.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "dataset_record",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "repository_name",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "persistent_identifier",
          "row_index": 1,
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
          "witness_key": "CQ-T1-04:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T1-04:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T1-04:c3"
        }
      ]
    },
    {
      "question_id": "CQ-T1-05",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "Three elements come from the one claim. The observing system is absent because no claim states it for this recording, and the surface could have carried it.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "recording_interval",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "duration_value",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "time_unit",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "observing_system",
          "row_index": null,
          "absent_reason": "NOT_CAPTURED",
          "note": "The single claim states only the span and its unit. No claim names the instruments or the network that did the recording, and neither does the answer's prose, although the block the claim cites carries that fact and the answer declares no gap for this question."
        }
      ],
      "source_locators": [
        "page:2:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-T1-05:c1"
        }
      ]
    },
    {
      "question_id": "CQ-T2-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The first claim names the subsection and the bounding relation, the second the detachment and the core complex it carries, the third the side of the axis. All are about the same subsection.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "named_subsection",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "structural_feature",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "bounding_relation",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "side_of_axis",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:1:block:005",
        "page:2:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-T2-01:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T2-01:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T2-01:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-T2-01:c4"
        },
        {
          "row_index": 4,
          "witness_key": "CQ-T2-01:c5"
        }
      ]
    },
    {
      "question_id": "CQ-T2-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One supported claim per element: the first program, the second program, their order, and the final catalogue the relocated events entered.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "initial_location_method",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "relocation_method",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "method_sequence",
          "row_index": 3,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "earthquake_catalog",
          "row_index": 4,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:7:block:004",
        "page:7:block:006",
        "page:2:block:002",
        "page:7:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-T2-02:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T2-02:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T2-02:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-T2-02:c4"
        },
        {
          "row_index": 4,
          "witness_key": "CQ-T2-02:c5"
        }
      ]
    },
    {
      "question_id": "CQ-T2-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The first claim names the extinct field and its host discontinuity; the second gives its position relative to the present-day axial valley.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "named_feature",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "host_discontinuity",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "spatial_relation",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "present_day_axis",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:3:block:002",
        "page:2:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-T2-03:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T2-03:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T2-03:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-T2-03:c4"
        }
      ]
    },
    {
      "question_id": "CQ-T2-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The second claim identifies the earlier study, the third gives the thickness, the fourth the flank and the age. Each concerns the thickness adopted for this study area.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "source_study",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "crustal_thickness_claim",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "location_relation",
          "row_index": 3,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "crustal_age",
          "row_index": 3,
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
          "witness_key": "CQ-T2-04:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T2-04:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T2-04:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-T2-04:c4"
        },
        {
          "row_index": 4,
          "witness_key": "CQ-T2-04:c5"
        }
      ]
    },
    {
      "question_id": "CQ-T2-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The first claim carries the funding statement's record and the grant's identifier; the second carries the individual, by initials, and the attribution of that agreement to them. The claim that expands the initials into a full name is only partially supported, so it names nothing here.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "funding_record",
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
          "semantic": "person",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "attribution_relation",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:10:block:044",
        "page:10:block:045",
        "page:11:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-T2-05:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T2-05:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T2-05:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-T2-05:c4"
        },
        {
          "row_index": 4,
          "witness_key": "CQ-T2-05:c5"
        }
      ]
    },
    {
      "question_id": "CQ-T3-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The first claim carries the band, its unit and its subject, the axis of the magmatic segment; the fifth states the depths were located in this study; the fourth states the reference surface.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "length_unit",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "quantity_subject",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "measurement_status",
          "row_index": 4,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "depth_reference_surface",
          "row_index": 3,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:2:block:004",
        "page:2:block:006",
        "page:7:block:012",
        "page:1:block:004",
        "page:2:block:003",
        "page:7:block:009",
        "page:8:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-T3-01:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T3-01:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T3-01:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-T3-01:c4"
        },
        {
          "row_index": 4,
          "witness_key": "CQ-T3-01:c5"
        },
        {
          "row_index": 5,
          "witness_key": "CQ-T3-01:c6"
        }
      ]
    },
    {
      "question_id": "CQ-T3-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The first claim gives the range and its subject, the primary melts of the studied segment; the second the unit; the third that the figure is calculated.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 0,
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
          "semantic": "quantity_subject",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "calculated_or_measured_status",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:5:block:005",
        "page:1:block:001",
        "page:5:block:004",
        "page:8:block:006",
        "page:8:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-T3-02:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T3-02:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T3-02:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-T3-02:c4"
        },
        {
          "row_index": 4,
          "witness_key": "CQ-T3-02:c5"
        },
        {
          "row_index": 5,
          "witness_key": "CQ-T3-02:c6"
        }
      ]
    },
    {
      "question_id": "CQ-T3-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The first claim gives the range and names the melt stage as pre-eruptive for the studied segment; the second the unit; the third that it is an estimate.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 0,
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
          "semantic": "melt_stage",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "estimation_status",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:5:block:006",
        "page:8:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-T3-03:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T3-03:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T3-03:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-T3-03:c4"
        },
        {
          "row_index": 4,
          "witness_key": "CQ-T3-03:c5"
        }
      ]
    },
    {
      "question_id": "CQ-T3-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The first claim gives the figure and names its subject, the catalogue after relocation; the second the unit; the third that it was derived from this study's own relocated catalogue; the fourth the set of events it describes.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "length_unit",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "quantity_subject",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "derivation_status",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "event_set",
          "row_index": 3,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:7:block:007",
        "page:3:block:004",
        "page:7:block:001",
        "page:6:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-T3-04:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T3-04:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T3-04:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-T3-04:c4"
        },
        {
          "row_index": 4,
          "witness_key": "CQ-T3-04:c5"
        }
      ]
    },
    {
      "question_id": "CQ-T3-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The first claim gives the saturation pressure and its subject, the melt; the fourth gives both units; the fifth states the conditions come from a solubility model. The claim identifying that model is only partially supported and names nothing here.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "pressure_unit",
          "row_index": 3,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "temperature_unit",
          "row_index": 3,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "quantity_subject",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "model_derived_status",
          "row_index": 4,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:5:block:006",
        "page:10:block:013",
        "page:10:block:014"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-T3-05:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T3-05:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T3-05:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-T3-05:c4"
        },
        {
          "row_index": 4,
          "witness_key": "CQ-T3-05:c5"
        },
        {
          "row_index": 5,
          "witness_key": "CQ-T3-05:c6"
        },
        {
          "row_index": 6,
          "witness_key": "CQ-T3-05:c7"
        }
      ]
    },
    {
      "question_id": "CQ-T4-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The first claim carries the causal account, the preference and the subject, the deep earthquakes; the third carries the strength of the claim.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "causal_claim",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "preferred_disposition",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "epistemic_modality",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "claim_subject",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:5:block:002",
        "page:1:block:001",
        "page:5:block:003"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-T4-01:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T4-01:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T4-01:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-T4-01:c4"
        },
        {
          "row_index": 4,
          "witness_key": "CQ-T4-01:c5"
        }
      ]
    },
    {
      "question_id": "CQ-T4-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The third claim names the melt movement mechanism, its declining and the earthquakes it was declined for; the fourth gives one stated ground. The first claim describes the mechanism but is only partially supported, since the block it rests on introduces it without declining it.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "candidate_mechanism",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "declined_disposition",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "stated_ground",
          "row_index": 3,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "claim_subject",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:4:block:002",
        "page:5:block:001",
        "page:4:block:003"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-T4-02:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T4-02:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T4-02:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-T4-02:c4"
        },
        {
          "row_index": 4,
          "witness_key": "CQ-T4-02:c5"
        },
        {
          "row_index": 5,
          "witness_key": "CQ-T4-02:c6"
        },
        {
          "row_index": 6,
          "witness_key": "CQ-T4-02:c7"
        },
        {
          "row_index": 7,
          "witness_key": "CQ-T4-02:c8"
        }
      ]
    },
    {
      "question_id": "CQ-T4-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The first claim carries the assumption and its status as a stated caveat; the fifth names the claim it qualifies and its subject, the melts of the studied segment.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "qualified_claim",
          "row_index": 4,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "stated_assumption",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "caveat_disposition",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "claim_subject",
          "row_index": 4,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:5:block:004",
        "page:8:block:006",
        "page:5:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-T4-03:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T4-03:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T4-03:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-T4-03:c4"
        },
        {
          "row_index": 4,
          "witness_key": "CQ-T4-03:c5"
        }
      ]
    },
    {
      "question_id": "CQ-T4-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The first claim carries the existence statement and its subject, active venting on that segment's axis; the second that it is a denial; the third the spatial scope.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "existence_claim",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "negated_disposition",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "claim_subject",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "spatial_scope",
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
          "witness_key": "CQ-T4-04:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T4-04:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T4-04:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-T4-04:c4"
        },
        {
          "row_index": 4,
          "witness_key": "CQ-T4-04:c5"
        }
      ]
    },
    {
      "question_id": "CQ-T4-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The second claim carries the hedged long-period reading, its status as an implication and the modality; the fourth carries what the authors say is still needed.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "hedged_claim",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "hypothesised_disposition",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "epistemic_modality",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "stated_limitation",
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
          "witness_key": "CQ-T4-05:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T4-05:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T4-05:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-T4-05:c4"
        },
        {
          "row_index": 4,
          "witness_key": "CQ-T4-05:c5"
        }
      ]
    },
    {
      "question_id": "CQ-T5-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The sixth claim carries the degassing mechanism and the relation by which it is offered as producing the observed depth band, so it names both the mechanism and the evidential tie. The first carries the geochemical observation and the third the seismological one. The claim that states the solubility link explicitly is only partially supported and names nothing here.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "causal_mechanism",
          "row_index": 5,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "supporting_observation",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "geochemical_evidence",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "seismic_evidence",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "evidence_relation",
          "row_index": 5,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:5:block:005",
        "page:2:block:004",
        "page:2:block:005",
        "page:2:block:006",
        "page:5:block:006",
        "page:5:block:009"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-T5-01:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T5-01:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T5-01:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-T5-01:c4"
        },
        {
          "row_index": 4,
          "witness_key": "CQ-T5-01:c5"
        },
        {
          "row_index": 5,
          "witness_key": "CQ-T5-01:c6"
        }
      ]
    },
    {
      "question_id": "CQ-T5-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The third claim carries the comparison, the first the deep-earthquake segment with its range and unit, the second the adjacent segment to the south.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "comparison_relation",
          "row_index": 2,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "first_quantity_subject",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "second_quantity_subject",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "bounded_quantity",
          "row_index": 0,
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
        "page:8:block:007",
        "page:5:block:004"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-T5-02:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T5-02:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T5-02:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-T5-02:c4"
        },
        {
          "row_index": 4,
          "witness_key": "CQ-T5-02:c5"
        },
        {
          "row_index": 5,
          "witness_key": "CQ-T5-02:c6"
        }
      ]
    },
    {
      "question_id": "CQ-T5-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The sixth claim names the set of subsections inside the expected range, the first the expected depth at this spreading rate, the fourth the maximum depth of the subsection that exceeds it and the comparison itself.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "subsection_set",
          "row_index": 5,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "maximum_depth_claim",
          "row_index": 3,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "expected_depth_claim",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "comparison_relation",
          "row_index": 3,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:2:block:005",
        "page:2:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-T5-03:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T5-03:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T5-03:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-T5-03:c4"
        },
        {
          "row_index": 4,
          "witness_key": "CQ-T5-03:c5"
        },
        {
          "row_index": 5,
          "witness_key": "CQ-T5-03:c6"
        },
        {
          "row_index": 6,
          "witness_key": "CQ-T5-03:c7"
        }
      ]
    },
    {
      "question_id": "CQ-T5-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The first claim carries the categories, their count and the located earthquakes they sort; the second names which categories carry the interpretation.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "category_set",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "category_count",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "selection_for_interpretation",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "earthquake_catalog",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:2:block:003",
        "page:7:block:008"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-T5-04:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T5-04:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T5-04:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-T5-04:c4"
        },
        {
          "row_index": 4,
          "witness_key": "CQ-T5-04:c5"
        }
      ]
    },
    {
      "question_id": "CQ-T5-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The first claim names the cold and thick lithosphere explanation and that it is being declined; the second the axial morphology; the fifth the off-axis shallow seismicity; the fourth the contrast that makes the morphology evidence against that explanation.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "candidate_explanation",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "morphological_observation",
          "row_index": 1,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "seismic_observation",
          "row_index": 4,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "evidence_relation",
          "row_index": 3,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "declined_disposition",
          "row_index": 0,
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
          "witness_key": "CQ-T5-05:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-T5-05:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-T5-05:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-T5-05:c4"
        },
        {
          "row_index": 4,
          "witness_key": "CQ-T5-05:c5"
        },
        {
          "row_index": 5,
          "witness_key": "CQ-T5-05:c6"
        },
        {
          "row_index": 6,
          "witness_key": "CQ-T5-05:c7"
        },
        {
          "row_index": 7,
          "witness_key": "CQ-T5-05:c8"
        }
      ]
    },
    {
      "question_id": "CQ-C-01",
      "question_responsiveness": "NONE",
      "responsiveness_rationale": "The answer declares no answer in source and carries no claim. Searching the reading for sulfur and chlorine returns nothing, so every element is absent because the reading does not state it. Under the subject tie, the sample sets the reading does name belong to the carbon dioxide estimation and do not name this question's sample set.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "No sulfur or chlorine concentration appears anywhere in the reading; its volatile treatment is confined to carbon dioxide and water."
        },
        {
          "semantic": "concentration_unit",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "With no such concentration in the reading there is no unit for one either."
        },
        {
          "semantic": "sample_set",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading names sample sets for the carbon dioxide estimation, but none for a sulfur and chlorine measurement, which is this question's subject, so no sample set for it is stated."
        },
        {
          "semantic": "measurement_status",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading states nothing about whether such concentrations were measured or estimated, because it reports none."
        }
      ],
      "source_locators": [
        "page:5:block:004",
        "page:8:block:005",
        "page:8:block:007"
      ],
      "rows": []
    },
    {
      "question_id": "CQ-C-02",
      "question_responsiveness": "NONE",
      "responsiveness_rationale": "The answer declares no answer in source and carries no claim. The reading reports magnitude statistics and calls the record a short snapshot but states no recurrence interval, so every element is absent from the source.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "temporal_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading gives no repeat time or return period for the deep mantle earthquakes."
        },
        {
          "semantic": "time_unit",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "With no recurrence quantity stated there is no unit for one."
        },
        {
          "semantic": "event_population",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading describes the deep earthquakes and the record as a brief snapshot, but it defines no population over which a recurrence would be counted."
        },
        {
          "semantic": "measurement_status",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading says nothing about how such an interval would have been obtained, because it reports none."
        }
      ],
      "source_locators": [
        "page:2:block:004",
        "page:8:block:002"
      ],
      "rows": []
    },
    {
      "question_id": "CQ-C-03",
      "question_responsiveness": "NONE",
      "responsiveness_rationale": "The answer declares no answer in source and carries no claim. The reading describes the compilation and its figure but gives no per-site depth or rate, so every element is absent from the source.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "site_set",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading says a compilation of other slow- and ultraslow-spreading sites was assembled and names a handful whose entries were updated, but it does not state the compiled set the question asks about."
        },
        {
          "semantic": "maximum_depth_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "No per-site maximum depth is stated in the reading; those values sit in the comparison figure and its supplementary table, which the text layer does not carry."
        },
        {
          "semantic": "spreading_rate_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "No per-site full spreading rate is stated in the reading, for the same reason."
        }
      ],
      "source_locators": [
        "page:8:block:004",
        "page:5:block:010"
      ],
      "rows": []
    },
    {
      "question_id": "CQ-C-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The first claim gives the count, names the instruments and states that they were placed on the sea floor for this experiment, covering all three elements.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "instrument_count",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "observing_system",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "deployment_event",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:6:block:002",
        "page:2:block:002",
        "page:2:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "CQ-C-04:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-C-04:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-C-04:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-C-04:c4"
        }
      ]
    },
    {
      "question_id": "CQ-C-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The first claim gives the range and its subject, the primary melts of the studied segment; the second the unit; the third that it was arrived at by calculation.",
      "assembly": "NOT_APPLICABLE",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 0,
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
          "semantic": "quantity_subject",
          "row_index": 0,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "calculated_or_measured_status",
          "row_index": 2,
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
          "witness_key": "CQ-C-05:c1"
        },
        {
          "row_index": 1,
          "witness_key": "CQ-C-05:c2"
        },
        {
          "row_index": 2,
          "witness_key": "CQ-C-05:c3"
        },
        {
          "row_index": 3,
          "witness_key": "CQ-C-05:c4"
        },
        {
          "row_index": 4,
          "witness_key": "CQ-C-05:c5"
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

Each `witnesses` entry has this shape:

```
{
  "witness_key": "CQ-T1-01:c1",
  "source_support": "SUPPORTED | PARTIAL | UNSUPPORTED | NOT_EVALUABLE",
  "source_locators": ["page:2:block:004"],
  "rationale": "one or two sentences in your own words"
}
```

Each `rows` entry names one claim of that question and the witness it is:

```
{
  "row_index": 0,
  "witness_key": "CQ-T1-01:c1"
}
```

Each `coverage` entry names one required semantic and either the claim that
carries it or one typed reason it is absent:

```
{
  "semantic": "instrument_count",
  "row_index": 3,
  "absent_reason": null,
  "note": ""
}

{
  "semantic": "instrument_count",
  "row_index": null,
  "absent_reason": "NOT_CAPTURED | NOT_IN_SOURCE | WITHHELD_STATEMENT | NOT_MODELLED",
  "note": "why, in your own words"
}
```
