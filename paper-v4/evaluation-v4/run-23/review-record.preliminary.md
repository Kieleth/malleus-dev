# Malleus paper v4 source-grounded review record, protocol v3

This is run-23's blank record, written by
`paper-v4/evaluation-v4/run-23/build_review_inputs.py` from the frozen v3
template. The question ids are this cell's frozen competency question file's,
in that file's order. The row and witness counts are figures of a producer
that has not run and are filled by the same script at freeze; no other
placeholder survives either stage.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

The `questions` block below carries one entry per question of the cell's
competency question file, 30 of them, in that file's order. Write one
`witnesses` entry per distinct witness the query result returns,
428 in all, and reference it from every row that shares it.
Rows: 130 rows for `CQ-T1-01`, 130 for `CQ-T1-02`, 190 for `CQ-T1-03`, 190 for
`CQ-T1-04`, 130 for `CQ-T1-05`, 142 for `CQ-T2-01`, 342 for `CQ-T2-02`, 270
for `CQ-T2-03`, 355 for `CQ-T2-04`, 30 for `CQ-T2-05`, 271 for `CQ-T3-01`,
278 for `CQ-T3-02`, 278 for `CQ-T3-03`, 258 for `CQ-T3-04`, 254 for
`CQ-T3-05`, 143 for `CQ-T4-01`, 143 for `CQ-T4-02`, 126 for `CQ-T4-03`, 270
for `CQ-T4-04`, 106 for `CQ-T4-05`, 233 for `CQ-T5-01`, 278 for `CQ-T5-02`,
271 for `CQ-T5-03`, 246 for `CQ-T5-04`, 271 for `CQ-T5-05`, 241 for
`CQ-C-01`, 234 for `CQ-C-02`, 355 for `CQ-C-03`, 130 for `CQ-C-04`, 278 for
`CQ-C-05`,
6573 in all.

Three things the validator derives or forbids, so that writing them wrong is
refused rather than recorded:

- `question_responsiveness` is derived from `coverage`. Write the label the
  derivation produces, `COVERED` when every required semantic names a row,
  `NONE` when none does, `PARTIAL` otherwise. A label the derivation does not
  produce is refused.
- A witness whose `resolution` is `LOCATOR_NOT_RESOLVABLE` carries
  `source_support` `NOT_EVALUABLE`, never `PARTIAL` and never `UNSUPPORTED`,
  and says in its `rationale` what did not resolve.
- `assembly` is a descriptor, not a grade. It never moves a label.

On a `STRUCTURED_ROWS` cell every witness carries `resolution` and cites
locators of the form `<source_id>#row:N:field`. On a
`SELECTED_READING_TEXT_LAYER` cell no witness carries `resolution` and every
locator is a reading block id. Copy no source passage or source row into this
record beyond the locator, and add no numerical aggregate.

```json
{
  "schema": "malleus.paper-v4.source-grounded-review/v3",
  "status": "PRELIMINARY_COMPLETE",
  "inputs": {
    "review_protocol_sha256": "sha256:17b5744a71a1e6a9ab1985f43b3e28d4d683f2d7d369e7decdb375171c2edc21",
    "review_input_manifest_sha256": "sha256:8f6dbe37a2da977213d1007eb3a64ea24cb2566745966abe6453a64662d52873"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-preliminary-run-23",
    "completed_at": "2026-09-09T22:42:31Z"
  },
  "witnesses": [
    {
      "witness_key": "sample:melt-inclusions",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names rare undegassed MORBs and olivine melt inclusions as the material that defined the global volatile to non-volatile trace element trends, which is what the name, the sample material and the description say.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "sample:morb-obs-network",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block says all published geochemical analyses of MORB samples inside the OBS network coverage were compiled, matching the name, the material and the description.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "sample:morb-rc2",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The figure-caption block distinguishes the MORB samples along RC2 from those along RC3 and says estimated primary-melt CO2 contents are shown for them, which carries the name, the material and the description.",
      "source_locators": [
        "page:6:block:005"
      ]
    },
    {
      "witness_key": "sample:morb-rc3",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Same caption block names the RC3 MORB samples alongside the RC2 ones and attaches estimated CO2 contents to them.",
      "source_locators": [
        "page:6:block:005"
      ]
    },
    {
      "witness_key": "sample:popping-rocks",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The caption lists popping rocks as one of the plotted sample groups next to MORB whole rocks and melt inclusions, which is all the record claims.",
      "source_locators": [
        "page:6:block:005"
      ]
    },
    {
      "witness_key": "claim:ab-good-quality",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states that categories A and B are of good quality and used for interpretation, and the STATED modality fits the plain declarative wording.",
      "source_locators": [
        "page:2:block:003"
      ]
    },
    {
      "witness_key": "claim:acknowledgement-crew",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The acknowledgements block thanks the officers, crew and scientific party for their work during the 2019 SMARTIES cruise, exactly as the name puts it.",
      "source_locators": [
        "page:10:block:043"
      ]
    },
    {
      "witness_key": "claim:acknowledgement-discussions",
      "source_support": "PARTIAL",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block breaks off at the first name of the thanked colleagues, so it supports that named people are thanked but not the purpose the record's name adds, useful discussions, whose words fall in the following block.",
      "source_locators": [
        "page:10:block:043"
      ]
    },
    {
      "witness_key": "claim:all-authors-discussed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The author-contributions block closes by saying every author took part in discussing the results and commenting on the manuscript.",
      "source_locators": [
        "page:10:block:046"
      ]
    },
    {
      "witness_key": "claim:axial-valley-floor-basaltic",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block describes the valley floor as raised bathymetry cut by axis-parallel normal faults with basaltic constructions confirmed by seafloor rocks, which is the whole of the record's name.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "claim:both-perturbations-deep",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block reports that raising and lowering the velocity by the same amount both still locate many events deeper than 10 km beneath the axis, and MEASURED fits a result read off the relocation tests.",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "claim:brittle-10km-at-ntds",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says the results suggest a brittle lithosphere at most about 10 km thick at the segment boundaries, and the hedge in suggest matches the HYPOTHESISED modality.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "claim:category-definitions",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block sets out which criteria categories A, B-C and D meet, which is what the name reports.",
      "source_locators": [
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "claim:co2-behaves-incompatible",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states that at depth, during partial melting and fractional crystallisation, CO2 behaves like highly incompatible trace elements.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "claim:co2-solubility-pressure",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block ties CO2 solubility to pressure and water content and says the CO2 stays dissolved at depth but saturates and nucleates a gas phase near the seafloor, both halves of the record's name.",
      "source_locators": [
        "page:5:block:003"
      ]
    },
    {
      "witness_key": "claim:compilation-covariates",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The methods block lists the influences included with the compilation: core complexes and detachment faults, hydrothermal vents, magmatism and adjacent transform faults.",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "claim:correlations-used-globally",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says these correlations have been used to calculate primary melt CO2 content of global ridge segments.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "claim:correspondence",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The back-matter block names Zhiteng Yu and Satish C. Singh as the correspondence addressees.",
      "source_locators": [
        "page:11:block:002"
      ]
    },
    {
      "witness_key": "claim:crust-from-mantle-melt",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block opens with oceanic crust being formed by mantle-derived melt at spreading centers, the whole of the claim.",
      "source_locators": [
        "page:1:block:002"
      ]
    },
    {
      "witness_key": "claim:deeper-eq-observed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block reports deeper earthquakes at slow- and ultraslow-spreading ridges and attributes them to deep-rooted detachment faults or cold thermal regimes, which is what the name carries.",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "claim:deepest-documented",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block ranks these events as the deepest so far documented at any slow-spreading centre, which is the record's whole claim.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "claim:degassing-volume-change",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives the volume change, the extensional stresses, the local high strain rates and the triggering of deep mantle earthquakes in one sentence.",
      "source_locators": [
        "page:5:block:003"
      ]
    },
    {
      "witness_key": "claim:eq-in-mantle-below-10km",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says the earthquakes mostly occur in the mantle below 10 km with scattered crustal events, far exceeding the suggested maximum depth, and the word suggesting matches HYPOTHESISED.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "claim:fig3-panel-content",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block is the figure caption itself and lists the RC2 and NTD2 panels with hummocky seafloor, volcanic cones, corrugated surfaces and lithospheric ages, and the record labels itself a figure description.",
      "source_locators": [
        "page:4:block:007"
      ]
    },
    {
      "witness_key": "claim:fixed-depth-rms-worse",
      "source_support": "PARTIAL",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block starts mid-sentence on the word higher, so it supports the slower decrease and the higher final RMS against the unfixed run, but the subject of the first comparison, that the initial RMS residuals were much higher, is left in the preceding block.",
      "source_locators": [
        "page:8:block:001"
      ]
    },
    {
      "witness_key": "claim:focus-on-segments",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block names RC1, NTD1, RC2 and NTD2 as the subsections the study focuses on.",
      "source_locators": [
        "page:2:block:003"
      ]
    },
    {
      "witness_key": "claim:h3-mylonite",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW One block carries both the hypothesis of localized high strain in high-temperature mylonite shear zones and the sentence refusing it, so the name, the candidate-explanation kind and the NOT_SUPPORTED disposition all rest on cited text.",
      "source_locators": [
        "page:3:block:003"
      ]
    },
    {
      "witness_key": "claim:h4-magmatic-tectonic",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The first block states the magmatic-tectonic possibility and the second says the melt-movement mechanism does not apply, which is where the NOT_SUPPORTED disposition comes from; both blocks are cited.",
      "source_locators": [
        "page:4:block:002",
        "page:5:block:001"
      ]
    },
    {
      "witness_key": "claim:long-period-events",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block reports deep earthquakes without high-frequency energy and the inference that they may be long-period events, and may matches HYPOTHESISED.",
      "source_locators": [
        "page:5:block:008"
      ]
    },
    {
      "witness_key": "claim:magmatic-tectonic-contexts-differ",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block contrasts the cited eruption-associated cases, thickened Icelandic crust and cold Mayotte lithosphere, with a mid-ocean ridge setting.",
      "source_locators": [
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "claim:manual-check",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says both P- and S-wave arrivals were checked manually.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "claim:max-depth-compilation",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The methods block states the world-wide compilation of maximum earthquake depth with the full spreading rate at each site.",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "claim:max-depth-other-factors",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block names tectonic, hydrothermal and petrological processes as further controls on maximum earthquake depth.",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "claim:max-depth-selection",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The same block states the selection rule, depths constrained by several earthquakes rather than one, and the reason given for it, so the stated-method-choice kind holds.",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "claim:max-depths-affected",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The figure caption block lists detachment faults, hydrothermal vents, volcanoes or hotspots and transform faults as processes affecting the maximum depths.",
      "source_locators": [
        "page:5:block:010"
      ]
    },
    {
      "witness_key": "claim:mechanism-similar-volcanoes",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block draws the analogy with rapid CO2 degassing beneath active volcanoes and adds that it may produce deep long-period volcanic earthquakes.",
      "source_locators": [
        "page:5:block:008"
      ]
    },
    {
      "witness_key": "claim:melt-focused-narrow-zone",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block contrasts melting over a wide zone at depth with focusing into a narrow zone under the axis during ascent, which is what the record's name asserts.",
      "source_locators": [
        "page:1:block:002"
      ]
    },
    {
      "witness_key": "claim:melt-migration-not-understood",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block is the sentence denying any clear understanding of how the melts migrate, which is both the knowledge-gap kind and the NEGATED modality.",
      "source_locators": [
        "page:1:block:003"
      ]
    },
    {
      "witness_key": "claim:melt-movement-not-applicable",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block carries the sentence rejecting the melt-movement mechanism for these earthquakes, and NEGATED matches it.",
      "source_locators": [
        "page:5:block:001"
      ]
    },
    {
      "witness_key": "claim:melt-movement-strain",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block ties movement of melt at depth to raised strain rates and to brittle failure lower in the crust, which is the whole of what the record's name asserts.",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "claim:melt-resides-fractionates",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block carries the whole chain the name repeats: microseismicity at 10 to 20 km depth, melt residing and fractionating there, moving upward to form crust, and possibly freezing at the base of the lithosphere, all under the hedge suggests.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "claim:more-events-needed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says not all events show low-frequency energy and that more earthquakes would be needed to study the sources, which is the stated limitation the record labels.",
      "source_locators": [
        "page:5:block:008"
      ]
    },
    {
      "witness_key": "claim:no-competing-interests",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block is the competing-interests declaration itself and its denial matches the NEGATED modality.",
      "source_locators": [
        "page:10:block:047"
      ]
    },
    {
      "witness_key": "claim:no-current-eruption",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block denies evidence of a current eruption in the axial valley and gives the grounds, and the retained gap explains why no feature record is bound as subject.",
      "source_locators": [
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "claim:ntd1-origin",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The same block introduces NTD1 two sentences earlier, so the pronoun the assertion carries has its antecedent inside the cited block and the record's naming of NTD1 rests on it.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "claim:occ-exhumed-mantle",
      "source_support": "PARTIAL",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block opens mid-sentence with the consequence, exhumed mantle and a tectonic origin for the subsection, while what does the indicating, the extensive observation of peridotites, sits in the preceding block, so the causal half of the name is uncited.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "claim:offaxis-magmatism",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block attributes the swarm-like off-axis shallow microseismicity west of the axis to off-axis crustal magmatism, hedged with probably, which the HYPOTHESISED modality reflects.",
      "source_locators": [
        "page:5:block:001"
      ]
    },
    {
      "witness_key": "claim:peer-review",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The back-matter block thanks the anonymous reviewers and says a peer review file is available.",
      "source_locators": [
        "page:11:block:003"
      ]
    },
    {
      "witness_key": "claim:preexisting-faults-favor-migration",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says faults and fractures already present above a deep reservoir can help melt migrate and generate earthquakes.",
      "source_locators": [
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "claim:primary-vs-preeruptive",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block draws exactly this distinction between primary melts in equilibrium with the mantle source and pre-eruptive melts that have fractionated.",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "claim:publisher-note",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block holds both the reprints line and the publisher's neutrality note the name reports.",
      "source_locators": [
        "page:11:block:004"
      ]
    },
    {
      "witness_key": "claim:ratios-good-proxy",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The methods block calls the CO2/Rb and CO2/Ba ratios of MORB melt inclusions a good proxy for CO2 concentration.",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "claim:reduced-velocity-preferred",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block carries all three parts: shallower events but fewer locations from the increased model, smaller depth uncertainty from the reduced one, and the preference for a normal or slightly decreased model.",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "claim:samples-degassed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block reports the calculated solubility values close to the measured CO2 contents and reads that as the samples being degassed.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "claim:seafloor-basalts-degassed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives the closeness of the existing RC2 and RC3 measurements to the solubility at sample depth and the reason, that seafloor basalts are mostly degassed.",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "claim:shear-zone-with-detachment",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states that a localized high-strain shear zone in the deep mantle can be expected during detachment fault development and produce deep microseismicity.",
      "source_locators": [
        "page:3:block:003"
      ]
    },
    {
      "witness_key": "claim:shiptime-funded",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The acknowledgements block names the TGIR French Oceanographic Fleet as the funder of the SMARTIES ship time; the retained gap concerns a contribution number the ontology has no slot for and does not touch this claim.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "claim:station-corrections-iterated",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block describes the iterative station corrections used to find the best solution and remove three-dimensional effects at minimum average RMS misfit.",
      "source_locators": [
        "page:7:block:005"
      ]
    },
    {
      "witness_key": "claim:swave-delays-removed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says the S-wave delays, attributed to low velocities in unconsolidated sediments, were removed from the original S-onsets before inversion.",
      "source_locators": [
        "page:7:block:005"
      ]
    },
    {
      "witness_key": "claim:tests-support-deep",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says the depth resolution tests further support that these events are indeed deep.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "claim:tf-deep-eq-mylonite",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block attributes deep earthquakes on oceanic transform faults to semi-brittle deformation in hot hydrated shear zones, which is the record's claim.",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "claim:trace-element-assumption",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the assumption behind estimating CO2 from trace elements, that they reflect the mantle source and are unaffected by secondary processes, which is the stated limitation the record labels.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "claim:ultraslow-co2-high",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says CO2 content is likely high at ultraslow-spreading ridges where deep mantle earthquakes are observed, and likely matches HYPOTHESISED.",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "claim:updated-depth-data",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The methods block names the three sites whose reported data were updated with newly located data.",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "claim:velocity-model-matters",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block opens the velocity-model section with exactly this statement about precision of locations.",
      "source_locators": [
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "claim:volatile-controls-magma",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block makes volatile concentration the control on how a magma's physical properties evolve and gives it a key part in eruption dynamics.",
      "source_locators": [
        "page:5:block:002"
      ]
    },
    {
      "witness_key": "claim:volatile-role-unknown",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The abstract block states that the role of volatiles during melt migration remains unknown, which is the knowledge gap the record labels.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "claim:volatiles-extend-melting-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says abundant volatiles would push the onset of incipient melting deeper under spreading centers, hedged in the way the modality records.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "claim:vpvs-reasonable",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block reports the lowest RMS residuals and the largest number of located earthquakes for the ratio near 1.7 and calls that setting reasonable.",
      "source_locators": [
        "page:7:block:003"
      ]
    },
    {
      "witness_key": "cnt:catalog-links",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states a minimum of six catalog links per event pair to form a continuous cluster, which is the count and the scope the record carries.",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "cnt:final-located",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states that 514 earthquakes were finally located, matching the count and the scope.",
      "source_locators": [
        "page:6:block:005"
      ]
    },
    {
      "witness_key": "cnt:identified-earthquakes",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states 760 earthquakes were identified and registered into the SEISAN database, which is the count and the scope verbatim in substance.",
      "source_locators": [
        "page:6:block:002"
      ]
    },
    {
      "witness_key": "cnt:location-categories",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says the locations were classified into four categories and names them A, B, C and D.",
      "source_locators": [
        "page:2:block:003"
      ]
    },
    {
      "witness_key": "cnt:magnitude-groups",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block divides the earthquakes into three groups, along the transform, at the ridge-transform intersection and along the MAR, and ties them to the b value determination.",
      "source_locators": [
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "cnt:new-focal-mechanisms",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives the number of newly obtained well-constrained focal mechanism solutions; the retained gap concerns other thresholds in the same sentence and not this count.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "cnt:ntds",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says the studied portion is offset by two non-transform discontinuities, which is the count and its scope.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "cnt:relocated-events",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives 364 well-constrained events relocated with hypoDD, matching count, scope and the MEASURED modality.",
      "source_locators": [
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "cnt:relocation-iterations",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW One sentence in the block gives both projected quantities, five iterations and a maximum event separation of 6 km, so the count and the attached length both rest on the cited block.",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "cnt:subsections",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says the portion subdivides into four subsections of 20 to 50 km, which carries the count and the length bounds and unit.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "cnt:total-focal-mechanisms",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says the three new solutions combined with three previous ones provided six focal mechanisms, which is the count and the scope.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "cnt:velest-iterations",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives six as the number of iterations after which the two models' residuals converge, which is the count and the scope the record carries.",
      "source_locators": [
        "page:6:block:004"
      ]
    },
    {
      "witness_key": "cnt:velest-subdataset",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives the 360-earthquake sub-dataset and both selection conditions, at least six arrivals and a station gap of at most 180 degrees, which is count and scope.",
      "source_locators": [
        "page:6:block:004"
      ]
    },
    {
      "witness_key": "cnt:velocity-models",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says five 1-D P-wave velocity models were constructed from an active-source wide-angle refraction profile, matching the count and the scope.",
      "source_locators": [
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "cnt:well-relocated",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states 276 events were well relocated and replaced the NonLinLoc locations in the final catalogue.",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "ratio:co2-ba",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives CO2/Ba as 81.3 plus or minus 23 and attributes the trend to undegassed MORBs and olivine melt inclusions, so numerator, denominator, value and uncertainty all rest on it.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "ratio:co2-rb",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The same sentence gives CO2/Rb as 991 plus or minus 129 for the same material.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "ratio:vp-vs",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says Wadati diagrams yield a Vp/Vs ratio of about 1.7, which is the numerator, denominator and value.",
      "source_locators": [
        "page:7:block:002"
      ]
    },
    {
      "witness_key": "gchem:abstract-co2-primary",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The abstract block gives about 0.4 to 3.0 wt% CO2 in the primary melts and attributes it to syntheses of rock samples and their geochemical analyses, which supports the melt stage, the bounds, the unit, the approximate qualification and a derived rather than directly measured determination.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "obs:average-depth-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives the average depth uncertainties as about 2.6 km and uses them as the yardstick for the depth shifts, which is the record's name, value and unit.",
      "source_locators": [
        "page:7:block:009"
      ]
    },
    {
      "witness_key": "obs:axial-event-depth-stability",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The same block says the depths of most axial events stay between 10 and 20 km across the five velocity models, which carries both bounds and the scope.",
      "source_locators": [
        "page:7:block:009"
      ]
    },
    {
      "witness_key": "obs:b-value",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives the b value of 0.87 and says it was calculated with ZMAP, matching the value and the CALCULATED modality.",
      "source_locators": [
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "obs:brittle-thickness",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block ties the predicted maximum depth to a brittle lithospheric thickness of less than 10 km, which is the bound, the unit and the open-upper qualification.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "obs:co2-gas-loss",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block puts the 80 to 90 percent loss on the gas phase nucleated by the time the melt reaches the seafloor, which is the record's bounds, unit and scope.",
      "source_locators": [
        "page:5:block:003"
      ]
    },
    {
      "witness_key": "obs:co2-saturation-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives about 25 km depth for saturation of a melt above 0.7 wt% CO2 and names the solubility model as the origin, which supports the value and the MODELLED determination.",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "obs:co2-saturation-pressure",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The same sentence gives about 0.7 GPa as the saturation pressure from the solubility model.",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "obs:co2-saturation-temperature",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The same sentence gives 1250 degrees Celsius as the saturation temperature from the solubility model.",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "obs:criterion-arrivals",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block lists more than eight arrivals as the second criterion for a well-constrained location, which is the bound and its open-lower qualification.",
      "source_locators": [
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "obs:criterion-azimuthal-gap",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives the azimuthal station gap criterion of less than 180 degrees.",
      "source_locators": [
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "obs:criterion-swave-distance",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives the third criterion, one S-wave arrival within 1.4 times the focal depth distance.",
      "source_locators": [
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "obs:crust-age-west-flank",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block calls the crust of the western ridge flank 8 Ma old in the same sentence that gives its thickness.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "obs:crust-thickness-west-flank",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives 5.4 plus or minus 0.3 km for that crust, matching value, uncertainty and unit.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "obs:degassing-eq-depth-range",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says continued degassing of the ascending melt would produce earthquakes in the mantle between 10 and 20 km, and would matches the hedged modality.",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "obs:depth-uncertainty-bound",
      "source_support": "PARTIAL",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The cited block opens mid-list with a bare of at most 10 km, so it carries the bound but not the words naming it a depth uncertainty, which fall at the end of the preceding block.",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "obs:dry-melting-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says extensive dry melting commences at 60 to 70 km depths, which is the record's bounds and unit.",
      "source_locators": [
        "page:1:block:002"
      ]
    },
    {
      "witness_key": "obs:error-ellipsoid-confidence",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says NonLinLoc estimates a three-dimensional error ellipsoid at 68 percent confidence.",
      "source_locators": [
        "page:7:block:005"
      ]
    },
    {
      "witness_key": "obs:expected-max-depth-slow",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives less than 8 km below the seafloor for slow-spreading ridges and names thermal models as the basis, supporting the bound, the depth reference and the modelled determination.",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "obs:expected-max-depth-ultraslow",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The same sentence gives less than 12 km below the seafloor for ultraslow-spreading ridges.",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "obs:fig3-shading-threshold",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The caption block puts the light brown and gray shadings either side of 10 km, which is the threshold the record carries; the retained gap notes only that the two open ranges cannot be expressed as one bound pair.",
      "source_locators": [
        "page:4:block:007"
      ]
    },
    {
      "witness_key": "obs:fig4-isotherm",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The caption block says the dashed black line marks the 750 degree Celsius isotherm.",
      "source_locators": [
        "page:5:block:010"
      ]
    },
    {
      "witness_key": "obs:focal-selection-criteria",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block states the whole selection criterion including more than eight P-wave polarities, which is the quantity the record projects; the retained gap says the other five thresholds are not carried as records.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "obs:fraction-two-criteria",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives the share of located earthquakes satisfying at least two of the criteria as a percentage, which is the value and unit the record carries.",
      "source_locators": [
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "obs:full-spreading-rate",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block opens with a full spreading rate of about 32 mm/yr as the basis for the expected maximum depth, matching value, unit and role.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "obs:group-b-values",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives 0.89 to 0.93 as the b values of the three groups.",
      "source_locators": [
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "obs:high-frequency-threshold",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block puts the missing energy above 5 Hz, which is the threshold and its open-lower qualification.",
      "source_locators": [
        "page:5:block:008"
      ]
    },
    {
      "witness_key": "obs:horizontal-uncertainty-bound",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block names horizontal uncertainties of at most 10 km in its own words; the retained gap only records that an inclusive bound cannot be distinguished from a strict one.",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "obs:instrument-spacing",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives an instrument spacing of about 30 km for the network.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "obs:lithosphere-age-45ma",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block attributes the cold-edge effect at the ridge-transform intersection to the cold 45 Ma lithosphere.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "obs:lithospheric-age-contours",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The caption block says the thin gray lines give lithospheric ages every 10 Ma, which is the interval the record carries.",
      "source_locators": [
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "obs:magnitude-completeness",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives the magnitude completeness of 1.5 calculated with ZMAP.",
      "source_locators": [
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "obs:mean-horizontal-error",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives the mean horizontal error as about 2.8 km; the population it belongs to is carried by a pronoun whose antecedent is the located earthquakes of the preceding block, which does not change the quantity or its value.",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "obs:mean-horizontal-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The figure caption block gives the average horizontal uncertainty after relocation as about 2.1 km, which is the record's quantity, value and unit.",
      "source_locators": [
        "page:3:block:004"
      ]
    },
    {
      "witness_key": "obs:mean-vertical-error",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives the mean vertical error as about 2.9 km; the population is carried by a pronoun pointing back to the located earthquakes of the preceding block, which leaves the quantity and value intact.",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "obs:melting-initiation-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says a small amount of melting initiates at about 150 to 300 km depths in the presence of volatiles.",
      "source_locators": [
        "page:1:block:002"
      ]
    },
    {
      "witness_key": "obs:model1-vp",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says Model 1 shows P-wave velocity exceeding 7.2 km/s at about 3 km depth, which is the record's bound, unit and open-lower qualification.",
      "source_locators": [
        "page:7:block:009"
      ]
    },
    {
      "witness_key": "obs:offaxis-cluster-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives shallow focal depths of about 2 to 6 km for the cluster on the western side of the axial valley.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "obs:offaxis-swarm-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block puts the swarm-like off-axis shallow microseismicity west of the axis at less than 10 km.",
      "source_locators": [
        "page:5:block:001"
      ]
    },
    {
      "witness_key": "obs:predicted-max-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says microseismicity studies indicate a maximum earthquake depth of less than 10 km for that spreading rate.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "obs:profile-halfwidth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The caption block says the depths are plotted within plus or minus 10 km of the profile, which is the half-width the record carries.",
      "source_locators": [
        "page:3:block:005"
      ]
    },
    {
      "witness_key": "obs:profile-tick-interval",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The caption block says the marks on top give 20 km intervals.",
      "source_locators": [
        "page:3:block:005"
      ]
    },
    {
      "witness_key": "obs:quality-abc-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The legend block gives an uncertainty of at most 5 km for qualities A, B and C, which is the bound and its unit.",
      "source_locators": [
        "page:3:block:004"
      ]
    },
    {
      "witness_key": "obs:quality-d-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The same legend gives category D as more than 5 km and at most 10 km, so both numbers rest on the block; the retained gap records that the open lower end cannot be expressed by a bound pair.",
      "source_locators": [
        "page:3:block:004"
      ]
    },
    {
      "witness_key": "obs:relocation-gap",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives azimuthal gaps of less than 270 degrees for the relocated events.",
      "source_locators": [
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "obs:relocation-obs-threshold",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The same sentence says all 364 relocated earthquakes were detected on more than six OBSs.",
      "source_locators": [
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "obs:relocation-rms",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The same sentence gives RMS residuals under 0.25 s for those events.",
      "source_locators": [
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "obs:relocation-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The same sentence gives uncertainties under 5 km for those events.",
      "source_locators": [
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "obs:rms-residual-bound",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block names RMS residuals of at most 0.3 s in its own words.",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "obs:solubility-calc-temperature",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block lists a temperature of 1200 degrees Celsius among the parameters of the theoretical solubility calculation.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "obs:station-gap-bound",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block names station gaps of less than 270 degrees.",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "obs:studied-portion-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says the studied portion of the ridge is about 120 km long.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "obs:triggering-pore-pressure",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says an increase in pore pressure of only 2 to 3 bars can trigger earthquakes.",
      "source_locators": [
        "page:5:block:003"
      ]
    },
    {
      "witness_key": "obs:updated-horizontal-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block gives the updated average horizontal uncertainty of about 2.1 km after the relocation.",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "obs:velocity-constraint-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says the refraction profile constrains velocities down to about 60 km below sea level, which carries the bound and the depth reference.",
      "source_locators": [
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "obs:velocity-perturbation",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says the velocity was increased and decreased by 0.1 km/s at all depths, which is the signed pair the record carries.",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "obs:vpvs-test-range",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block says ratios ranging from 1.5 to 2.5 were used to locate earthquakes.",
      "source_locators": [
        "page:7:block:002"
      ]
    },
    {
      "witness_key": "obs:young-crust-age",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW The block puts a magmatically accreted young crust at under 7.5 Ma in the same parenthesis.",
      "source_locators": [
        "page:7:block:009"
      ]
    },
    {
      "witness_key": "claim:axis-relocating",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the OCC termination and the OCC faulted dome, so the subject occurs in it, and it states the suggested relocation of the ridge axis under the hedge the HYPOTHESISED modality records.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "claim:bdb-shallower-southward",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block opens by naming the BDB and gives the southward shallowing and the cold-edge reason the name reports.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "claim:co2-degassing-deep-eq",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The abstract block carries the mechanism claim and the discussion block names the segment RC2 and calls this possibility the preferred one, so the subject and the PREFERRED disposition both occur in cited blocks.",
      "source_locators": [
        "page:1:block:001",
        "page:5:block:002"
      ]
    },
    {
      "witness_key": "claim:co2-influences-lab-melt",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The abstract block names the lithosphere-asthenosphere boundary and states the projected influence of a large CO2 concentration on melt beneath it.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "claim:deep-eq-aligned",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The first block names the segment RC2 axis and gives the N150E alignment parallel to the axial normal faults, and the sentence denying a cluster runs into the second cited block, which completes it with the word swarm.",
      "source_locators": [
        "page:4:block:003",
        "page:5:block:001"
      ]
    },
    {
      "witness_key": "claim:deep-events-not-artifacts",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names RC2 in the parenthesis and reports that the tests leave the deep events well constrained, demanded by the data and not artefacts.",
      "source_locators": [
        "page:8:block:001"
      ]
    },
    {
      "witness_key": "claim:depths-not-artifact",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the MAR axis and denies that the unexpected depths are an artifact of location errors.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "claim:detachment-inactive",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block speaks of this detachment fault and infers from the absence of deep microseismicity near the OCC termination that it is inactive.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "claim:enriched-basalts-low-melting",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the Romanche transform and reports the interpretation of the enriched basalts and high volatile contents as low degrees of partial melting of an enriched source near it.",
      "source_locators": [
        "page:5:block:005"
      ]
    },
    {
      "witness_key": "claim:extinct-vent-too-far",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names NTD1, places the extinct vent field on its eastern flank, and says its distance from the present-day axial valley means it would not affect the lithosphere beneath the RC2 axis.",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "claim:fig3-panels",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The caption block names the OCC and lists the marked tectonic information and the two depth transects within 5 km of the profile, which is what the figure-description claim carries.",
      "source_locators": [
        "page:4:block:006"
      ]
    },
    {
      "witness_key": "claim:fig6-panels",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The caption block names the BDB and gives the three segments, the brittle and ductile patches and the line constrained by the maximum earthquake depth.",
      "source_locators": [
        "page:7:block:011"
      ]
    },
    {
      "witness_key": "claim:five-models-enumerated",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the Romanche transform and enumerates the same five models the record lists.",
      "source_locators": [
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "claim:focal-not-robust",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the OBSs, says the mechanism solutions are not very robust because of their large spacing, and adds the azimuthal ray path limitation, which is the stated limitation the record labels.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "claim:h1-cold-lithosphere",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK One block carries the cold and thick lithosphere explanation, names the segment RC2 in the sentence that refuses it on magmatic morphology, so name, subject and NOT_SUPPORTED disposition all rest on it.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "claim:h2-hydrothermal-cooling",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the BDB, states the hydrothermal cooling hypothesis, and in the same block records that no active vents are observed on the RC2 axis and the extinct field is too far to matter, which is where the NOT_SUPPORTED disposition comes from.",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "claim:higher-temp-hinders-nucleation",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the RC2 ridge axis, reports no earthquakes below 20 km there and offers temperatures above 1200 degrees as the possible reason, matching the hedged modality.",
      "source_locators": [
        "page:5:block:007"
      ]
    },
    {
      "witness_key": "claim:keller-volatiles-flush",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the lithosphere-asthenosphere boundary and reports the cited suggestion about focalizing and flushing melt.",
      "source_locators": [
        "page:5:block:010"
      ]
    },
    {
      "witness_key": "claim:lab-melt-co2-h2o",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the LAB and says a large amount of CO2 suggests the melt there could be due to a combination of CO2 and water.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "claim:magmatism-dominates-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC2 and states both halves, magmatism dominating crustal accretion and earthquakes in a hot mantle above 1100 degrees.",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "claim:mantle-hot",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the RC2 segment axis and concludes from thermal modelling that the mantle beneath it is hot as expected for a magmatic segment, which fits the CALCULATED modality.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "claim:max-depth-not-following-relationship",
      "source_support": "PARTIAL",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the MAR and carries the denial, but the sentence breaks after the word spreading, so the second term of the relationship and the qualifier observed elsewhere are only in the following block.",
      "source_locators": [
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "claim:melt-lens-defines-bdb",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the brittle-ductile boundary and says axial melt lenses define it at fast- and intermediate-spreading ridges.",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "claim:model1-inappropriate",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the Romanche transform, carries the concession about mantle peridotites and a crust-free lithosphere, and the refusal of that model for events beneath the MAR axis.",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "claim:model5-selected",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names Model 5, calls the average velocity model the best-fitting one and says it was selected for the subsequent location and focal mechanism work.",
      "source_locators": [
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "claim:no-active-vents-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC2 axis and denies observations of active hydrothermal vents there, which is the NEGATED modality.",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "claim:ntd2-bdb-normal",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names NTD2 and gives all three parts: microseismicity to 10 km, a BDB at about 10 km called normal, and the contrast with the deeper RC2 seismicity.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "claim:occ-recent-deformation",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names this OCC and calls the normal faults cutting its surface suggestive of recent active deformation, which matches the hedged modality.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "claim:occ-shallow-ruptures",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the OCC dome and puts the shallow earthquakes beneath it down to rupture on the steep normal faults that cut its surface.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "claim:one-obs-no-data",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The caption block names the deployed ocean-bottom seismometers and says the blue triangle marks the one that generated no data.",
      "source_locators": [
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "claim:rc2-magmatic-origin",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC2 and states its magmatic origin on the morphological evidence.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "claim:rc2-no-detachment",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC2 and carries the denial of any evidence for detachment faults in full.",
      "source_locators": [
        "page:4:block:001"
      ]
    },
    {
      "witness_key": "claim:rc2-rc3-analysed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The methods block names the segment RC2 and the adjacent RC3 to the south and says their samples were analysed.",
      "source_locators": [
        "page:8:block:005"
      ]
    },
    {
      "witness_key": "claim:rc2-robust",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC2 and calls it magmatically robust on the median valley and neo-volcanic ridge, hedged with suggesting.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "claim:refraction-profile-used",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the one-dimensional velocity model and says the refraction profile was used to find the best one for travel times during earthquake locations.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "claim:rti-amagmatic",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the RTI segment and RC2's neighbour RC1 in the same paragraph and states plainly that the RTI segment is amagmatic.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "claim:selected-model-more-events",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names Model 5 and carries the close RMS residuals after six iterations, the larger number of located earthquakes and the preference that follows.",
      "source_locators": [
        "page:6:block:004"
      ]
    },
    {
      "witness_key": "claim:small-pressure-increase-induces",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the RC2 ridge axis and states the suggestion that the small pressure increase from CO2 degassing induces the earthquakes observed there.",
      "source_locators": [
        "page:5:block:003"
      ]
    },
    {
      "witness_key": "claim:snapshot-limitation",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the MAR supersegment and states the snapshot caveat and the year-to-year variability, which is the stated limitation the record labels.",
      "source_locators": [
        "page:2:block:004"
      ]
    },
    {
      "witness_key": "claim:tomography-normal-vpvs",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the present segment RC2 and reports normal Vp/Vs ratios there from the tomographic results.",
      "source_locators": [
        "page:7:block:003"
      ]
    },
    {
      "witness_key": "claim:volatiles-reduce-solidus",
      "source_support": "PARTIAL",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the LAB and carries the consequence, melt at sub-solidus temperatures for anhydrous peridotites, but it opens mid-sentence on the words solidus temperature, so the agent of the claim, that volatiles would reduce it, is left in the preceding block.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "cnt:events-mar",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the MAR and gives 317 events located along it.",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "cnt:events-romanche",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence names the Romanche transform and gives 197 events located along it.",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "cnt:forced-depth-subset",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC2 and gives the subset of 45 events between 10 and 20 km along the cross-section whose depths were forced; the retained gap concerns the four forced depths, not this count.",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "cnt:located-earthquakes",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the Romanche RTI region and gives 514 earthquakes located in its vicinity.",
      "source_locators": [
        "page:2:block:003"
      ]
    },
    {
      "witness_key": "cnt:min-obs-per-event",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the OBSs and says each manually checked event had to be detected by at least five of them.",
      "source_locators": [
        "page:6:block:002"
      ]
    },
    {
      "witness_key": "cnt:obs-deployed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the network of 19 ocean-bottom seismometers that acquired the microseismicity data, which is the count and the scope.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "cnt:useful-obs",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block says initial arrivals were detected automatically from 17 useful OBSs.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "gchem:eq-atlantic-co2-avg",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the equatorial Atlantic Ocean between 5 South and 5 North, gives the average of about 2800 ppm and names the CO2/Rb and CO2/Ba estimations as the proxy.",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "gchem:eq-atlantic-co2-max",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives up to about 8799 ppm for the same region and the same proxy.",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "gchem:rc2-ba",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC2 and gives Ba above 89 ppm for all its samples, which is the analyte, the bound and the unit.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "gchem:rc2-co2-ba",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC2, defines CO2(Ba) as the estimate from Ba for pre-eruptive melts and gives 0.7 to 4.6 wt%.",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "gchem:rc2-co2-ba90",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC2, ties Ba90 to melts in equilibrium with Fo90 olivine and gives CO2(Ba90) of 0.4 to 3.0 wt% in the primary melts.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "gchem:rc2-co2-minimum",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the studied segment RC2 and says the primary-melt CO2 concentration is at least 0.4 wt%, which is the open lower bound the record carries.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "gchem:rc2-co2-preeruptive",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC2 and gives estimated pre-eruptive CO2 of 0.7 to 4.6 wt% after fractional crystallisation.",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "gchem:rc2-co2-primary-calc",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC2 and gives CO2(calculated) of 0.4 to 3.0 wt% for the melts generated along it.",
      "source_locators": [
        "page:5:block:005"
      ]
    },
    {
      "witness_key": "gchem:rc2-co2-rb",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC2, defines CO2(Rb) as the estimate from Rb for pre-eruptive melts and gives 0.9 to 4.3 wt%.",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "gchem:rc2-co2-rb90",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC2 and gives CO2(Rb90) of 0.5 to 2.8 wt% in the primary melts.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "gchem:rc2-rb",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC2 and gives Rb above 8 ppm for all its samples.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "gchem:rc3-co2-ba",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC3 and gives CO2(Ba) of 0.06 to 0.8 wt% for its pre-eruptive melts.",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "gchem:rc3-co2-ba90",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC3 and gives CO2(Ba90) of 0.04 to 0.5 wt% in its primary melts.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "gchem:rc3-co2-primary-calc",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC3 and gives CO2(calculated) of 0.04 to 0.7 wt% for it in the comparison with RC2.",
      "source_locators": [
        "page:5:block:005"
      ]
    },
    {
      "witness_key": "gchem:rc3-co2-rb",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC3 and gives CO2(Rb) of 0.07 to 1.0 wt% for its pre-eruptive melts.",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "gchem:rc3-co2-rb90",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC3 and gives CO2(Rb90) of 0.05 to 0.7 wt% in its primary melts.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "gchem:swir-co2-highest",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the SWIR and reports 1.9 wt% as the highest previously reported CO2 in the melt there.",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "obs:abstract-deep-eq-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The abstract block names the Mid-Atlantic Ridge axis and reports deep earthquakes at 10 to 20 km depth in the mantle.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "obs:bdb-isotherm",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the BDB and gives the 700 plus or minus 100 degree isotherms it is tied to at slow- and ultraslow-spreading ridges.",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "obs:coverage-mar",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the MAR axis and gives 120 km of it as covered by the network.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "obs:coverage-romanche",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence names the Romanche transform and gives 140 km of its eastern part as covered.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "obs:deep-eq-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC2 axis and gives the observed deep earthquakes at 16 to 19 km.",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "obs:deep-micro-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the ridge axis of the segment RC2 and puts the deep microseismicity there at about 10 to 20 km.",
      "source_locators": [
        "page:2:block:004"
      ]
    },
    {
      "witness_key": "obs:forced-depths",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC2 and lists the forced depths from 2.5 km to 10 km; the retained gap records that a bound pair cannot show they are four discrete settings.",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "obs:h1-bdb-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the BDB and puts it at about 20 km under the cold and thick lithosphere explanation, with the hedge the modality records.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "obs:h1-isotherms",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the 600 to 800 degree isotherms corresponding to that BDB depth.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "obs:iceland-magmatic-depths",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names Iceland, hyphenated across the line break, and gives depths greater than 10 km for the Askja and Fagradalsfjall cases.",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "obs:interpreted-deep-eq-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The caption block names the MAR axis, gives 10 to 19 km below the seafloor and attaches the CO2 degassing interpretation.",
      "source_locators": [
        "page:7:block:012"
      ]
    },
    {
      "witness_key": "obs:lab-melt-fraction",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the LAB and reports the proposed melt fraction of about 1.1 percent at its base.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "obs:lab-water-content",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives a water content of up to 332 ppm there.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "obs:mar-half-spreading-rate",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the MAR and gives its half-spreading rate here as 16 mm/yr.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "obs:mar-segment-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block places the study area in the MAR segment between the two named transforms and gives that segment's length in kilometres as the record carries it.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "obs:mayotte-depths",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names Mayotte Island and gives depths greater than 30 km offshore it.",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "obs:no-eq-below-20km",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the RC2 ridge axis and says no earthquakes are observed below 20 km beneath it.",
      "source_locators": [
        "page:5:block:007"
      ]
    },
    {
      "witness_key": "obs:normal-depth-ntd2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the southern NTD2 and gives normal-depth earthquakes of 4 to 10 km beneath it.",
      "source_locators": [
        "page:2:block:004"
      ]
    },
    {
      "witness_key": "obs:ntd1-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names NTD1 and gives its length as about 35 km.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "obs:ntd2-depth-10",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names NTD2 and says the earthquakes there reach down to about 10 km.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "obs:ntd2-depth-range",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names NTD2 with a bound of less than 10 km, and the depth range that sentence refers back to is set out earlier in the same block.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "obs:ntd2-offset",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names NTD2 and gives its ridge offset as about 33 km.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "obs:occ-depth-range",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence names the OCC with a bound of less than 6 km.",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "obs:offaxis-bdb-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the BDB and says it remains shallow, under 10 km, west of the segment RC2 axis.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "obs:offaxis-crustal-age",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence names the MAR and gives the crustal age of about 1.3 Ma up to which that holds.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "obs:rc2-crust-thickness",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The caption block names the segment RC2 and gives its crust as about 5.4 plus or minus 0.3 km thick.",
      "source_locators": [
        "page:7:block:011"
      ]
    },
    {
      "witness_key": "obs:rc2-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC2 and gives its length as about 22 km.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "obs:rc2-valley-width",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same sentence gives the median valley of RC2 as typically 10 km wide.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "obs:rc3-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the segment RC3 and calls it 50 km long.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "obs:shallow-eq-rti",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the RTI and gives 0 to 6 km for the majority of shallow earthquakes on its outside corner.",
      "source_locators": [
        "page:2:block:004"
      ]
    },
    {
      "witness_key": "obs:thermal-model-temp",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block names the RC2 segment axis and gives 1100 to 1200 degrees at 10 to 20 km depth from thermal modelling, which supports the bounds and the modelled determination.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "event:romanche-2016",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The figure caption block names the 2016 Mw 7.1 Romanche earthquake, which is the record's name and magnitude; the retained gap concerns the two unnamed subevents, not this record.",
      "source_locators": [
        "page:3:block:004"
      ]
    },
    {
      "witness_key": "geo:askja",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names Askja Volcano, which carries both the name and the volcano feature kind.",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "geo:bdb",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The abstract block writes the brittle-ductile boundary out in full and the introduction block gives the BDB abbreviation the record carries as a tag.",
      "source_locators": [
        "page:1:block:001",
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "geo:chain-tf",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the Romanche and Chain transform faults, which gives the name and the transform-fault kind.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "geo:detachment-east",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block calls the eastern boundary of the RTI segment a westward dipping detachment fault, which is the name and the feature kind.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "geo:equatorial-atlantic",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block places the study in the equatorial Atlantic Ocean, which is the record's whole content.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "geo:extinct-vent-field",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block reports an extinct hydrothermal vent field observed on the eastern flank of NTD1, which is the name and the feature kind.",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "geo:fagradalsfjall",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the Fagradalsfjall Peninsula, giving the name and the peninsula kind.",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "geo:gakkel",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the Gakkel Ridge among ultraslow-spreading ridges, which is the name and the kind.",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "geo:iceland",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names Iceland, hyphenated across the line break, which the record keeps as a tag alongside the plain name.",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "geo:inactive-mound",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The caption block reports an inactive hydrothermal mound suggested by the dive observations, which is the name and the kind.",
      "source_locators": [
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "geo:juan-de-fuca",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the young Juan de Fuca plate, giving the name and the plate kind.",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "geo:knipovich",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The methods block names Knipovich Ridge; its ultraslow-spreading kind is the sense the compilation sentence works in, which the same block sets out.",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "geo:lab",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The abstract block writes the lithosphere-asthenosphere boundary out in full, which is the record's name and its LAB tag.",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "geo:logachev",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the Logachev Seamount of Knipovich Ridge, which carries the name and the seamount kind.",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "geo:mar",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The title block names the Mid-Atlantic Ridge and the introduction block gives the MAR abbreviation the record keeps as a tag.",
      "source_locators": [
        "page:1:block:001",
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "geo:mayotte",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names Mayotte Island offshore in the western Indian Ocean, which is the name, the tag and the island kind.",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "geo:moho",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The figure block carries Moho as a label and the caption block calls it the expected Moho interface, which is the record's name and feature kind.",
      "source_locators": [
        "page:7:block:010",
        "page:7:block:011"
      ]
    },
    {
      "witness_key": "geo:neovolcanic-ridge",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the N154E-oriented neo-volcanic ridge in RC2, which is the name, the kind and the orientation.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "geo:ntd1",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The introduction block names the first NTD as NTD1 and calls the two offsets non-transform discontinuities, and the later block gives its N76E orientation.",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "geo:ntd1-faults",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block says NTD1 is characterized by a large number of N118E- and E-W-striking faults, which is the name, the kind and both orientations.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "geo:ntd2",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The introduction block names the second NTD as NTD2 under the non-transform discontinuity kind and the later block gives its N110E orientation.",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "geo:ntd2-faults",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block says large areas of NTD2 are affected by normal faults striking N115E and N145E, which is the name, the kind and both orientations.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "geo:occ",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the prominent oceanic core complex and its OCC abbreviation, which is the name, the tag and the kind.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "geo:occ-normal-faults",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block says the OCC surface is cut by roughly N20E- and N20W-striking normal faults, which is the name, the kind and both orientations.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "geo:rainbow",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the Rainbow massif; the retained gap records only that the discontinuity it sits at is unnamed, which this record does not claim.",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "geo:rc1",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the RTI segment RC1 in the enumeration of the four subsections, which is the name, the tag and the kind.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "geo:rc2",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The same enumeration names RC2 as a short ridge segment, which is the name and the ridge-segment kind.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "geo:rc2-bounding-faults",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block describes the faults bounding RC2 as high-angle, inward dipping and NNW-SSE oriented, which is the name, the kind and the orientation.",
      "source_locators": [
        "page:4:block:001"
      ]
    },
    {
      "witness_key": "geo:rc3",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The introduction block names the segment south of NTD2 as RC3 and the later block gives its about N165E orientation.",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "geo:romanche-tf",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The introduction block names the Romanche transform fault and the results block uses the Romanche TF abbreviation the record keeps as a tag.",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "geo:rti",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the eastern Romanche ridge-transform intersection and its RTI abbreviation, which is the name, the tag and the kind.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "geo:swir",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the Southwest Indian Ridge with its SWIR abbreviation and, in the following sentence, treats it as an amagmatic ultraslow-spreading setting.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "work:article",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The title block gives the DOI, the article kind and the title, the first-page footer gives the journal, year, volume and page, and the back-matter block gives the licence, so every projected field rests on a cited block.",
      "source_locators": [
        "page:1:block:001",
        "page:1:block:006",
        "page:11:block:005"
      ]
    },
    {
      "witness_key": "work:cruise-portal",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The data availability block names the website, its address and what it holds; the record only normalises the fl ligature the extractor left in the URL.",
      "source_locators": [
        "page:8:block:008"
      ]
    },
    {
      "witness_key": "work:eq-catalog",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The first block names the catalogue and picked arrivals deposited in Zenodo and carries the DOI up to the last digits, and the second block carries the remainder, so both halves of the identifier are cited.",
      "source_locators": [
        "page:8:block:008",
        "page:8:block:009"
      ]
    },
    {
      "witness_key": "work:petdb",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The caption block names the PetDb database as the source of the MORB whole rocks and the methods block gives its address and what was compiled from it.",
      "source_locators": [
        "page:6:block:005",
        "page:8:block:005"
      ]
    },
    {
      "witness_key": "work:ref-001",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The reference entry runs across the two cited blocks and carries the author, the title, the journal, the volume, the pages and the year.",
      "source_locators": [
        "page:8:block:012",
        "page:8:block:013"
      ]
    },
    {
      "witness_key": "work:ref-002",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The reference entry sits whole in one block with the author, the title, the journal, the volume, the pages and the year.",
      "source_locators": [
        "page:8:block:014"
      ]
    },
    {
      "witness_key": "work:ref-003",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 3 sits whole in the block with the two authors, the title, Nature, volume 440, pages 659 to 662 and 2006.",
      "source_locators": [
        "page:8:block:015"
      ]
    },
    {
      "witness_key": "work:ref-004",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 4 sits whole in the block; the record only rejoins the words the extractor broke across lines.",
      "source_locators": [
        "page:8:block:016"
      ]
    },
    {
      "witness_key": "work:ref-005",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 5 gives the authors, the title, Earth Planet. Sci. Lett., volume 45, pages 115 to 122 and 1979, all in the cited block.",
      "source_locators": [
        "page:8:block:017"
      ]
    },
    {
      "witness_key": "work:ref-006",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The entry is split across the page break: the first block holds the authors, title and journal, the second the volume, page and year, and both are cited.",
      "source_locators": [
        "page:9:block:001",
        "page:9:block:002"
      ]
    },
    {
      "witness_key": "work:ref-007",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The first block gives the authors, the chapter title, the monograph series, the pages and the DOI, the second block the 1992 year, so the book-chapter kind and all fields rest on cited text.",
      "source_locators": [
        "page:9:block:003",
        "page:9:block:004"
      ]
    },
    {
      "witness_key": "work:ref-008",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 8 sits whole in the block with author, title, J. Petrol., volume 25, pages 713 to 765 and 1984.",
      "source_locators": [
        "page:9:block:005"
      ]
    },
    {
      "witness_key": "work:ref-009",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 9 sits whole in the block with both authors, the title, the journal, volume 29, pages 625 to 679 and 1988.",
      "source_locators": [
        "page:9:block:006"
      ]
    },
    {
      "witness_key": "work:ref-010",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 10 carries the authors, the title, Nature, volume 364, pages 706 to 708 and 1993 in the cited block.",
      "source_locators": [
        "page:9:block:007"
      ]
    },
    {
      "witness_key": "work:ref-011",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 11 sits whole in the block; the long title is rejoined from the extractor's line breaks without change of wording.",
      "source_locators": [
        "page:9:block:008"
      ]
    },
    {
      "witness_key": "work:ref-012",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 12 gives the three authors, the title, Earth Planet. Sci. Lett., volume 233, pages 337 to 349 and 2005.",
      "source_locators": [
        "page:9:block:009"
      ]
    },
    {
      "witness_key": "work:ref-013",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 13 sits whole in the block with Grevemeyer et al., the title, Geology, volume 47, pages 1069 to 1073 and 2019.",
      "source_locators": [
        "page:9:block:010"
      ]
    },
    {
      "witness_key": "work:ref-014",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The author line and the rest of the entry fall in two consecutive blocks, both cited, and together carry every projected field.",
      "source_locators": [
        "page:9:block:011",
        "page:9:block:012"
      ]
    },
    {
      "witness_key": "work:ref-015",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 15 sits whole in the block; the record closes the stray space the extractor left inside the word Oceanic.",
      "source_locators": [
        "page:9:block:013"
      ]
    },
    {
      "witness_key": "work:ref-016",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The chapter, its editors, series and pages are in the first block and the DOI and year in the second; the record drops the accent the extractor kept on the second author's name.",
      "source_locators": [
        "page:9:block:014",
        "page:9:block:015"
      ]
    },
    {
      "witness_key": "work:ref-017",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 17 sits whole in the block with the four authors, the title, Nat. Geosci., volume 14, pages 606 to 611 and 2021.",
      "source_locators": [
        "page:9:block:016"
      ]
    },
    {
      "witness_key": "work:ref-018",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The authors and title are in the first block and the journal, volume, article number and year in the second, both cited.",
      "source_locators": [
        "page:9:block:017",
        "page:9:block:018"
      ]
    },
    {
      "witness_key": "work:ref-019",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 19 sits whole in the block; the record only closes the letter spacing the extractor produced in the author line.",
      "source_locators": [
        "page:9:block:019"
      ]
    },
    {
      "witness_key": "work:ref-020",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The authors, title and journal start in the first block and the volume, pages and year finish in the second, both cited.",
      "source_locators": [
        "page:9:block:020",
        "page:9:block:021"
      ]
    },
    {
      "witness_key": "work:ref-021",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 21 sits whole in the block and carries the conference abstract kind, the abstract number, the DOI and 2020.",
      "source_locators": [
        "page:9:block:022"
      ]
    },
    {
      "witness_key": "work:ref-022",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The cruise entry runs across two blocks, the first with the authors and the cruise name, the second with the DOI and the 2019 year.",
      "source_locators": [
        "page:9:block:023",
        "page:9:block:024"
      ]
    },
    {
      "witness_key": "work:ref-023",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The authors and title are in the first block and the journal, volume, pages and year in the second, both cited.",
      "source_locators": [
        "page:9:block:025",
        "page:9:block:026"
      ]
    },
    {
      "witness_key": "work:ref-024",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The author line and the rest of the entry are in consecutive blocks, both cited; the record normalises the accent and the letter spacing the extractor left.",
      "source_locators": [
        "page:9:block:027",
        "page:9:block:028"
      ]
    },
    {
      "witness_key": "work:ref-025",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 25 sits whole in the block and names the volume it is a chapter in, which is the book-chapter kind the record carries.",
      "source_locators": [
        "page:9:block:029"
      ]
    },
    {
      "witness_key": "work:ref-026",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 26 sits whole in the block with the authors, the title, the bulletin, volume 90, pages 1353 to 1368 and 2000.",
      "source_locators": [
        "page:9:block:030"
      ]
    },
    {
      "witness_key": "work:ref-027",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 27 sits in the block with the authors, the title, CORSSA, the page range, the DOI and the year in its trailing parenthesis.",
      "source_locators": [
        "page:9:block:031"
      ]
    },
    {
      "witness_key": "work:ref-028",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 28 begins in the block that also holds reference 27 and finishes in the next, and both are cited.",
      "source_locators": [
        "page:9:block:031",
        "page:9:block:032"
      ]
    },
    {
      "witness_key": "work:ref-029",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 29 sits whole in the block with the four authors, the title, the journal, volume 85, pages 1365 to 1387 and 1980.",
      "source_locators": [
        "page:9:block:033"
      ]
    },
    {
      "witness_key": "work:ref-030",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 30 sits whole in the block with Bonatti et al., the title, Geology, volume 29, pages 979 to 982 and 2001.",
      "source_locators": [
        "page:9:block:034"
      ]
    },
    {
      "witness_key": "work:ref-031",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 31 sits whole in the block with the four authors, the title, Nature, volume 434, pages 66 to 69 and 2005.",
      "source_locators": [
        "page:9:block:035"
      ]
    },
    {
      "witness_key": "work:ref-032",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 32 sits whole in the block with the two authors, the title, Nat. Commun., volume 13, article 7809 and 2022.",
      "source_locators": [
        "page:9:block:036"
      ]
    },
    {
      "witness_key": "work:ref-033",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The authors, title and journal name start in the first block and the volume, pages and year finish in the second, both cited.",
      "source_locators": [
        "page:9:block:037",
        "page:9:block:038"
      ]
    },
    {
      "witness_key": "work:ref-034",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 34 sits whole in the block with Cannat et al., the title, Geology, volume 34, pages 605 to 608 and 2006.",
      "source_locators": [
        "page:9:block:039"
      ]
    },
    {
      "witness_key": "work:ref-035",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 35 sits whole in the block; the record drops the umlaut the extractor kept on the first author's name and rejoins the journal title.",
      "source_locators": [
        "page:9:block:040"
      ]
    },
    {
      "witness_key": "work:ref-036",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 36 sits whole in the block with the five authors, the title, Nat. Commun., volume 11, article 4122 and 2020.",
      "source_locators": [
        "page:9:block:041"
      ]
    },
    {
      "witness_key": "work:ref-037",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 37 sits whole in the block; the record replaces the extractor's non-breaking hyphen in brittle-plastic with a plain one.",
      "source_locators": [
        "page:9:block:042"
      ]
    },
    {
      "witness_key": "work:ref-038",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 38 sits whole in the block with the three authors, the title, Nat. Commun., volume 14, article 430 and 2023.",
      "source_locators": [
        "page:9:block:043"
      ]
    },
    {
      "witness_key": "work:ref-039",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The authors, title and journal start in the first block and the volume, article number and year finish in the second, both cited.",
      "source_locators": [
        "page:9:block:044",
        "page:9:block:045"
      ]
    },
    {
      "witness_key": "work:ref-040",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The entry runs across the two cited blocks and together they carry the five authors, the title, the journal, the volume, the article number and the year.",
      "source_locators": [
        "page:9:block:046",
        "page:9:block:047"
      ]
    },
    {
      "witness_key": "work:ref-041",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 41 sits whole in the block with Wright et al., the title, Nat. Geosci., volume 5, pages 242 to 250 and 2012.",
      "source_locators": [
        "page:9:block:048"
      ]
    },
    {
      "witness_key": "work:ref-042",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 42 sits whole in the block with the two authors, the title, the journal, volume 120, pages 7771 to 7788 and 2015.",
      "source_locators": [
        "page:9:block:049"
      ]
    },
    {
      "witness_key": "work:ref-043",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 43 sits whole in the block with Greenfield et al., the title, Bull. Volcanol., volume 84, article 101 and 2022.",
      "source_locators": [
        "page:9:block:050"
      ]
    },
    {
      "witness_key": "work:ref-044",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 44 sits whole in the block; the record drops the accents the extractor kept on the first author's name.",
      "source_locators": [
        "page:9:block:051"
      ]
    },
    {
      "witness_key": "work:ref-045",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 45 sits whole in the block with Feuillet et al., the title, Nat. Geosci., volume 14, pages 787 to 795 and 2021.",
      "source_locators": [
        "page:9:block:052"
      ]
    },
    {
      "witness_key": "work:ref-046",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The authors, title and journal are in the first block and the volume, pages and year in the second, both cited.",
      "source_locators": [
        "page:9:block:053",
        "page:9:block:054"
      ]
    },
    {
      "witness_key": "work:ref-047",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 47 sits whole in the block with White et al., the title, Earth Planet. Sci. Lett., volume 304, pages 300 to 312 and 2011.",
      "source_locators": [
        "page:9:block:055"
      ]
    },
    {
      "witness_key": "work:ref-048",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The entry straddles the page break, with the authors and the first half of the title in one block and the rest of the title, the journal, volume, pages and year in the other.",
      "source_locators": [
        "page:9:block:056",
        "page:10:block:001"
      ]
    },
    {
      "witness_key": "work:ref-049",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 49 sits whole in the block with Kisslinger, the title, Eng. Geol., volume 10, pages 85 to 98 and 1976.",
      "source_locators": [
        "page:10:block:002"
      ]
    },
    {
      "witness_key": "work:ref-050",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 50 sits whole in the block; the record only closes the letter spacing the extractor produced in the author line.",
      "source_locators": [
        "page:10:block:003"
      ]
    },
    {
      "witness_key": "work:ref-051",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The authors, title and journal name start in the first block and the volume, pages and year finish in the second, both cited.",
      "source_locators": [
        "page:10:block:004",
        "page:10:block:005"
      ]
    },
    {
      "witness_key": "work:ref-052",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The entry runs across the two cited blocks and together they carry the four authors, the title, Nat. Commun., volume 8, the article number and 2017.",
      "source_locators": [
        "page:10:block:006",
        "page:10:block:007"
      ]
    },
    {
      "witness_key": "work:ref-053",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 53 sits whole in the block with the four authors, the title, Nature, volume 419, pages 451 to 455 and 2002.",
      "source_locators": [
        "page:10:block:008"
      ]
    },
    {
      "witness_key": "work:ref-054",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 54 sits whole in the block with the five authors, the title, the journal, volume 99, pages 12005 to 12028 and 1994.",
      "source_locators": [
        "page:10:block:009"
      ]
    },
    {
      "witness_key": "work:ref-055",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 55 sits whole in the block with Schilling et al., the long title, the journal, volume 100, pages 10057 to 10076 and 1995.",
      "source_locators": [
        "page:10:block:010"
      ]
    },
    {
      "witness_key": "work:ref-056",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 56 sits whole in the block; the record's title keeps the block's wording and leaves out only the trailing latitude range the entry gives in parentheses.",
      "source_locators": [
        "page:10:block:011"
      ]
    },
    {
      "witness_key": "work:ref-057",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 57 sits whole in the block with the three authors, the title, J. Petrol., volume 55, pages 1051 to 1082 and 2014.",
      "source_locators": [
        "page:10:block:012"
      ]
    },
    {
      "witness_key": "work:ref-058",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The authors, title and journal name are in the first block and the volume, pages and year in the second, both cited.",
      "source_locators": [
        "page:10:block:013",
        "page:10:block:014"
      ]
    },
    {
      "witness_key": "work:ref-059",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 59 sits whole in the block with Shapiro et al., the title, Nat. Geosci., volume 10, pages 442 to 445 and 2017.",
      "source_locators": [
        "page:10:block:015"
      ]
    },
    {
      "witness_key": "work:ref-060",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 60 sits whole in the block with the three authors, the title, Science, volume 368, pages 775 to 779 and 2020.",
      "source_locators": [
        "page:10:block:016"
      ]
    },
    {
      "witness_key": "work:ref-061",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 61 sits whole in the block; the record rejoins the last author's surname that the extractor split across lines.",
      "source_locators": [
        "page:10:block:017"
      ]
    },
    {
      "witness_key": "work:ref-062",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 62 sits whole in the block; the record writes the 85E of the title as 85 degrees East and keeps everything else.",
      "source_locators": [
        "page:10:block:018"
      ]
    },
    {
      "witness_key": "work:ref-063",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 63 sits whole in the block with the three authors, the title, Earth Planet. Sci. Lett., volume 464, pages 55 to 68 and 2017.",
      "source_locators": [
        "page:10:block:019"
      ]
    },
    {
      "witness_key": "work:ref-064",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 64 sits whole in the block with the two authors, the title, Sci. Adv., volume 8, the article number and 2022.",
      "source_locators": [
        "page:10:block:020"
      ]
    },
    {
      "witness_key": "work:ref-065",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 65 sits whole in the block with the two authors, the title, Nat. Geosci., volume 11, pages 65 to 69 and 2018.",
      "source_locators": [
        "page:10:block:021"
      ]
    },
    {
      "witness_key": "work:ref-066",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The author line and the rest of the entry fall in consecutive blocks, both cited, and together carry every projected field.",
      "source_locators": [
        "page:10:block:022",
        "page:10:block:023"
      ]
    },
    {
      "witness_key": "work:ref-067",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 67 sits whole in the block with the three authors, the title, Earth Planet. Sci. Lett., volume 621, the article number and 2023.",
      "source_locators": [
        "page:10:block:024"
      ]
    },
    {
      "witness_key": "work:ref-068",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 68 sits whole in the block with Kissling, the title, Rev. Geophys., volume 26, pages 659 to 698 and 1988.",
      "source_locators": [
        "page:10:block:025"
      ]
    },
    {
      "witness_key": "work:ref-069",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 69 sits whole in the block; the record replaces the non-breaking hyphen in two-dimensional with a plain one.",
      "source_locators": [
        "page:10:block:026"
      ]
    },
    {
      "witness_key": "work:ref-070",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The authors, title and the start of the journal name are in the first block and the volume, pages and year in the second, both cited.",
      "source_locators": [
        "page:10:block:027",
        "page:10:block:028"
      ]
    },
    {
      "witness_key": "work:ref-071",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 71 sits whole in the block with Wiemer, the title, Seismol. Res. Lett., volume 72, pages 373 to 382 and 2001.",
      "source_locators": [
        "page:10:block:029"
      ]
    },
    {
      "witness_key": "work:ref-072",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 72 sits whole in the block with the two authors, the title, the bulletin, volume 92, pages 2264 to 2276 and 2002.",
      "source_locators": [
        "page:10:block:030"
      ]
    },
    {
      "witness_key": "work:ref-073",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The entry runs across three cited blocks: the authors, then the title and the start of the address, then the last part of the address and the year, so the preprint kind and the full URL both rest on cited text.",
      "source_locators": [
        "page:10:block:031",
        "page:10:block:032",
        "page:10:block:033"
      ]
    },
    {
      "witness_key": "work:ref-074",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 74 sits whole in the block; the record replaces the non-breaking hyphen in Segment-scale with a plain one.",
      "source_locators": [
        "page:10:block:034"
      ]
    },
    {
      "witness_key": "work:ref-075",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The authors, title and journal name start in the first block and the volume, DOI and year finish in the second, both cited.",
      "source_locators": [
        "page:10:block:035",
        "page:10:block:036"
      ]
    },
    {
      "witness_key": "work:ref-076",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 76 sits whole in the block with the four authors, the title, Geochim. Cosmochim. Acta, volume 97, pages 1 to 23 and 2012.",
      "source_locators": [
        "page:10:block:037"
      ]
    },
    {
      "witness_key": "work:ref-077",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The authors, title and the start of the journal name are in the first block and the volume, pages and year in the second, both cited.",
      "source_locators": [
        "page:10:block:038",
        "page:10:block:039"
      ]
    },
    {
      "witness_key": "work:ref-078",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW Reference 78 sits whole in the block with Hicks et al., the title naming the 2016 Mw 7.1 Romanche earthquake, Nat. Geosci., volume 13, pages 647 to 653 and 2020.",
      "source_locators": [
        "page:10:block:040"
      ]
    },
    {
      "witness_key": "work:ref-079",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The authors and title are in the first block and the journal, volume, pages and year in the second; the record's title keeps the block's wording and leaves out the two parenthetical lists the entry carries.",
      "source_locators": [
        "page:10:block:041",
        "page:10:block:042"
      ]
    },
    {
      "witness_key": "work:zenodo",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The data availability block names the Zenodo database as the repository the catalogue was deposited in, which is the name and the database kind.",
      "source_locators": [
        "page:8:block:008"
      ]
    },
    {
      "witness_key": "rel:mar-in-atlantic",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The one sentence that places the Mid-Atlantic Ridge in the equatorial Atlantic Ocean is in the same block that derives both endpoint records, and it carries the LOCATED_IN sense directly.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "rel:rc1-bounded-detachment",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The sentence putting a westward dipping detachment fault on the eastern boundary of the RTI segment is in the block that derives both endpoints, so the BOUNDED_BY relation and its endpoints rest on the same text.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "rel:rc2-adjacent-ntd1",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The sentence placing the segment RC2 immediately south of NTD1 is in a block that also derives the NTD1 endpoint, and being directly south of it is what the ADJACENT_TO sense rests on.",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "rel:rc2-bounded-faults",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The sentence saying RC2 is bounded by the high-angle inward dipping faults is the same text that derives the fault endpoint, so relation and target rest on one block.",
      "source_locators": [
        "page:4:block:001"
      ]
    },
    {
      "witness_key": "rel:rc3-adjacent-ntd2",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The sentence naming the ridge segment south of NTD2 as RC3 sits in a block that derives both endpoints, and the southward adjacency is stated in it.",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "rel:catalog-in-zenodo",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The data availability sentence says the catalogue was deposited in the Zenodo database, and that block derives both endpoints, so the DEPOSITED_IN relation is local to it.",
      "source_locators": [
        "page:8:block:008"
      ]
    },
    {
      "witness_key": "cruise:smarties",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The blocks name the SMARTIES cruise, describe it as the passive OBS experiment that acquired the microseismicity data, and give about 21 days as the continuous recording span the record carries as its duration; the source states that span of the recording rather than of the ship time, which the record's own description is about.",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ]
    },
    {
      "witness_key": "instr:obs",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The blocks name the ocean-bottom seismometers and their OBS abbreviation and say the study's data were recorded by them.",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ]
    },
    {
      "witness_key": "method:cross-correlation",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block says the relocation used differential travel times from the original catalogue together with waveform cross-correlation data, which is the name and the description.",
      "source_locators": [
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "method:depth-resolution-tests",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block reports that tests of depth resolution were run to check how reliable the earthquake locations are, which is the name and the description.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "method:double-difference",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block says the hypocentres were relocated using a double-difference location method, which is the name and the stated use.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "method:fc-correction",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block says that after correcting for fractional crystallisation the CO2 concentrations in melts in equilibrium with the mantle source were calculated, which is the name and the description.",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "method:first-motion",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the P-phase first-motion polarities and says they were picked from unfiltered vertical-component waveforms and used for the focal mechanisms.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "method:local-magnitude",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The results block says local magnitudes were determined and the methods block repeats it with the scale used.",
      "source_locators": [
        "page:2:block:002",
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "method:location-criteria",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The first block says the locations were classified into four categories on the basis of well-established criteria and the second sets those criteria out.",
      "source_locators": [
        "page:2:block:003",
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "method:ml-formula",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the local magnitude scale ML and states that the maximum amplitude comes from a simulated Wood-Anderson seismogram and that the distance is hypocentral in kilometres; the retained gap notes only that the formula itself has no type.",
      "source_locators": [
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "method:nonlinear-location",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block says a non-linear earthquake location algorithm was used to obtain the hypocentres, which is the name and the description.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "method:stalta",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the short-term-average over long-term-average trigger algorithm and says it detected the initial arrivals automatically.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "method:station-corrections",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block says station corrections were calculated and updated.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "method:swave-delay-removal",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The same sentence reports the removal of the S-wave delays attributed to slow unconsolidated sediments, which is the name and the description.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "method:wadati",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the Wadati diagrams and says they yield the Vp/Vs ratio, which is what the description states.",
      "source_locators": [
        "page:7:block:002"
      ]
    },
    {
      "witness_key": "sw:global-mapper",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The code availability block names Global Mapper, its use for structural analysis and its address.",
      "source_locators": [
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "sw:gmt6",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The first block names the GMT 6 toolbox, its use for graphing and the start of its address, and the second block carries the rest of that address.",
      "source_locators": [
        "page:8:block:010",
        "page:8:block:011"
      ]
    },
    {
      "witness_key": "sw:hash",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The methods block names the HASH package for focal mechanisms and the code availability block gives version 1.2 and the address.",
      "source_locators": [
        "page:8:block:003",
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "sw:hypodd",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The methods block names the hypoDD program used for the relocations and the code availability block gives the name, version 1.3, the stated use and the address.",
      "source_locators": [
        "page:7:block:006",
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "sw:nonlinloc",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The methods block names NonLinLoc and its oct-tree search for the initial hypocentres and the code availability block gives the address.",
      "source_locators": [
        "page:7:block:004",
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "sw:seisan",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The three cited blocks name SEISAN for the automatic detection, for the Wood-Anderson simulation and for phase picking with its address, which is name, description and URL.",
      "source_locators": [
        "page:6:block:002",
        "page:8:block:002",
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "sw:velest",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The methods block names the VELEST program and its search for the minimum 1-D model and the code availability block gives the address and the inversion use.",
      "source_locators": [
        "page:6:block:004",
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "sw:zmap",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The methods block names ZMAP as what calculated the b value and magnitude completeness and the code availability block gives the address and the same use.",
      "source_locators": [
        "page:8:block:002",
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "rel:hash-used-for-focal",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL One sentence says the first-motion polarities were used with the HASH package to determine focal mechanisms, and that block derives both endpoints.",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "rel:nonlinloc-used-for-location",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The sentence naming the non-linear oct-tree search algorithm of NonLinLoc as what located the initial hypocentres is in a block that derives the software endpoint, so the USED_FOR relation is local to that endpoint even though the method record also draws on an earlier block.",
      "source_locators": [
        "page:7:block:004"
      ]
    },
    {
      "witness_key": "rel:seisan-used-for-stalta",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The sentence putting the trigger algorithm inside the SEISAN package is in a block that derives the SEISAN endpoint, so the relation sits with one of its endpoints.",
      "source_locators": [
        "page:6:block:002"
      ]
    },
    {
      "witness_key": "award:erc-advanced",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The funding block names the ERC Advanced Grant agreement and gives its number 339442_TransAtlanticILAB.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "award:fp7",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The same block names the European Union's Seventh Framework Program and gives FP7/2007-2013 as the programme, with the letter spacing the extractor left closed up in the record.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "award:investissements",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the French government programme Investissements d'Avenir, which is both the name and the programme the record carries.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "award:isblue",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the ISblue project, its description as the interdisciplinary graduate school for the blue planet and its ANR number, which the record writes without the stray dash the extractor inserted.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "award:nsfc",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the National Natural Science Foundation of China and gives both grant numbers the record lists.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "award:sad",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the SAD program of the Regional Council of Brittany.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "award:zjnsf",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the Zhejiang Provincial Natural Science Foundation of China and gives the award number the record carries.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "agent:briais",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The author line names Anne Briais as a person and the contributions block carries her initials; the retained gaps concern affiliation and contributor role, neither of which this record claims.",
      "source_locators": [
        "page:1:block:001",
        "page:10:block:045"
      ]
    },
    {
      "witness_key": "agent:brittany",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The funding block names the Regional Council of Brittany, which is an organisation and not a person.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "agent:brunelli",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The author line names Daniele Brunelli, which the record reconstructs from the letter spacing the extractor produced, and the contributions block carries his initials.",
      "source_locators": [
        "page:1:block:001",
        "page:10:block:045"
      ]
    },
    {
      "witness_key": "agent:erc",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The funding block names the European Research Council, an organisation and not a person.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "agent:french-government",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The funding block names the French government as one of the funders, which is the name and the organisation type.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "agent:grenet",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The author line names Lea Grenet as a person, with the accent the record drops, and the contributions block carries her initials.",
      "source_locators": [
        "page:1:block:001",
        "page:10:block:045"
      ]
    },
    {
      "witness_key": "agent:hamelin",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The author line names Cedric Hamelin as a person, again with the accent the record drops, and the contributions block carries his initials.",
      "source_locators": [
        "page:1:block:001",
        "page:10:block:045"
      ]
    },
    {
      "witness_key": "agent:maia",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The author line names Marcia Maia as a person and the contributions block carries her initials.",
      "source_locators": [
        "page:1:block:001",
        "page:10:block:045"
      ]
    },
    {
      "witness_key": "agent:nsfc",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The acknowledgements block names the National Natural Science Foundation of China as a funding organisation.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "agent:org-cnr-igag",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The affiliation block carries the fifth entry, the Cnr institute in Rome, word for word as the record's name; the retained gap concerns the independent-scholar entry, not this one.",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "agent:org-geoocean",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The affiliation block carries the second entry, Geo-Ocean UMR6538 with its consortium, as the record's name.",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "agent:org-ipgp",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The affiliation block carries the third entry, the Paris university, institute and CNRS, with the accents the record drops.",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "agent:org-sio",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The affiliation block carries the first entry, the Hangzhou laboratory, institute and ministry, as the record's name.",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "agent:org-unimore",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The affiliation block carries the sixth entry, the Modena department and university, as the record's name.",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "agent:petracchini",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The author line names Lorenzo Petracchini as a person and the contributions block carries his initials.",
      "source_locators": [
        "page:1:block:001",
        "page:10:block:045"
      ]
    },
    {
      "witness_key": "agent:singh",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The author line names Satish C. Singh, spaced by the extractor and rejoined in the record, and the correspondence block names him again in clean type.",
      "source_locators": [
        "page:1:block:001",
        "page:11:block:002"
      ]
    },
    {
      "witness_key": "agent:tgir",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The acknowledgements block names the TGIR French Oceanographic Fleet as what funded the ship time, an organisation.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "agent:yu",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The author line and the correspondence block both name Zhiteng Yu as a person.",
      "source_locators": [
        "page:1:block:001",
        "page:11:block:002"
      ]
    },
    {
      "witness_key": "agent:zjnsf",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The acknowledgements block names the Zhejiang Provincial Natural Science Foundation of China as a funding organisation.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "rel:singh-funded-erc",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The funding sentence names the ERC Advanced Grant agreement and says it went to S.C.S, and that same block derives both endpoints, the award and the initials the person record carries.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "rel:singh-funded-fp7",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The same sentence names the Seventh Framework Program funding to S.C.S, and the block derives both endpoints; the recipient is named there by initials rather than in full.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "rel:yu-funded-nsfc",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The sentence says Z.Y. is partly funded by the National Natural Science Foundation of China, and the block derives both endpoints; the record carries the funding link without the word partly that qualifies its extent.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "rel:yu-funded-zjnsf",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL The same sentence names the Zhejiang provincial award to Z.Y., and the block derives both endpoints of the relation.",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "model:co2-solubility",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the CO2 solubility model and says it is what gives the saturation pressure and temperature, which is the record's name, kind and description.",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "model:iacono-marziano",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the model of Iacono-Marziano et al. and says the theoretical CO2 solubility of the measured samples was calculated from it.",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "model:min-1d",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the minimum 1-D velocity model searched for with VELEST and sets it against the selected model.",
      "source_locators": [
        "page:6:block:004"
      ]
    },
    {
      "witness_key": "model:thermal",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names thermal modelling and gives the temperatures it suggests beneath the RC2 segment axis, which is the record's name, kind and description.",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "model:thermal-simulated",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The caption block says the isotherms are extracted from a simulated thermal model, which is the name, the kind and the stated use.",
      "source_locators": [
        "page:7:block:012"
      ]
    },
    {
      "witness_key": "model:velocity-1d",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names the one-dimensional velocity model and says it is what travel times were calculated with during the locations.",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "model:velocity-model-1",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names Model 1 as the fastest model, derived from the southern Romanche transform, and reports the shallow crustal events it produces.",
      "source_locators": [
        "page:7:block:009"
      ]
    },
    {
      "witness_key": "model:velocity-model-5",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW The block names Model 5, calls the average north-to-south model the best-fitting one and says it was selected for the later location and focal mechanism work.",
      "source_locators": [
        "page:6:block:003"
      ]
    }
  ],
  "questions": [
    {
      "question_id": "CQ-T1-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The cruise row names the campaign and describes it as the experiment during which the microseismicity data were acquired, and a separate instrument row carries the ocean-bottom seismometer network. Nothing in the row representation joins the two, so the answer is read off two rows that stand side by side.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "campaign_name",
          "row_index": 0,
          "absent_reason": null,
          "note": "The name field carries SMARTIES cruise."
        },
        {
          "semantic": "observing_system",
          "row_index": 1,
          "absent_reason": null,
          "note": "The instrument row names the ocean-bottom seismometers whose records the study uses."
        },
        {
          "semantic": "data_acquisition",
          "row_index": 0,
          "absent_reason": null,
          "note": "The description field states that this is the experiment during which the microseismicity data were acquired."
        }
      ],
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "cruise:smarties"
        },
        {
          "row_index": 1,
          "witness_key": "instr:obs"
        },
        {
          "row_index": 2,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 3,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 4,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 5,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 6,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 7,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 8,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 9,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 10,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 11,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 12,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 13,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 14,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 15,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 16,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 17,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 18,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 19,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 20,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 21,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 22,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 23,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 24,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 25,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 26,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 27,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 28,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 29,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 30,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 31,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 32,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 33,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 34,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 35,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 36,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 37,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 38,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 39,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 40,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 41,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 42,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 43,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 44,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 45,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 46,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 47,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 48,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 49,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 50,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 51,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 52,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 53,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 54,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 55,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 56,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 57,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 58,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 59,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 60,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 61,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 62,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 63,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 64,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 65,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 66,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 67,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 68,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 69,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 70,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 71,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 72,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 73,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 74,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 75,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 76,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 77,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 79,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 80,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 81,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 82,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 83,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 84,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 85,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 86,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 87,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 88,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 89,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 90,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 91,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 92,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 93,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 94,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 95,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 96,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 97,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 98,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 99,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 100,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 101,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 102,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 103,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 104,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 105,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 106,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 107,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 108,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 109,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 110,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 111,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 112,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 113,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 114,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 115,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 116,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 117,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 118,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 119,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 120,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 121,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 122,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 123,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 124,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 125,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 126,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 127,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 128,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 129,
          "witness_key": "obs:thermal-model-temp"
        }
      ]
    },
    {
      "question_id": "CQ-T1-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The count row gives nineteen instruments and names the acquiring network as its scope, the instrument row carries the network itself, and the cruise row is the experiment the deployment sentence derives. The three rows are not joined by anything in the result.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "instrument_count",
          "row_index": 76,
          "absent_reason": null,
          "note": "The count field carries nineteen and the scope names the network of ocean-bottom seismometers."
        },
        {
          "semantic": "observing_system",
          "row_index": 1,
          "absent_reason": null,
          "note": "The instrument row names the ocean-bottom seismometers."
        },
        {
          "semantic": "deployment_event",
          "row_index": 0,
          "absent_reason": null,
          "note": "The cruise row is the experiment the deployment sentence derives; its fields name the campaign and describe the experiment rather than the act of deploying."
        }
      ],
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "cruise:smarties"
        },
        {
          "row_index": 1,
          "witness_key": "instr:obs"
        },
        {
          "row_index": 2,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 3,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 4,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 5,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 6,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 7,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 8,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 9,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 10,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 11,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 12,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 13,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 14,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 15,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 16,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 17,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 18,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 19,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 20,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 21,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 22,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 23,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 24,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 25,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 26,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 27,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 28,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 29,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 30,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 31,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 32,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 33,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 34,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 35,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 36,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 37,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 38,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 39,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 40,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 41,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 42,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 43,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 44,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 45,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 46,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 47,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 48,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 49,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 50,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 51,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 52,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 53,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 54,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 55,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 56,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 57,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 58,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 59,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 60,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 61,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 62,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 63,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 64,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 65,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 66,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 67,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 68,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 69,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 70,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 71,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 72,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 73,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 74,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 75,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 76,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 77,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 79,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 80,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 81,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 82,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 83,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 84,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 85,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 86,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 87,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 88,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 89,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 90,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 91,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 92,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 93,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 94,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 95,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 96,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 97,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 98,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 99,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 100,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 101,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 102,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 103,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 104,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 105,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 106,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 107,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 108,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 109,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 110,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 111,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 112,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 113,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 114,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 115,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 116,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 117,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 118,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 119,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 120,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 121,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 122,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 123,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 124,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 125,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 126,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 127,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 128,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 129,
          "witness_key": "obs:thermal-model-temp"
        }
      ]
    },
    {
      "question_id": "CQ-T1-03",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The article row carries the publication record, but the received and accepted dates are held only as a retained assertion that formalizes no record, so nothing in the result carries an acceptance event or its date.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "publication_record",
          "row_index": 0,
          "absent_reason": null,
          "note": "The row carries the article with its DOI, journal, year, volume and page."
        },
        {
          "semantic": "acceptance_event",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "The capture retains the sentence with the received and accepted dates, and that assertion formalizes no record, so no acceptance event exists in the graph."
        },
        {
          "semantic": "calendar_date",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "The accepted date is in the same retained assertion and no record or field carries it."
        }
      ],
      "source_locators": [
        "page:11:block:005",
        "page:1:block:001",
        "page:1:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "work:article"
        },
        {
          "row_index": 1,
          "witness_key": "work:cruise-portal"
        },
        {
          "row_index": 2,
          "witness_key": "work:eq-catalog"
        },
        {
          "row_index": 3,
          "witness_key": "work:petdb"
        },
        {
          "row_index": 4,
          "witness_key": "work:ref-001"
        },
        {
          "row_index": 5,
          "witness_key": "work:ref-002"
        },
        {
          "row_index": 6,
          "witness_key": "work:ref-003"
        },
        {
          "row_index": 7,
          "witness_key": "work:ref-004"
        },
        {
          "row_index": 8,
          "witness_key": "work:ref-005"
        },
        {
          "row_index": 9,
          "witness_key": "work:ref-006"
        },
        {
          "row_index": 10,
          "witness_key": "work:ref-007"
        },
        {
          "row_index": 11,
          "witness_key": "work:ref-008"
        },
        {
          "row_index": 12,
          "witness_key": "work:ref-009"
        },
        {
          "row_index": 13,
          "witness_key": "work:ref-010"
        },
        {
          "row_index": 14,
          "witness_key": "work:ref-011"
        },
        {
          "row_index": 15,
          "witness_key": "work:ref-012"
        },
        {
          "row_index": 16,
          "witness_key": "work:ref-013"
        },
        {
          "row_index": 17,
          "witness_key": "work:ref-014"
        },
        {
          "row_index": 18,
          "witness_key": "work:ref-015"
        },
        {
          "row_index": 19,
          "witness_key": "work:ref-016"
        },
        {
          "row_index": 20,
          "witness_key": "work:ref-017"
        },
        {
          "row_index": 21,
          "witness_key": "work:ref-018"
        },
        {
          "row_index": 22,
          "witness_key": "work:ref-019"
        },
        {
          "row_index": 23,
          "witness_key": "work:ref-020"
        },
        {
          "row_index": 24,
          "witness_key": "work:ref-021"
        },
        {
          "row_index": 25,
          "witness_key": "work:ref-022"
        },
        {
          "row_index": 26,
          "witness_key": "work:ref-023"
        },
        {
          "row_index": 27,
          "witness_key": "work:ref-024"
        },
        {
          "row_index": 28,
          "witness_key": "work:ref-025"
        },
        {
          "row_index": 29,
          "witness_key": "work:ref-026"
        },
        {
          "row_index": 30,
          "witness_key": "work:ref-027"
        },
        {
          "row_index": 31,
          "witness_key": "work:ref-028"
        },
        {
          "row_index": 32,
          "witness_key": "work:ref-029"
        },
        {
          "row_index": 33,
          "witness_key": "work:ref-030"
        },
        {
          "row_index": 34,
          "witness_key": "work:ref-031"
        },
        {
          "row_index": 35,
          "witness_key": "work:ref-032"
        },
        {
          "row_index": 36,
          "witness_key": "work:ref-033"
        },
        {
          "row_index": 37,
          "witness_key": "work:ref-034"
        },
        {
          "row_index": 38,
          "witness_key": "work:ref-035"
        },
        {
          "row_index": 39,
          "witness_key": "work:ref-036"
        },
        {
          "row_index": 40,
          "witness_key": "work:ref-037"
        },
        {
          "row_index": 41,
          "witness_key": "work:ref-038"
        },
        {
          "row_index": 42,
          "witness_key": "work:ref-039"
        },
        {
          "row_index": 43,
          "witness_key": "work:ref-040"
        },
        {
          "row_index": 44,
          "witness_key": "work:ref-041"
        },
        {
          "row_index": 45,
          "witness_key": "work:ref-042"
        },
        {
          "row_index": 46,
          "witness_key": "work:ref-043"
        },
        {
          "row_index": 47,
          "witness_key": "work:ref-044"
        },
        {
          "row_index": 48,
          "witness_key": "work:ref-045"
        },
        {
          "row_index": 49,
          "witness_key": "work:ref-046"
        },
        {
          "row_index": 50,
          "witness_key": "work:ref-047"
        },
        {
          "row_index": 51,
          "witness_key": "work:ref-048"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref-049"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref-050"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref-051"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref-052"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref-053"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref-054"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref-055"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref-056"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref-057"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref-058"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref-059"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref-060"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref-061"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref-062"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref-063"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref-064"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref-065"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref-066"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref-067"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref-068"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref-069"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref-070"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref-071"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref-072"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref-073"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref-074"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref-075"
        },
        {
          "row_index": 79,
          "witness_key": "work:ref-076"
        },
        {
          "row_index": 80,
          "witness_key": "work:ref-077"
        },
        {
          "row_index": 81,
          "witness_key": "work:ref-078"
        },
        {
          "row_index": 82,
          "witness_key": "work:ref-079"
        },
        {
          "row_index": 83,
          "witness_key": "work:zenodo"
        },
        {
          "row_index": 84,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 85,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 86,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 87,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 88,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 89,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 90,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 91,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 92,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 93,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 94,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 95,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 96,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 97,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 98,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 99,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 100,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 101,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 102,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 103,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 104,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 105,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 106,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 107,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 108,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 109,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 110,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 111,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 112,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 113,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 114,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 115,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 116,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 117,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 118,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 119,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 120,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 121,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 122,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 123,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 124,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 125,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 126,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 127,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 128,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 129,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 130,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 131,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 132,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 133,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 134,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 135,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 136,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 137,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 138,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 139,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 140,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 141,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 142,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 143,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 144,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 145,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 146,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 147,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 148,
          "witness_key": "rel:catalog-in-zenodo"
        },
        {
          "row_index": 149,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 150,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 151,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 152,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 153,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 154,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 155,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 156,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 157,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 158,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 159,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 160,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 161,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 162,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 163,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 164,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 165,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 166,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 167,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 168,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 169,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 170,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 171,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 172,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 173,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 174,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 175,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 176,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 177,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 178,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 179,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 180,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 181,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 182,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 183,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 184,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 185,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 186,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 187,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 188,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 189,
          "witness_key": "claim:volatiles-reduce-solidus"
        }
      ]
    },
    {
      "question_id": "CQ-T1-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The dataset row carries the catalogue and its Zenodo identifier, the repository row carries the database, and a DEPOSITED_IN relation row in the same result joins them.",
      "assembly": "LINKED_ROWS",
      "coverage": [
        {
          "semantic": "dataset_record",
          "row_index": 2,
          "absent_reason": null,
          "note": "The row names the earthquake catalogue and picked arrivals generated in this study."
        },
        {
          "semantic": "repository_name",
          "row_index": 83,
          "absent_reason": null,
          "note": "The row names the Zenodo database."
        },
        {
          "semantic": "persistent_identifier",
          "row_index": 2,
          "absent_reason": null,
          "note": "The doi field carries the Zenodo identifier, whose last digits fall in a second reading block that the witness also cites."
        }
      ],
      "source_locators": [
        "page:8:block:008",
        "page:8:block:009"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "work:article"
        },
        {
          "row_index": 1,
          "witness_key": "work:cruise-portal"
        },
        {
          "row_index": 2,
          "witness_key": "work:eq-catalog"
        },
        {
          "row_index": 3,
          "witness_key": "work:petdb"
        },
        {
          "row_index": 4,
          "witness_key": "work:ref-001"
        },
        {
          "row_index": 5,
          "witness_key": "work:ref-002"
        },
        {
          "row_index": 6,
          "witness_key": "work:ref-003"
        },
        {
          "row_index": 7,
          "witness_key": "work:ref-004"
        },
        {
          "row_index": 8,
          "witness_key": "work:ref-005"
        },
        {
          "row_index": 9,
          "witness_key": "work:ref-006"
        },
        {
          "row_index": 10,
          "witness_key": "work:ref-007"
        },
        {
          "row_index": 11,
          "witness_key": "work:ref-008"
        },
        {
          "row_index": 12,
          "witness_key": "work:ref-009"
        },
        {
          "row_index": 13,
          "witness_key": "work:ref-010"
        },
        {
          "row_index": 14,
          "witness_key": "work:ref-011"
        },
        {
          "row_index": 15,
          "witness_key": "work:ref-012"
        },
        {
          "row_index": 16,
          "witness_key": "work:ref-013"
        },
        {
          "row_index": 17,
          "witness_key": "work:ref-014"
        },
        {
          "row_index": 18,
          "witness_key": "work:ref-015"
        },
        {
          "row_index": 19,
          "witness_key": "work:ref-016"
        },
        {
          "row_index": 20,
          "witness_key": "work:ref-017"
        },
        {
          "row_index": 21,
          "witness_key": "work:ref-018"
        },
        {
          "row_index": 22,
          "witness_key": "work:ref-019"
        },
        {
          "row_index": 23,
          "witness_key": "work:ref-020"
        },
        {
          "row_index": 24,
          "witness_key": "work:ref-021"
        },
        {
          "row_index": 25,
          "witness_key": "work:ref-022"
        },
        {
          "row_index": 26,
          "witness_key": "work:ref-023"
        },
        {
          "row_index": 27,
          "witness_key": "work:ref-024"
        },
        {
          "row_index": 28,
          "witness_key": "work:ref-025"
        },
        {
          "row_index": 29,
          "witness_key": "work:ref-026"
        },
        {
          "row_index": 30,
          "witness_key": "work:ref-027"
        },
        {
          "row_index": 31,
          "witness_key": "work:ref-028"
        },
        {
          "row_index": 32,
          "witness_key": "work:ref-029"
        },
        {
          "row_index": 33,
          "witness_key": "work:ref-030"
        },
        {
          "row_index": 34,
          "witness_key": "work:ref-031"
        },
        {
          "row_index": 35,
          "witness_key": "work:ref-032"
        },
        {
          "row_index": 36,
          "witness_key": "work:ref-033"
        },
        {
          "row_index": 37,
          "witness_key": "work:ref-034"
        },
        {
          "row_index": 38,
          "witness_key": "work:ref-035"
        },
        {
          "row_index": 39,
          "witness_key": "work:ref-036"
        },
        {
          "row_index": 40,
          "witness_key": "work:ref-037"
        },
        {
          "row_index": 41,
          "witness_key": "work:ref-038"
        },
        {
          "row_index": 42,
          "witness_key": "work:ref-039"
        },
        {
          "row_index": 43,
          "witness_key": "work:ref-040"
        },
        {
          "row_index": 44,
          "witness_key": "work:ref-041"
        },
        {
          "row_index": 45,
          "witness_key": "work:ref-042"
        },
        {
          "row_index": 46,
          "witness_key": "work:ref-043"
        },
        {
          "row_index": 47,
          "witness_key": "work:ref-044"
        },
        {
          "row_index": 48,
          "witness_key": "work:ref-045"
        },
        {
          "row_index": 49,
          "witness_key": "work:ref-046"
        },
        {
          "row_index": 50,
          "witness_key": "work:ref-047"
        },
        {
          "row_index": 51,
          "witness_key": "work:ref-048"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref-049"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref-050"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref-051"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref-052"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref-053"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref-054"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref-055"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref-056"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref-057"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref-058"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref-059"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref-060"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref-061"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref-062"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref-063"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref-064"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref-065"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref-066"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref-067"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref-068"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref-069"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref-070"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref-071"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref-072"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref-073"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref-074"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref-075"
        },
        {
          "row_index": 79,
          "witness_key": "work:ref-076"
        },
        {
          "row_index": 80,
          "witness_key": "work:ref-077"
        },
        {
          "row_index": 81,
          "witness_key": "work:ref-078"
        },
        {
          "row_index": 82,
          "witness_key": "work:ref-079"
        },
        {
          "row_index": 83,
          "witness_key": "work:zenodo"
        },
        {
          "row_index": 84,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 85,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 86,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 87,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 88,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 89,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 90,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 91,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 92,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 93,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 94,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 95,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 96,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 97,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 98,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 99,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 100,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 101,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 102,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 103,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 104,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 105,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 106,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 107,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 108,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 109,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 110,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 111,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 112,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 113,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 114,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 115,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 116,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 117,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 118,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 119,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 120,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 121,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 122,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 123,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 124,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 125,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 126,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 127,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 128,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 129,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 130,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 131,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 132,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 133,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 134,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 135,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 136,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 137,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 138,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 139,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 140,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 141,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 142,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 143,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 144,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 145,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 146,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 147,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 148,
          "witness_key": "rel:catalog-in-zenodo"
        },
        {
          "row_index": 149,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 150,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 151,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 152,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 153,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 154,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 155,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 156,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 157,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 158,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 159,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 160,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 161,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 162,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 163,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 164,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 165,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 166,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 167,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 168,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 169,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 170,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 171,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 172,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 173,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 174,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 175,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 176,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 177,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 178,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 179,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 180,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 181,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 182,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 183,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 184,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 185,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 186,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 187,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 188,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 189,
          "witness_key": "claim:volatiles-reduce-solidus"
        }
      ]
    },
    {
      "question_id": "CQ-T1-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The cruise row carries the recording span as a single duration string and the instrument row carries the network. The value and its unit are inside one field rather than typed separately, and nothing joins the two rows.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "recording_interval",
          "row_index": 0,
          "absent_reason": null,
          "note": "The duration field carries the continuous recording span of about twenty-one days."
        },
        {
          "semantic": "duration_value",
          "row_index": 0,
          "absent_reason": null,
          "note": "The number sits inside the same duration string; the graph carries no separate value field for it."
        },
        {
          "semantic": "time_unit",
          "row_index": 0,
          "absent_reason": null,
          "note": "The unit days sits inside the same duration string."
        },
        {
          "semantic": "observing_system",
          "row_index": 1,
          "absent_reason": null,
          "note": "The instrument row names the ocean-bottom seismometers."
        }
      ],
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "cruise:smarties"
        },
        {
          "row_index": 1,
          "witness_key": "instr:obs"
        },
        {
          "row_index": 2,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 3,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 4,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 5,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 6,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 7,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 8,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 9,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 10,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 11,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 12,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 13,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 14,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 15,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 16,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 17,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 18,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 19,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 20,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 21,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 22,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 23,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 24,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 25,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 26,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 27,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 28,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 29,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 30,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 31,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 32,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 33,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 34,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 35,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 36,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 37,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 38,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 39,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 40,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 41,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 42,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 43,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 44,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 45,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 46,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 47,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 48,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 49,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 50,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 51,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 52,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 53,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 54,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 55,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 56,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 57,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 58,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 59,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 60,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 61,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 62,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 63,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 64,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 65,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 66,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 67,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 68,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 69,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 70,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 71,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 72,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 73,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 74,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 75,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 76,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 77,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 79,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 80,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 81,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 82,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 83,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 84,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 85,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 86,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 87,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 88,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 89,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 90,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 91,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 92,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 93,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 94,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 95,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 96,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 97,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 98,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 99,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 100,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 101,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 102,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 103,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 104,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 105,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 106,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 107,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 108,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 109,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 110,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 111,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 112,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 113,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 114,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 115,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 116,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 117,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 118,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 119,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 120,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 121,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 122,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 123,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 124,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 125,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 126,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 127,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 128,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 129,
          "witness_key": "obs:thermal-model-temp"
        }
      ]
    },
    {
      "question_id": "CQ-T2-01",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The subsection, the detachment fault and the BOUNDED_BY relation that joins them are all in the result, but which side of the ridge axis the core complex sits on is stated only inside the assertion the rows bind by locator and digest; no projected field carries it.",
      "assembly": "LINKED_ROWS",
      "coverage": [
        {
          "semantic": "named_subsection",
          "row_index": 25,
          "absent_reason": null,
          "note": "The row names RC1 and its RTI segment kind."
        },
        {
          "semantic": "structural_feature",
          "row_index": 3,
          "absent_reason": null,
          "note": "The row names the westward dipping detachment fault."
        },
        {
          "semantic": "bounding_relation",
          "row_index": 97,
          "absent_reason": null,
          "note": "The relation row carries BOUNDED_BY between the subsection and the fault."
        },
        {
          "semantic": "side_of_axis",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "The sentence puts the core complex on the eastern side of the ridge axis; the claim record holds that sentence as a locator and a digest and no field carries the side."
        }
      ],
      "source_locators": [
        "page:1:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 33,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 34,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 35,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 36,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 37,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 38,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 39,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 40,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 41,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 42,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 43,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 44,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 45,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 46,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 47,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 48,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 49,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 50,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 51,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 52,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 53,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 54,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 55,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 56,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 57,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 58,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 59,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 60,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 61,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 62,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 63,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 64,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 65,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 66,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 67,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 68,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 69,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 70,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 71,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 72,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 73,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 74,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 75,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 76,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 77,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 78,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 79,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 80,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 81,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 83,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 84,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 85,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 86,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 87,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 88,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 89,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 90,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 91,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 92,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 93,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 94,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 95,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 96,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 97,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 98,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 99,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 100,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 101,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 102,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 103,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 104,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 105,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 106,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 107,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 108,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 109,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 110,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 111,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 112,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 113,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 114,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 115,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 116,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 117,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 118,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 119,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 120,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 121,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 122,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 123,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 124,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 125,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 126,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 127,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 128,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 129,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 130,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 131,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 132,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 133,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 134,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 135,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 136,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 137,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 138,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 139,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 140,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 141,
          "witness_key": "claim:selected-model-more-events"
        }
      ]
    },
    {
      "question_id": "CQ-T2-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One software row carries the program that produced the initial hypocentres, another the program applied afterwards, a method row states the relocation of those hypocentres and the dataset row carries the catalogue. No relation in the result joins the two programs to each other.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "initial_location_method",
          "row_index": 101,
          "absent_reason": null,
          "note": "The row names NonLinLoc and describes its oct-tree search for the initial hypocentres."
        },
        {
          "semantic": "relocation_method",
          "row_index": 100,
          "absent_reason": null,
          "note": "The row names HypoDD and describes its use for double-difference relocation."
        },
        {
          "semantic": "method_sequence",
          "row_index": 2,
          "absent_reason": null,
          "note": "The description field says this method relocated the hypocentres the other obtained, which is the ordering; the word then is only in the assertion the record binds by digest."
        },
        {
          "semantic": "earthquake_catalog",
          "row_index": 15,
          "absent_reason": null,
          "note": "The row carries the earthquake catalogue generated in this study."
        }
      ],
      "source_locators": [
        "page:2:block:002",
        "page:7:block:004",
        "page:7:block:006",
        "page:8:block:008",
        "page:8:block:009",
        "page:8:block:010"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "method:cross-correlation"
        },
        {
          "row_index": 1,
          "witness_key": "method:depth-resolution-tests"
        },
        {
          "row_index": 2,
          "witness_key": "method:double-difference"
        },
        {
          "row_index": 3,
          "witness_key": "method:fc-correction"
        },
        {
          "row_index": 4,
          "witness_key": "method:first-motion"
        },
        {
          "row_index": 5,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 6,
          "witness_key": "method:location-criteria"
        },
        {
          "row_index": 7,
          "witness_key": "method:ml-formula"
        },
        {
          "row_index": 8,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 9,
          "witness_key": "method:stalta"
        },
        {
          "row_index": 10,
          "witness_key": "method:station-corrections"
        },
        {
          "row_index": 11,
          "witness_key": "method:swave-delay-removal"
        },
        {
          "row_index": 12,
          "witness_key": "method:wadati"
        },
        {
          "row_index": 13,
          "witness_key": "work:article"
        },
        {
          "row_index": 14,
          "witness_key": "work:cruise-portal"
        },
        {
          "row_index": 15,
          "witness_key": "work:eq-catalog"
        },
        {
          "row_index": 16,
          "witness_key": "work:petdb"
        },
        {
          "row_index": 17,
          "witness_key": "work:ref-001"
        },
        {
          "row_index": 18,
          "witness_key": "work:ref-002"
        },
        {
          "row_index": 19,
          "witness_key": "work:ref-003"
        },
        {
          "row_index": 20,
          "witness_key": "work:ref-004"
        },
        {
          "row_index": 21,
          "witness_key": "work:ref-005"
        },
        {
          "row_index": 22,
          "witness_key": "work:ref-006"
        },
        {
          "row_index": 23,
          "witness_key": "work:ref-007"
        },
        {
          "row_index": 24,
          "witness_key": "work:ref-008"
        },
        {
          "row_index": 25,
          "witness_key": "work:ref-009"
        },
        {
          "row_index": 26,
          "witness_key": "work:ref-010"
        },
        {
          "row_index": 27,
          "witness_key": "work:ref-011"
        },
        {
          "row_index": 28,
          "witness_key": "work:ref-012"
        },
        {
          "row_index": 29,
          "witness_key": "work:ref-013"
        },
        {
          "row_index": 30,
          "witness_key": "work:ref-014"
        },
        {
          "row_index": 31,
          "witness_key": "work:ref-015"
        },
        {
          "row_index": 32,
          "witness_key": "work:ref-016"
        },
        {
          "row_index": 33,
          "witness_key": "work:ref-017"
        },
        {
          "row_index": 34,
          "witness_key": "work:ref-018"
        },
        {
          "row_index": 35,
          "witness_key": "work:ref-019"
        },
        {
          "row_index": 36,
          "witness_key": "work:ref-020"
        },
        {
          "row_index": 37,
          "witness_key": "work:ref-021"
        },
        {
          "row_index": 38,
          "witness_key": "work:ref-022"
        },
        {
          "row_index": 39,
          "witness_key": "work:ref-023"
        },
        {
          "row_index": 40,
          "witness_key": "work:ref-024"
        },
        {
          "row_index": 41,
          "witness_key": "work:ref-025"
        },
        {
          "row_index": 42,
          "witness_key": "work:ref-026"
        },
        {
          "row_index": 43,
          "witness_key": "work:ref-027"
        },
        {
          "row_index": 44,
          "witness_key": "work:ref-028"
        },
        {
          "row_index": 45,
          "witness_key": "work:ref-029"
        },
        {
          "row_index": 46,
          "witness_key": "work:ref-030"
        },
        {
          "row_index": 47,
          "witness_key": "work:ref-031"
        },
        {
          "row_index": 48,
          "witness_key": "work:ref-032"
        },
        {
          "row_index": 49,
          "witness_key": "work:ref-033"
        },
        {
          "row_index": 50,
          "witness_key": "work:ref-034"
        },
        {
          "row_index": 51,
          "witness_key": "work:ref-035"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref-036"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref-037"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref-038"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref-039"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref-040"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref-041"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref-042"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref-043"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref-044"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref-045"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref-046"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref-047"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref-048"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref-049"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref-050"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref-051"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref-052"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref-053"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref-054"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref-055"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref-056"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref-057"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref-058"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref-059"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref-060"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref-061"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref-062"
        },
        {
          "row_index": 79,
          "witness_key": "work:ref-063"
        },
        {
          "row_index": 80,
          "witness_key": "work:ref-064"
        },
        {
          "row_index": 81,
          "witness_key": "work:ref-065"
        },
        {
          "row_index": 82,
          "witness_key": "work:ref-066"
        },
        {
          "row_index": 83,
          "witness_key": "work:ref-067"
        },
        {
          "row_index": 84,
          "witness_key": "work:ref-068"
        },
        {
          "row_index": 85,
          "witness_key": "work:ref-069"
        },
        {
          "row_index": 86,
          "witness_key": "work:ref-070"
        },
        {
          "row_index": 87,
          "witness_key": "work:ref-071"
        },
        {
          "row_index": 88,
          "witness_key": "work:ref-072"
        },
        {
          "row_index": 89,
          "witness_key": "work:ref-073"
        },
        {
          "row_index": 90,
          "witness_key": "work:ref-074"
        },
        {
          "row_index": 91,
          "witness_key": "work:ref-075"
        },
        {
          "row_index": 92,
          "witness_key": "work:ref-076"
        },
        {
          "row_index": 93,
          "witness_key": "work:ref-077"
        },
        {
          "row_index": 94,
          "witness_key": "work:ref-078"
        },
        {
          "row_index": 95,
          "witness_key": "work:ref-079"
        },
        {
          "row_index": 96,
          "witness_key": "work:zenodo"
        },
        {
          "row_index": 97,
          "witness_key": "sw:global-mapper"
        },
        {
          "row_index": 98,
          "witness_key": "sw:gmt6"
        },
        {
          "row_index": 99,
          "witness_key": "sw:hash"
        },
        {
          "row_index": 100,
          "witness_key": "sw:hypodd"
        },
        {
          "row_index": 101,
          "witness_key": "sw:nonlinloc"
        },
        {
          "row_index": 102,
          "witness_key": "sw:seisan"
        },
        {
          "row_index": 103,
          "witness_key": "sw:velest"
        },
        {
          "row_index": 104,
          "witness_key": "sw:zmap"
        },
        {
          "row_index": 105,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 106,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 107,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 108,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 109,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 110,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 111,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 112,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 113,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 114,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 115,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 116,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 117,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 118,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 119,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 120,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 121,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 122,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 123,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 124,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 125,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 126,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 127,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 128,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 129,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 130,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 131,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 132,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 133,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 134,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 135,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 136,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 137,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 138,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 139,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 140,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 141,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 142,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 143,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 144,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 145,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 146,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 147,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 148,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 149,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 150,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 151,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 152,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 153,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 154,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 155,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 156,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 157,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 158,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 159,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 160,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 161,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 162,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 163,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 164,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 165,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 166,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 167,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 168,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 169,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 170,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 171,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 172,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 173,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 174,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 175,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 176,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 177,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 178,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 179,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 180,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 181,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 182,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 183,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 184,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 185,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 186,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 187,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 188,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 189,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 190,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 191,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 192,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 193,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 194,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 195,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 196,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 197,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 198,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 199,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 200,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 201,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 202,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 203,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 204,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 205,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 206,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 207,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 208,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 209,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 210,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 211,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 212,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 213,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 214,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 215,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 216,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 217,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 218,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 219,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 220,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 221,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 222,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 223,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 224,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 225,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 226,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 227,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 228,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 229,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 230,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 231,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 232,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 233,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 234,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 235,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 236,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 237,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 238,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 239,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 240,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 241,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 242,
          "witness_key": "rel:catalog-in-zenodo"
        },
        {
          "row_index": 243,
          "witness_key": "rel:hash-used-for-focal"
        },
        {
          "row_index": 244,
          "witness_key": "rel:nonlinloc-used-for-location"
        },
        {
          "row_index": 245,
          "witness_key": "rel:seisan-used-for-stalta"
        },
        {
          "row_index": 246,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 247,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 248,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 249,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 250,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 251,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 252,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 253,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 254,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 255,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 256,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 257,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 258,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 259,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 260,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 261,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 262,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 263,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 264,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 265,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 266,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 267,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 268,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 269,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 270,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 271,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 272,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 273,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 274,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 275,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 276,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 277,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 278,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 279,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 280,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 281,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 282,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 283,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 284,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 285,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 286,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 287,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 288,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 289,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 290,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 291,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 292,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 293,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 294,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 295,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 296,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 297,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 298,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 299,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 300,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 301,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 302,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 303,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 304,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 305,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 306,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 307,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 308,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 309,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 310,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 311,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 312,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 313,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 314,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 315,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 316,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 317,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 318,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 319,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 320,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 321,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 322,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 323,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 324,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 325,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 326,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 327,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 328,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 329,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 330,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 331,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 332,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 333,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 334,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 335,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 336,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 337,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 338,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 339,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 340,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 341,
          "witness_key": "obs:thermal-model-temp"
        }
      ]
    },
    {
      "question_id": "CQ-T2-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The vent field and the discontinuity are separate entity rows and one claim row carries both the flank it sits on and its distance from the present-day axial valley. Nothing in the row representation joins the vent-field row to the claim.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "named_feature",
          "row_index": 5,
          "absent_reason": null,
          "note": "The row names the extinct hydrothermal vent field."
        },
        {
          "semantic": "host_discontinuity",
          "row_index": 18,
          "absent_reason": null,
          "note": "The row names NTD1, which is also the claim row's subject."
        },
        {
          "semantic": "spatial_relation",
          "row_index": 183,
          "absent_reason": null,
          "note": "The name field places the vent field on the eastern flank of NTD1 and far from the present-day axial valley."
        },
        {
          "semantic": "present_day_axis",
          "row_index": 183,
          "absent_reason": null,
          "note": "The same name field names the present-day axial valley; no separate record for it exists."
        }
      ],
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001",
        "page:3:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 33,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 34,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 35,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 36,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 37,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 38,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 39,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 40,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 41,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 42,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 43,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 44,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 45,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 46,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 47,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 48,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 49,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 50,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 51,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 52,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 53,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 54,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 55,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 56,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 57,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 58,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 59,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 60,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 61,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 62,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 63,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 64,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 65,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 66,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 67,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 68,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 69,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 70,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 71,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 72,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 73,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 74,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 75,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 76,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 77,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 78,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 79,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 80,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 81,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 83,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 84,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 85,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 86,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 87,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 88,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 89,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 90,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 91,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 92,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 93,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 94,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 95,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 96,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 100,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 111,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 112,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 113,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 114,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 115,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 116,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 117,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 118,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 119,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 120,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 121,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 122,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 123,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 124,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 125,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 126,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 127,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 128,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 129,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 130,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 131,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 132,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 133,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 134,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 135,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 136,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 137,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 138,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 139,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 140,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 141,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 142,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 143,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 144,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 145,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 146,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 147,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 148,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 149,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 150,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 151,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 152,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 153,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 154,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 155,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 156,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 157,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 158,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 159,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 160,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 161,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 162,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 163,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 164,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 165,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 166,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 167,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 168,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 169,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 170,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 171,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 172,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 173,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 174,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 175,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 176,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 177,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 178,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 179,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 180,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 181,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 182,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 183,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 184,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 185,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 186,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 187,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 188,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 189,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 190,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 191,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 192,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 193,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 194,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 195,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 196,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 197,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 198,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 199,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 200,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 201,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 202,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 203,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 204,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 205,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 206,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 207,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 208,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 209,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 210,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 211,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 212,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 213,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 214,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 215,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 216,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 217,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 218,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 219,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 220,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 221,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 222,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 223,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 224,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 225,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 226,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 227,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 228,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 229,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 230,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 231,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 232,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 233,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 234,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 235,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 236,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 237,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 238,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 239,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 240,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 241,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 242,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 243,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 244,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 245,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 246,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 247,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 248,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 249,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 250,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 251,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 252,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 253,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 254,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 255,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 256,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 257,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 258,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 259,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 260,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 261,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 262,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 263,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 264,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 265,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 266,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 267,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 268,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 269,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-T2-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The thickness, the flank it belongs to and the crustal age are carried by two observation rows, and the earlier study is a reference row in the same result. No row states that this reference is the one the thickness is cited from; the citation marker is inside the assertion the observation binds by digest.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "source_study",
          "row_index": 67,
          "absent_reason": null,
          "note": "The row carries the 2022 study on crustal accretion in the equatorial Atlantic, which is the reference the thickness sentence cites; no field in the result carries that citation link."
        },
        {
          "semantic": "crustal_thickness_claim",
          "row_index": 208,
          "absent_reason": null,
          "note": "The row carries 5.4 plus or minus 0.3 km."
        },
        {
          "semantic": "location_relation",
          "row_index": 208,
          "absent_reason": null,
          "note": "The name field attributes the thickness to the crust of the western ridge flank."
        },
        {
          "semantic": "crustal_age",
          "row_index": 207,
          "absent_reason": null,
          "note": "The row carries the 8 Ma age of that crust."
        }
      ],
      "source_locators": [
        "page:2:block:006",
        "page:9:block:036"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "work:article"
        },
        {
          "row_index": 33,
          "witness_key": "work:cruise-portal"
        },
        {
          "row_index": 34,
          "witness_key": "work:eq-catalog"
        },
        {
          "row_index": 35,
          "witness_key": "work:petdb"
        },
        {
          "row_index": 36,
          "witness_key": "work:ref-001"
        },
        {
          "row_index": 37,
          "witness_key": "work:ref-002"
        },
        {
          "row_index": 38,
          "witness_key": "work:ref-003"
        },
        {
          "row_index": 39,
          "witness_key": "work:ref-004"
        },
        {
          "row_index": 40,
          "witness_key": "work:ref-005"
        },
        {
          "row_index": 41,
          "witness_key": "work:ref-006"
        },
        {
          "row_index": 42,
          "witness_key": "work:ref-007"
        },
        {
          "row_index": 43,
          "witness_key": "work:ref-008"
        },
        {
          "row_index": 44,
          "witness_key": "work:ref-009"
        },
        {
          "row_index": 45,
          "witness_key": "work:ref-010"
        },
        {
          "row_index": 46,
          "witness_key": "work:ref-011"
        },
        {
          "row_index": 47,
          "witness_key": "work:ref-012"
        },
        {
          "row_index": 48,
          "witness_key": "work:ref-013"
        },
        {
          "row_index": 49,
          "witness_key": "work:ref-014"
        },
        {
          "row_index": 50,
          "witness_key": "work:ref-015"
        },
        {
          "row_index": 51,
          "witness_key": "work:ref-016"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref-017"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref-018"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref-019"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref-020"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref-021"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref-022"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref-023"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref-024"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref-025"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref-026"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref-027"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref-028"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref-029"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref-030"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref-031"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref-032"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref-033"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref-034"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref-035"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref-036"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref-037"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref-038"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref-039"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref-040"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref-041"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref-042"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref-043"
        },
        {
          "row_index": 79,
          "witness_key": "work:ref-044"
        },
        {
          "row_index": 80,
          "witness_key": "work:ref-045"
        },
        {
          "row_index": 81,
          "witness_key": "work:ref-046"
        },
        {
          "row_index": 82,
          "witness_key": "work:ref-047"
        },
        {
          "row_index": 83,
          "witness_key": "work:ref-048"
        },
        {
          "row_index": 84,
          "witness_key": "work:ref-049"
        },
        {
          "row_index": 85,
          "witness_key": "work:ref-050"
        },
        {
          "row_index": 86,
          "witness_key": "work:ref-051"
        },
        {
          "row_index": 87,
          "witness_key": "work:ref-052"
        },
        {
          "row_index": 88,
          "witness_key": "work:ref-053"
        },
        {
          "row_index": 89,
          "witness_key": "work:ref-054"
        },
        {
          "row_index": 90,
          "witness_key": "work:ref-055"
        },
        {
          "row_index": 91,
          "witness_key": "work:ref-056"
        },
        {
          "row_index": 92,
          "witness_key": "work:ref-057"
        },
        {
          "row_index": 93,
          "witness_key": "work:ref-058"
        },
        {
          "row_index": 94,
          "witness_key": "work:ref-059"
        },
        {
          "row_index": 95,
          "witness_key": "work:ref-060"
        },
        {
          "row_index": 96,
          "witness_key": "work:ref-061"
        },
        {
          "row_index": 97,
          "witness_key": "work:ref-062"
        },
        {
          "row_index": 98,
          "witness_key": "work:ref-063"
        },
        {
          "row_index": 99,
          "witness_key": "work:ref-064"
        },
        {
          "row_index": 100,
          "witness_key": "work:ref-065"
        },
        {
          "row_index": 101,
          "witness_key": "work:ref-066"
        },
        {
          "row_index": 102,
          "witness_key": "work:ref-067"
        },
        {
          "row_index": 103,
          "witness_key": "work:ref-068"
        },
        {
          "row_index": 104,
          "witness_key": "work:ref-069"
        },
        {
          "row_index": 105,
          "witness_key": "work:ref-070"
        },
        {
          "row_index": 106,
          "witness_key": "work:ref-071"
        },
        {
          "row_index": 107,
          "witness_key": "work:ref-072"
        },
        {
          "row_index": 108,
          "witness_key": "work:ref-073"
        },
        {
          "row_index": 109,
          "witness_key": "work:ref-074"
        },
        {
          "row_index": 110,
          "witness_key": "work:ref-075"
        },
        {
          "row_index": 111,
          "witness_key": "work:ref-076"
        },
        {
          "row_index": 112,
          "witness_key": "work:ref-077"
        },
        {
          "row_index": 113,
          "witness_key": "work:ref-078"
        },
        {
          "row_index": 114,
          "witness_key": "work:ref-079"
        },
        {
          "row_index": 115,
          "witness_key": "work:zenodo"
        },
        {
          "row_index": 116,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 117,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 118,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 119,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 120,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 121,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 122,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 123,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 124,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 125,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 126,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 127,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 128,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 129,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 130,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 131,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 132,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 133,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 134,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 135,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 136,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 137,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 138,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 139,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 140,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 141,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 142,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 143,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 144,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 145,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 146,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 147,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 148,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 149,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 150,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 151,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 152,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 153,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 154,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 155,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 156,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 157,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 158,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 159,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 160,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 161,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 162,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 163,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 164,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 165,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 166,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 167,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 168,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 169,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 170,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 171,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 172,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 173,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 174,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 175,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 176,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 177,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 178,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 179,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 180,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 181,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 182,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 183,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 184,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 185,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 186,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 187,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 188,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 189,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 190,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 191,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 192,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 193,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 194,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 195,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 196,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 197,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 198,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 199,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 200,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 201,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 202,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 203,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 204,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 205,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 206,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 207,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 208,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 209,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 210,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 211,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 212,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 213,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 214,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 215,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 216,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 217,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 218,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 219,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 220,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 221,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 222,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 223,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 224,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 225,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 226,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 227,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 228,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 229,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 230,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 231,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 232,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 233,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 234,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 235,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 236,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 237,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 238,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 239,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 240,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 241,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 242,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 243,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 244,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 245,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 246,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 247,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 248,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 249,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 250,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 251,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 252,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 253,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 254,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 255,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 256,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 257,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 258,
          "witness_key": "rel:catalog-in-zenodo"
        },
        {
          "row_index": 259,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 260,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 261,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 262,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 263,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 264,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 265,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 266,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 267,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 268,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 269,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 270,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 271,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 272,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 273,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 274,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 275,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 276,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 277,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 278,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 279,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 280,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 281,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 282,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 283,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 284,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 285,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 286,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 287,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 288,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 289,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 290,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 291,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 292,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 293,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 294,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 295,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 296,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 297,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 298,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 299,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 300,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 301,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 302,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 303,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 304,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 305,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 306,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 307,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 308,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 309,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 310,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 311,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 312,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 313,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 314,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 315,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 316,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 317,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 318,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 319,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 320,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 321,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 322,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 323,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 324,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 325,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 326,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 327,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 328,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 329,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 330,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 331,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 332,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 333,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 334,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 335,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 336,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 337,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 338,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 339,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 340,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 341,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 342,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 343,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 344,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 345,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 346,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 347,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 348,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 349,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 350,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 351,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 352,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 353,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 354,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-T2-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The award row carries the named grant and its number, the agent row carries the author and a FUNDED_BY relation row joins them.",
      "assembly": "LINKED_ROWS",
      "coverage": [
        {
          "semantic": "funding_record",
          "row_index": 0,
          "absent_reason": null,
          "note": "The row names the ERC Advanced Grant agreement."
        },
        {
          "semantic": "grant_identifier",
          "row_index": 0,
          "absent_reason": null,
          "note": "The award identifier field carries the agreement number."
        },
        {
          "semantic": "person",
          "row_index": 22,
          "absent_reason": null,
          "note": "The row carries the individual author, named in the funding sentence by initials."
        },
        {
          "semantic": "attribution_relation",
          "row_index": 26,
          "absent_reason": null,
          "note": "The relation row carries FUNDED_BY from the author to the award."
        }
      ],
      "source_locators": [
        "page:10:block:044",
        "page:11:block:002",
        "page:1:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "award:erc-advanced"
        },
        {
          "row_index": 1,
          "witness_key": "award:fp7"
        },
        {
          "row_index": 2,
          "witness_key": "award:investissements"
        },
        {
          "row_index": 3,
          "witness_key": "award:isblue"
        },
        {
          "row_index": 4,
          "witness_key": "award:nsfc"
        },
        {
          "row_index": 5,
          "witness_key": "award:sad"
        },
        {
          "row_index": 6,
          "witness_key": "award:zjnsf"
        },
        {
          "row_index": 7,
          "witness_key": "agent:briais"
        },
        {
          "row_index": 8,
          "witness_key": "agent:brittany"
        },
        {
          "row_index": 9,
          "witness_key": "agent:brunelli"
        },
        {
          "row_index": 10,
          "witness_key": "agent:erc"
        },
        {
          "row_index": 11,
          "witness_key": "agent:french-government"
        },
        {
          "row_index": 12,
          "witness_key": "agent:grenet"
        },
        {
          "row_index": 13,
          "witness_key": "agent:hamelin"
        },
        {
          "row_index": 14,
          "witness_key": "agent:maia"
        },
        {
          "row_index": 15,
          "witness_key": "agent:nsfc"
        },
        {
          "row_index": 16,
          "witness_key": "agent:org-cnr-igag"
        },
        {
          "row_index": 17,
          "witness_key": "agent:org-geoocean"
        },
        {
          "row_index": 18,
          "witness_key": "agent:org-ipgp"
        },
        {
          "row_index": 19,
          "witness_key": "agent:org-sio"
        },
        {
          "row_index": 20,
          "witness_key": "agent:org-unimore"
        },
        {
          "row_index": 21,
          "witness_key": "agent:petracchini"
        },
        {
          "row_index": 22,
          "witness_key": "agent:singh"
        },
        {
          "row_index": 23,
          "witness_key": "agent:tgir"
        },
        {
          "row_index": 24,
          "witness_key": "agent:yu"
        },
        {
          "row_index": 25,
          "witness_key": "agent:zjnsf"
        },
        {
          "row_index": 26,
          "witness_key": "rel:singh-funded-erc"
        },
        {
          "row_index": 27,
          "witness_key": "rel:singh-funded-fp7"
        },
        {
          "row_index": 28,
          "witness_key": "rel:yu-funded-nsfc"
        },
        {
          "row_index": 29,
          "witness_key": "rel:yu-funded-zjnsf"
        }
      ]
    },
    {
      "question_id": "CQ-T3-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One observation row carries the depth range, its unit, its subject and its measured status, and a second row carries the same earthquakes with the below-seafloor reference. The two rows are not joined in the result.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 236,
          "absent_reason": null,
          "note": "The row carries 16 to 19 km."
        },
        {
          "semantic": "length_unit",
          "row_index": 236,
          "absent_reason": null,
          "note": "The unit field carries km."
        },
        {
          "semantic": "quantity_subject",
          "row_index": 236,
          "absent_reason": null,
          "note": "The subject reference resolves to the segment RC2."
        },
        {
          "semantic": "measurement_status",
          "row_index": 236,
          "absent_reason": null,
          "note": "The determination and modality fields both read as measured, matching the observed wording."
        },
        {
          "semantic": "depth_reference_surface",
          "row_index": 242,
          "absent_reason": null,
          "note": "That row carries the same deep earthquakes with a below-seafloor depth reference."
        }
      ],
      "source_locators": [
        "page:2:block:006",
        "page:7:block:012"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 33,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 34,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 35,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 36,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 37,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 38,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 39,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 40,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 41,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 42,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 43,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 44,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 45,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 46,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 47,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 48,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 49,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 50,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 51,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 52,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 53,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 54,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 55,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 56,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 57,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 58,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 59,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 60,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 61,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 62,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 63,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 64,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 65,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 66,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 67,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 68,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 69,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 70,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 71,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 72,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 73,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 74,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 75,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 76,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 77,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 78,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 79,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 80,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 81,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 83,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 84,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 85,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 86,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 87,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 88,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 89,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 90,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 91,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 92,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 93,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 94,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 95,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 96,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 100,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 111,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 112,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 113,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 114,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 115,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 116,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 117,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 118,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 119,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 120,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 121,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 122,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 123,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 124,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 125,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 126,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 127,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 128,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 129,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 130,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 131,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 132,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 133,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 134,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 135,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 136,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 137,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 138,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 139,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 140,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 141,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 142,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 143,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 144,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 145,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 146,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 147,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 148,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 149,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 150,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 151,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 152,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 153,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 154,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 155,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 156,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 157,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 158,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 159,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 160,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 161,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 162,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 163,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 164,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 165,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 166,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 167,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 168,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 169,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 170,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 171,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 172,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 173,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 174,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 175,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 176,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 177,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 178,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 179,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 180,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 181,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 182,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 183,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 184,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 185,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 186,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 187,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 188,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 189,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 190,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 191,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 192,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 193,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 194,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 195,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 196,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 197,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 198,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 199,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 200,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 201,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 202,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 203,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 204,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 205,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 206,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 207,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 208,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 209,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 210,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 211,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 212,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 213,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 214,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 215,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 216,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 217,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 218,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 219,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 220,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 221,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 222,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 223,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 224,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 225,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 226,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 227,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 228,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 229,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 230,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 231,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 232,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 233,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 234,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 235,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 236,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 237,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 238,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 239,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 240,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 241,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 242,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 243,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 244,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 245,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 246,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 247,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 248,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 249,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 250,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 251,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 252,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 253,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 254,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 255,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 256,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 257,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 258,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 259,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 260,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 261,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 262,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 263,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 264,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 265,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 266,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 267,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 268,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 269,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 270,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-T3-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One geochemical row carries the range, the unit, the segment it belongs to and the calculated determination.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 229,
          "absent_reason": null,
          "note": "The row carries 0.4 to 3.0 wt%."
        },
        {
          "semantic": "concentration_unit",
          "row_index": 229,
          "absent_reason": null,
          "note": "The unit field carries wt%."
        },
        {
          "semantic": "quantity_subject",
          "row_index": 229,
          "absent_reason": null,
          "note": "The subject reference resolves to the segment RC2."
        },
        {
          "semantic": "calculated_or_measured_status",
          "row_index": 229,
          "absent_reason": null,
          "note": "The quantity kind is written as CO2 calculated and the determination is derived."
        }
      ],
      "source_locators": [
        "page:5:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "sample:melt-inclusions"
        },
        {
          "row_index": 33,
          "witness_key": "sample:morb-obs-network"
        },
        {
          "row_index": 34,
          "witness_key": "sample:morb-rc2"
        },
        {
          "row_index": 35,
          "witness_key": "sample:morb-rc3"
        },
        {
          "row_index": 36,
          "witness_key": "sample:popping-rocks"
        },
        {
          "row_index": 37,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 38,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 39,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 40,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 41,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 42,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 43,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 44,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 45,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 46,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 47,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 48,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 49,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 50,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 51,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 52,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 53,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 54,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 55,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 56,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 57,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 58,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 59,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 60,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 61,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 62,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 63,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 64,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 65,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 66,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 67,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 68,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 69,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 70,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 71,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 72,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 73,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 74,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 75,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 76,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 77,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 78,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 79,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 80,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 81,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 82,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 83,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 84,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 85,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 86,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 87,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 88,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 89,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 90,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 91,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 92,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 93,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 94,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 95,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 96,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 97,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 98,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 99,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 100,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 111,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 112,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 113,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 114,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 115,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 116,
          "witness_key": "ratio:co2-ba"
        },
        {
          "row_index": 117,
          "witness_key": "ratio:co2-rb"
        },
        {
          "row_index": 118,
          "witness_key": "ratio:vp-vs"
        },
        {
          "row_index": 119,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 120,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 121,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 122,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 123,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 124,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 125,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 126,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 127,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 128,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 129,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 130,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 131,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 132,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 133,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 134,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 135,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 136,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 137,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 138,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 139,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 140,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 141,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 142,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 143,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 144,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 145,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 146,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 147,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 148,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 149,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 150,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 151,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 152,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 153,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 154,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 155,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 156,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 157,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 158,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 159,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 160,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 161,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 162,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 163,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 164,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 165,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 166,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 167,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 168,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 169,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 170,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 171,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 172,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 173,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 174,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 175,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 176,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 177,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 178,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 179,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 180,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 181,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 182,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 183,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 184,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 185,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 186,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 187,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 188,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 189,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 190,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 191,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 192,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 193,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 194,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 195,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 196,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 197,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 198,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 199,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 200,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 201,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 202,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 203,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 204,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 205,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 206,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 207,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 208,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 209,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 210,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 211,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 212,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 213,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 214,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 215,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 216,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 217,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 218,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 219,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 220,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 221,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 222,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 223,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 224,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 225,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 226,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 227,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 228,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 229,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 230,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 231,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 232,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 233,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 234,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 235,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 236,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 237,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 238,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 239,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 240,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 241,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 242,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 243,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 244,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 245,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 246,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 247,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 248,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 249,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 250,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 251,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 252,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 253,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 254,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 255,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 256,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 257,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 258,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 259,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 260,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 261,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 262,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 263,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 264,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 265,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 266,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 267,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 268,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 269,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 270,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 271,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 272,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 273,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 274,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 275,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 276,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 277,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-T3-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One geochemical row carries the pre-eruptive range, its unit, the melt stage and the estimated determination.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 228,
          "absent_reason": null,
          "note": "The row carries 0.7 to 4.6 wt%."
        },
        {
          "semantic": "concentration_unit",
          "row_index": 228,
          "absent_reason": null,
          "note": "The unit field carries wt%."
        },
        {
          "semantic": "melt_stage",
          "row_index": 228,
          "absent_reason": null,
          "note": "The melt stage field reads pre-eruptive melt."
        },
        {
          "semantic": "estimation_status",
          "row_index": 228,
          "absent_reason": null,
          "note": "The determination field reads estimated, matching the word estimated in the source sentence."
        }
      ],
      "source_locators": [
        "page:5:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "sample:melt-inclusions"
        },
        {
          "row_index": 33,
          "witness_key": "sample:morb-obs-network"
        },
        {
          "row_index": 34,
          "witness_key": "sample:morb-rc2"
        },
        {
          "row_index": 35,
          "witness_key": "sample:morb-rc3"
        },
        {
          "row_index": 36,
          "witness_key": "sample:popping-rocks"
        },
        {
          "row_index": 37,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 38,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 39,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 40,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 41,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 42,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 43,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 44,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 45,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 46,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 47,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 48,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 49,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 50,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 51,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 52,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 53,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 54,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 55,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 56,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 57,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 58,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 59,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 60,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 61,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 62,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 63,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 64,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 65,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 66,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 67,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 68,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 69,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 70,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 71,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 72,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 73,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 74,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 75,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 76,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 77,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 78,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 79,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 80,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 81,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 82,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 83,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 84,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 85,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 86,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 87,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 88,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 89,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 90,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 91,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 92,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 93,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 94,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 95,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 96,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 97,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 98,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 99,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 100,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 111,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 112,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 113,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 114,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 115,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 116,
          "witness_key": "ratio:co2-ba"
        },
        {
          "row_index": 117,
          "witness_key": "ratio:co2-rb"
        },
        {
          "row_index": 118,
          "witness_key": "ratio:vp-vs"
        },
        {
          "row_index": 119,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 120,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 121,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 122,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 123,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 124,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 125,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 126,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 127,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 128,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 129,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 130,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 131,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 132,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 133,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 134,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 135,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 136,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 137,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 138,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 139,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 140,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 141,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 142,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 143,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 144,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 145,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 146,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 147,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 148,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 149,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 150,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 151,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 152,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 153,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 154,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 155,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 156,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 157,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 158,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 159,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 160,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 161,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 162,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 163,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 164,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 165,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 166,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 167,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 168,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 169,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 170,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 171,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 172,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 173,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 174,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 175,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 176,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 177,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 178,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 179,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 180,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 181,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 182,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 183,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 184,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 185,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 186,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 187,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 188,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 189,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 190,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 191,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 192,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 193,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 194,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 195,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 196,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 197,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 198,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 199,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 200,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 201,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 202,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 203,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 204,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 205,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 206,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 207,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 208,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 209,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 210,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 211,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 212,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 213,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 214,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 215,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 216,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 217,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 218,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 219,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 220,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 221,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 222,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 223,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 224,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 225,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 226,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 227,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 228,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 229,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 230,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 231,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 232,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 233,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 234,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 235,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 236,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 237,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 238,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 239,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 240,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 241,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 242,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 243,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 244,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 245,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 246,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 247,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 248,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 249,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 250,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 251,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 252,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 253,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 254,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 255,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 256,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 257,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 258,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 259,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 260,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 261,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 262,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 263,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 264,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 265,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 266,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 267,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 268,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 269,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 270,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 271,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 272,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 273,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 274,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 275,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 276,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 277,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-T3-04",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The uncertainty, its unit and its measured status come from one observation row and the set of events from a count row, but that observation carries no subject, so no row binds the uncertainty to a record.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 154,
          "absent_reason": null,
          "note": "The row carries about 2.1 km."
        },
        {
          "semantic": "length_unit",
          "row_index": 154,
          "absent_reason": null,
          "note": "The unit field carries km."
        },
        {
          "semantic": "quantity_subject",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "The observation type carries a subject slot and this record leaves it unset, so no row says what the uncertainty is an uncertainty of beyond the words after relocation in its name."
        },
        {
          "semantic": "derivation_status",
          "row_index": 154,
          "absent_reason": null,
          "note": "The modality field reads measured and the name says the value is the updated one after relocation."
        },
        {
          "semantic": "event_set",
          "row_index": 100,
          "absent_reason": null,
          "note": "The row carries the 276 events well relocated in the final catalogue."
        }
      ],
      "source_locators": [
        "page:7:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "method:cross-correlation"
        },
        {
          "row_index": 1,
          "witness_key": "method:depth-resolution-tests"
        },
        {
          "row_index": 2,
          "witness_key": "method:double-difference"
        },
        {
          "row_index": 3,
          "witness_key": "method:fc-correction"
        },
        {
          "row_index": 4,
          "witness_key": "method:first-motion"
        },
        {
          "row_index": 5,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 6,
          "witness_key": "method:location-criteria"
        },
        {
          "row_index": 7,
          "witness_key": "method:ml-formula"
        },
        {
          "row_index": 8,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 9,
          "witness_key": "method:stalta"
        },
        {
          "row_index": 10,
          "witness_key": "method:station-corrections"
        },
        {
          "row_index": 11,
          "witness_key": "method:swave-delay-removal"
        },
        {
          "row_index": 12,
          "witness_key": "method:wadati"
        },
        {
          "row_index": 13,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 14,
          "witness_key": "sw:global-mapper"
        },
        {
          "row_index": 15,
          "witness_key": "sw:gmt6"
        },
        {
          "row_index": 16,
          "witness_key": "sw:hash"
        },
        {
          "row_index": 17,
          "witness_key": "sw:hypodd"
        },
        {
          "row_index": 18,
          "witness_key": "sw:nonlinloc"
        },
        {
          "row_index": 19,
          "witness_key": "sw:seisan"
        },
        {
          "row_index": 20,
          "witness_key": "sw:velest"
        },
        {
          "row_index": 21,
          "witness_key": "sw:zmap"
        },
        {
          "row_index": 22,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 23,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 24,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 25,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 26,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 27,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 28,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 29,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 30,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 31,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 32,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 33,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 34,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 35,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 36,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 37,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 38,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 39,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 40,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 41,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 42,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 43,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 44,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 45,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 46,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 47,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 48,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 49,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 50,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 51,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 52,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 53,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 54,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 55,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 56,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 57,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 58,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 59,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 60,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 61,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 62,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 63,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 64,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 65,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 66,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 67,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 68,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 69,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 70,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 71,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 72,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 73,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 74,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 75,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 76,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 77,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 78,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 79,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 80,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 81,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 82,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 83,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 84,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 85,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 86,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 87,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 88,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 89,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 90,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 91,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 92,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 93,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 94,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 95,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 96,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 100,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 101,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 102,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 103,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 104,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 105,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 106,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 107,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 108,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 109,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 110,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 111,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 112,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 113,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 114,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 115,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 116,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 117,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 118,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 119,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 120,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 121,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 122,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 123,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 124,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 125,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 126,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 127,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 128,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 129,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 130,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 131,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 132,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 133,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 134,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 135,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 136,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 137,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 138,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 139,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 140,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 141,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 142,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 143,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 144,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 145,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 146,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 147,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 148,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 149,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 150,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 151,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 152,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 153,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 154,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 155,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 156,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 157,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 158,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 159,
          "witness_key": "rel:hash-used-for-focal"
        },
        {
          "row_index": 160,
          "witness_key": "rel:nonlinloc-used-for-location"
        },
        {
          "row_index": 161,
          "witness_key": "rel:seisan-used-for-stalta"
        },
        {
          "row_index": 162,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 163,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 164,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 165,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 166,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 167,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 168,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 169,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 170,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 171,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 172,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 173,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 174,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 175,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 176,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 177,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 178,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 179,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 180,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 181,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 182,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 183,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 184,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 185,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 186,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 187,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 188,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 189,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 190,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 191,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 192,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 193,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 194,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 195,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 196,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 197,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 198,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 199,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 200,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 201,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 202,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 203,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 204,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 205,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 206,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 207,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 208,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 209,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 210,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 211,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 212,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 213,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 214,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 215,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 216,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 217,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 218,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 219,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 220,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 221,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 222,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 223,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 224,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 225,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 226,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 227,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 228,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 229,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 230,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 231,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 232,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 233,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 234,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 235,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 236,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 237,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 238,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 239,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 240,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 241,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 242,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 243,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 244,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 245,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 246,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 247,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 248,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 249,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 250,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 251,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 252,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 253,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 254,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 255,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 256,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 257,
          "witness_key": "obs:thermal-model-temp"
        }
      ]
    },
    {
      "question_id": "CQ-T3-05",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "Pressure, temperature and the modelled determination are carried by two observation rows and the solubility model is a row of its own, but neither observation carries a subject and the melt they are about has no record in the graph.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 107,
          "absent_reason": null,
          "note": "The row carries about 0.7 GPa."
        },
        {
          "semantic": "pressure_unit",
          "row_index": 107,
          "absent_reason": null,
          "note": "The unit field carries GPa."
        },
        {
          "semantic": "temperature_unit",
          "row_index": 108,
          "absent_reason": null,
          "note": "That row carries 1250 with degrees Celsius as its unit."
        },
        {
          "semantic": "quantity_subject",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "Both observations leave the subject slot unset and the melt they describe has no record of its own in the graph."
        },
        {
          "semantic": "model_derived_status",
          "row_index": 107,
          "absent_reason": null,
          "note": "The determination field reads modelled and a numerical model row carries the CO2 solubility model itself."
        }
      ],
      "source_locators": [
        "page:5:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "method:cross-correlation"
        },
        {
          "row_index": 1,
          "witness_key": "method:depth-resolution-tests"
        },
        {
          "row_index": 2,
          "witness_key": "method:double-difference"
        },
        {
          "row_index": 3,
          "witness_key": "method:fc-correction"
        },
        {
          "row_index": 4,
          "witness_key": "method:first-motion"
        },
        {
          "row_index": 5,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 6,
          "witness_key": "method:location-criteria"
        },
        {
          "row_index": 7,
          "witness_key": "method:ml-formula"
        },
        {
          "row_index": 8,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 9,
          "witness_key": "method:stalta"
        },
        {
          "row_index": 10,
          "witness_key": "method:station-corrections"
        },
        {
          "row_index": 11,
          "witness_key": "method:swave-delay-removal"
        },
        {
          "row_index": 12,
          "witness_key": "method:wadati"
        },
        {
          "row_index": 13,
          "witness_key": "model:co2-solubility"
        },
        {
          "row_index": 14,
          "witness_key": "model:iacono-marziano"
        },
        {
          "row_index": 15,
          "witness_key": "model:min-1d"
        },
        {
          "row_index": 16,
          "witness_key": "model:thermal"
        },
        {
          "row_index": 17,
          "witness_key": "model:thermal-simulated"
        },
        {
          "row_index": 18,
          "witness_key": "model:velocity-1d"
        },
        {
          "row_index": 19,
          "witness_key": "model:velocity-model-1"
        },
        {
          "row_index": 20,
          "witness_key": "model:velocity-model-5"
        },
        {
          "row_index": 21,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 22,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 23,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 24,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 25,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 26,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 27,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 28,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 29,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 30,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 31,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 32,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 33,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 34,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 35,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 36,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 37,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 38,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 39,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 40,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 41,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 42,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 43,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 44,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 45,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 46,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 47,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 48,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 49,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 50,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 51,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 52,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 53,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 54,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 55,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 56,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 57,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 58,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 59,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 60,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 61,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 62,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 63,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 64,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 65,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 66,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 67,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 68,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 69,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 70,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 71,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 72,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 73,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 74,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 75,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 76,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 77,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 78,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 79,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 80,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 81,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 82,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 83,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 84,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 85,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 86,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 87,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 88,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 89,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 90,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 91,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 92,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 93,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 94,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 95,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 96,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 100,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 101,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 102,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 103,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 104,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 105,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 106,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 107,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 108,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 109,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 110,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 111,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 112,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 113,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 114,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 115,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 116,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 117,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 118,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 119,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 120,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 121,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 122,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 123,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 124,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 125,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 126,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 127,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 128,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 129,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 130,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 131,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 132,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 133,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 134,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 135,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 136,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 137,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 138,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 139,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 140,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 141,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 142,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 143,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 144,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 145,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 146,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 147,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 148,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 149,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 150,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 151,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 152,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 153,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 154,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 155,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 156,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 157,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 158,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 159,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 160,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 161,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 162,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 163,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 164,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 165,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 166,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 167,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 168,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 169,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 170,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 171,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 172,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 173,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 174,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 175,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 176,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 177,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 178,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 179,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 180,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 181,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 182,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 183,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 184,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 185,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 186,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 187,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 188,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 189,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 190,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 191,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 192,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 193,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 194,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 195,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 196,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 197,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 198,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 199,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 200,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 201,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 202,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 203,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 204,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 205,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 206,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 207,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 208,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 209,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 210,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 211,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 212,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 213,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 214,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 215,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 216,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 217,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 218,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 219,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 220,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 221,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 222,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 223,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 224,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 225,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 226,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 227,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 228,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 229,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 230,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 231,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 232,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 233,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 234,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 235,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 236,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 237,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 238,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 239,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 240,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 241,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 242,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 243,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 244,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 245,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 246,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 247,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 248,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 249,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 250,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 251,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 252,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 253,
          "witness_key": "obs:thermal-model-temp"
        }
      ]
    },
    {
      "question_id": "CQ-T4-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One claim row carries the causal claim, its preferred disposition, its hedged modality and the segment it is about.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "causal_claim",
          "row_index": 104,
          "absent_reason": null,
          "note": "The name field states that the deep mantle earthquakes result from CO2 degassing."
        },
        {
          "semantic": "preferred_disposition",
          "row_index": 104,
          "absent_reason": null,
          "note": "The hypothesis disposition field reads preferred."
        },
        {
          "semantic": "epistemic_modality",
          "row_index": 104,
          "absent_reason": null,
          "note": "The assertion modality field reads hypothesised, matching the word suggest."
        },
        {
          "semantic": "claim_subject",
          "row_index": 104,
          "absent_reason": null,
          "note": "The subject reference resolves to the segment RC2."
        }
      ],
      "source_locators": [
        "page:1:block:001",
        "page:5:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 33,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 34,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 35,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 36,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 37,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 38,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 39,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 40,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 41,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 42,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 43,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 44,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 45,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 46,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 47,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 48,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 49,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 50,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 51,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 52,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 53,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 54,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 55,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 56,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 57,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 58,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 59,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 60,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 61,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 62,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 63,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 64,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 65,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 66,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 67,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 68,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 69,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 70,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 71,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 72,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 73,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 74,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 75,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 76,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 77,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 78,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 79,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 80,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 81,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 83,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 84,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 85,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 86,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 87,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 88,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 89,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 90,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 91,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 92,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 93,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 94,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 95,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 96,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 97,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 98,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 99,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 100,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 101,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 102,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 103,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 104,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 105,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 106,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 107,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 108,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 109,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 110,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 111,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 112,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 113,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 114,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 115,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 116,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 117,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 118,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 119,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 120,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 121,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 122,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 123,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 124,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 125,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 126,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 127,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 128,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 129,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 130,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 131,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 132,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 133,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 134,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 135,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 136,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 137,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 138,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 139,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 140,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 141,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 142,
          "witness_key": "claim:selected-model-more-events"
        }
      ]
    },
    {
      "question_id": "CQ-T4-02",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The candidate mechanism, its refusal and the ground for it are carried by three separate claim rows, but the candidate claim leaves its subject slot unset, so no row binds the declined explanation to the segment it is about.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "candidate_mechanism",
          "row_index": 55,
          "absent_reason": null,
          "note": "The row states the magmatic-tectonic possibility and labels itself a candidate explanation."
        },
        {
          "semantic": "declined_disposition",
          "row_index": 55,
          "absent_reason": null,
          "note": "The hypothesis disposition field reads not supported, drawn from the sentence refusing the melt-movement mechanism."
        },
        {
          "semantic": "stated_ground",
          "row_index": 57,
          "absent_reason": null,
          "note": "The row states that the cited cases are eruption-associated and sit in a thickened crust or a cold lithosphere, unlike a mid-ocean ridge."
        },
        {
          "semantic": "claim_subject",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "The candidate-explanation record carries no subject and no other row binds this declined mechanism to a feature."
        }
      ],
      "source_locators": [
        "page:4:block:002",
        "page:4:block:003",
        "page:5:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 33,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 34,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 35,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 36,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 37,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 38,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 39,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 40,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 41,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 42,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 43,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 44,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 45,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 46,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 47,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 48,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 49,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 50,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 51,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 52,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 53,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 54,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 55,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 56,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 57,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 58,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 59,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 60,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 61,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 62,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 63,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 64,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 65,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 66,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 67,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 68,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 69,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 70,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 71,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 72,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 73,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 74,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 75,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 76,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 77,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 78,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 79,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 80,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 81,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 83,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 84,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 85,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 86,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 87,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 88,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 89,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 90,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 91,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 92,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 93,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 94,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 95,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 96,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 97,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 98,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 99,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 100,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 101,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 102,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 103,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 104,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 105,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 106,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 107,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 108,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 109,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 110,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 111,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 112,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 113,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 114,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 115,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 116,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 117,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 118,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 119,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 120,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 121,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 122,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 123,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 124,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 125,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 126,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 127,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 128,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 129,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 130,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 131,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 132,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 133,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 134,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 135,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 136,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 137,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 138,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 139,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 140,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 141,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 142,
          "witness_key": "claim:selected-model-more-events"
        }
      ]
    },
    {
      "question_id": "CQ-T4-03",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The caveat and the claim it qualifies are both in the result as separate claim rows, but the caveat record carries no subject, so nothing binds it to what it is about.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "qualified_claim",
          "row_index": 64,
          "absent_reason": null,
          "note": "The row states that the CO2 to Rb and CO2 to Ba ratios are a good proxy for CO2 concentration, which is the claim the caveat qualifies; no row states the qualification link."
        },
        {
          "semantic": "stated_assumption",
          "row_index": 74,
          "absent_reason": null,
          "note": "The name field states the assumption that the trace elements reflect the mantle source and are unaffected by secondary processes."
        },
        {
          "semantic": "caveat_disposition",
          "row_index": 74,
          "absent_reason": null,
          "note": "The claim kind field reads stated limitation."
        },
        {
          "semantic": "claim_subject",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "The caveat record leaves the subject slot unset and no other row binds it to a subject."
        }
      ],
      "source_locators": [
        "page:5:block:004",
        "page:8:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "method:cross-correlation"
        },
        {
          "row_index": 1,
          "witness_key": "method:depth-resolution-tests"
        },
        {
          "row_index": 2,
          "witness_key": "method:double-difference"
        },
        {
          "row_index": 3,
          "witness_key": "method:fc-correction"
        },
        {
          "row_index": 4,
          "witness_key": "method:first-motion"
        },
        {
          "row_index": 5,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 6,
          "witness_key": "method:location-criteria"
        },
        {
          "row_index": 7,
          "witness_key": "method:ml-formula"
        },
        {
          "row_index": 8,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 9,
          "witness_key": "method:stalta"
        },
        {
          "row_index": 10,
          "witness_key": "method:station-corrections"
        },
        {
          "row_index": 11,
          "witness_key": "method:swave-delay-removal"
        },
        {
          "row_index": 12,
          "witness_key": "method:wadati"
        },
        {
          "row_index": 13,
          "witness_key": "sample:melt-inclusions"
        },
        {
          "row_index": 14,
          "witness_key": "sample:morb-obs-network"
        },
        {
          "row_index": 15,
          "witness_key": "sample:morb-rc2"
        },
        {
          "row_index": 16,
          "witness_key": "sample:morb-rc3"
        },
        {
          "row_index": 17,
          "witness_key": "sample:popping-rocks"
        },
        {
          "row_index": 18,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 19,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 20,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 21,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 22,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 23,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 24,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 25,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 26,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 27,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 28,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 29,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 30,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 31,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 32,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 33,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 34,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 35,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 36,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 37,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 38,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 39,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 40,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 41,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 42,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 43,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 44,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 45,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 46,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 47,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 48,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 49,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 50,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 51,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 52,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 53,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 54,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 55,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 56,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 57,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 58,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 59,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 60,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 61,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 62,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 63,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 64,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 65,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 66,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 67,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 68,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 69,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 70,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 71,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 72,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 73,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 74,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 75,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 76,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 77,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 78,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 79,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 80,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 81,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 82,
          "witness_key": "ratio:co2-ba"
        },
        {
          "row_index": 83,
          "witness_key": "ratio:co2-rb"
        },
        {
          "row_index": 84,
          "witness_key": "ratio:vp-vs"
        },
        {
          "row_index": 85,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 86,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 87,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 88,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 89,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 90,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 91,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 92,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 93,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 94,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 95,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 96,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 97,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 98,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 99,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 100,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 101,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 102,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 103,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 104,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 105,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 106,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 107,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 108,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 109,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 110,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 111,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 112,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 113,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 114,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 115,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 116,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 117,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 118,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 119,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 120,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 121,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 122,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 123,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 124,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 125,
          "witness_key": "claim:volatiles-reduce-solidus"
        }
      ]
    },
    {
      "question_id": "CQ-T4-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One claim row carries the statement, its negation, the segment it is about and the axis it is scoped to.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "existence_claim",
          "row_index": 197,
          "absent_reason": null,
          "note": "The name field states that no active hydrothermal vents are observed there."
        },
        {
          "semantic": "negated_disposition",
          "row_index": 197,
          "absent_reason": null,
          "note": "The assertion modality field reads negated."
        },
        {
          "semantic": "claim_subject",
          "row_index": 197,
          "absent_reason": null,
          "note": "The subject reference resolves to the segment RC2."
        },
        {
          "semantic": "spatial_scope",
          "row_index": 197,
          "absent_reason": null,
          "note": "The name field scopes the statement to the segment RC2 axis."
        }
      ],
      "source_locators": [
        "page:3:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 33,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 34,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 35,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 36,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 37,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 38,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 39,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 40,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 41,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 42,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 43,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 44,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 45,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 46,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 47,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 48,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 49,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 50,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 51,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 52,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 53,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 54,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 55,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 56,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 57,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 58,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 59,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 60,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 61,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 62,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 63,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 64,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 65,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 66,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 67,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 68,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 69,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 70,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 71,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 72,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 73,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 74,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 75,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 76,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 77,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 78,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 79,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 80,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 81,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 83,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 84,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 85,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 86,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 87,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 88,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 89,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 90,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 91,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 92,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 93,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 94,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 95,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 96,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 100,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 111,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 112,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 113,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 114,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 115,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 116,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 117,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 118,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 119,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 120,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 121,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 122,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 123,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 124,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 125,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 126,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 127,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 128,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 129,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 130,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 131,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 132,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 133,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 134,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 135,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 136,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 137,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 138,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 139,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 140,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 141,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 142,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 143,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 144,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 145,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 146,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 147,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 148,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 149,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 150,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 151,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 152,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 153,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 154,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 155,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 156,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 157,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 158,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 159,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 160,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 161,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 162,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 163,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 164,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 165,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 166,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 167,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 168,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 169,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 170,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 171,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 172,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 173,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 174,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 175,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 176,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 177,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 178,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 179,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 180,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 181,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 182,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 183,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 184,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 185,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 186,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 187,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 188,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 189,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 190,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 191,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 192,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 193,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 194,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 195,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 196,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 197,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 198,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 199,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 200,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 201,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 202,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 203,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 204,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 205,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 206,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 207,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 208,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 209,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 210,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 211,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 212,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 213,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 214,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 215,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 216,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 217,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 218,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 219,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 220,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 221,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 222,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 223,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 224,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 225,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 226,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 227,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 228,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 229,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 230,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 231,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 232,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 233,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 234,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 235,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 236,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 237,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 238,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 239,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 240,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 241,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 242,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 243,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 244,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 245,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 246,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 247,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 248,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 249,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 250,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 251,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 252,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 253,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 254,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 255,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 256,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 257,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 258,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 259,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 260,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 261,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 262,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 263,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 264,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 265,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 266,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 267,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 268,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 269,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-T4-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One claim row carries the hedged statement and its modality and a second carries what is still needed. The two rows are not joined in the result.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "hedged_claim",
          "row_index": 24,
          "absent_reason": null,
          "note": "The name field says the deep earthquakes may be long-period events."
        },
        {
          "semantic": "hypothesised_disposition",
          "row_index": 24,
          "absent_reason": null,
          "note": "The record carries the hedge as an assertion modality of hypothesised rather than as a disposition field."
        },
        {
          "semantic": "epistemic_modality",
          "row_index": 24,
          "absent_reason": null,
          "note": "The same assertion modality field carries the epistemic reading."
        },
        {
          "semantic": "stated_limitation",
          "row_index": 37,
          "absent_reason": null,
          "note": "The row says more earthquakes would be required and labels itself a stated limitation."
        }
      ],
      "source_locators": [
        "page:5:block:008"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 1,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 2,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 3,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 4,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 5,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 6,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 7,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 8,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 9,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 10,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 11,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 12,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 13,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 14,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 15,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 16,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 17,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 18,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 19,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 20,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 21,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 22,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 23,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 24,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 25,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 26,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 27,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 28,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 29,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 30,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 31,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 32,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 33,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 34,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 35,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 36,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 37,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 38,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 39,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 40,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 41,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 42,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 43,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 44,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 45,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 46,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 47,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 48,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 49,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 50,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 51,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 52,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 53,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 54,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 55,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 56,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 57,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 58,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 59,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 60,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 61,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 62,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 63,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 64,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 65,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 66,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 67,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 68,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 69,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 70,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 71,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 72,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 73,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 74,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 75,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 76,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 77,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 78,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 79,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 80,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 81,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 82,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 83,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 84,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 85,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 86,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 87,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 88,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 89,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 90,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 91,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 92,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 93,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 94,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 95,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 96,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 97,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 98,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 99,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 100,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 101,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 102,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 103,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 104,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 105,
          "witness_key": "claim:volatiles-reduce-solidus"
        }
      ]
    },
    {
      "question_id": "CQ-T5-01",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The mechanism claim, the volatile observation and the depth observations are all returned as separate rows, but nothing in the result ties an observation to the claim it supports: the graph holds no evidence record and no relation between an observation and a claim.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "causal_mechanism",
          "row_index": 139,
          "absent_reason": null,
          "note": "The row states the degassing mechanism and marks it preferred."
        },
        {
          "semantic": "supporting_observation",
          "row_index": 207,
          "absent_reason": null,
          "note": "The row carries the deep microseismicity beneath the RC2 axis that the mechanism is offered for."
        },
        {
          "semantic": "geochemical_evidence",
          "row_index": 192,
          "absent_reason": null,
          "note": "The row carries the calculated CO2 content of the RC2 melts."
        },
        {
          "semantic": "seismic_evidence",
          "row_index": 206,
          "absent_reason": null,
          "note": "The row carries the measured 16 to 19 km depths beneath the RC2 axis."
        },
        {
          "semantic": "evidence_relation",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "No evidence record and no relation joining an observation to a claim exists in the graph, although the question's type set admits both."
        }
      ],
      "source_locators": [
        "page:1:block:001",
        "page:2:block:004",
        "page:2:block:006",
        "page:5:block:002",
        "page:5:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 1,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 2,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 3,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 4,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 5,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 6,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 7,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 8,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 9,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 10,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 11,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 12,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 13,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 14,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 15,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 16,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 17,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 18,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 19,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 20,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 21,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 22,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 23,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 24,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 25,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 26,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 27,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 28,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 29,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 30,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 31,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 32,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 33,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 34,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 35,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 36,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 37,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 38,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 39,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 40,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 41,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 42,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 43,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 44,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 45,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 46,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 47,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 48,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 49,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 50,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 51,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 52,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 53,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 54,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 55,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 56,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 57,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 58,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 59,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 60,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 61,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 62,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 63,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 64,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 65,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 66,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 67,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 68,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 69,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 70,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 71,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 72,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 73,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 74,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 75,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 76,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 77,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 79,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 80,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 81,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 82,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 83,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 84,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 85,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 86,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 87,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 88,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 89,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 90,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 91,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 92,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 93,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 94,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 95,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 96,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 97,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 98,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 99,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 100,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 101,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 102,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 103,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 104,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 105,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 106,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 107,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 108,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 109,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 110,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 111,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 112,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 113,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 114,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 115,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 116,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 117,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 118,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 119,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 120,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 121,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 122,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 123,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 124,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 125,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 126,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 127,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 128,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 129,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 130,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 131,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 132,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 133,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 134,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 135,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 136,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 137,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 138,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 139,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 140,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 141,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 142,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 143,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 144,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 145,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 146,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 147,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 148,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 149,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 150,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 151,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 152,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 153,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 154,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 155,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 156,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 157,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 158,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 159,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 160,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 161,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 162,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 163,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 164,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 165,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 166,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 167,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 168,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 169,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 170,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 171,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 172,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 173,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 174,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 175,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 176,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 177,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 178,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 179,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 180,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 181,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 182,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 183,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 184,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 185,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 186,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 187,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 188,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 189,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 190,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 191,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 192,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 193,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 194,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 195,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 196,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 197,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 198,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 199,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 200,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 201,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 202,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 203,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 204,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 205,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 206,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 207,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 208,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 209,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 210,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 211,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 212,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 213,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 214,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 215,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 216,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 217,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 218,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 219,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 220,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 221,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 222,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 223,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 224,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 225,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 226,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 227,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 228,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 229,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 230,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 231,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 232,
          "witness_key": "obs:thermal-model-temp"
        }
      ]
    },
    {
      "question_id": "CQ-T5-02",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "Both segments' calculated contents are returned with their unit and subject, but the comparison itself is only in the sentence the two records bind by locator and digest; no field and no relation row carries it.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "comparison_relation",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "The source sentence sets the RC2 value against RC3; both records hold that sentence as a locator and a digest and neither carries the comparison as a field."
        },
        {
          "semantic": "first_quantity_subject",
          "row_index": 229,
          "absent_reason": null,
          "note": "The subject reference resolves to the segment RC2."
        },
        {
          "semantic": "second_quantity_subject",
          "row_index": 235,
          "absent_reason": null,
          "note": "The subject reference resolves to the segment RC3."
        },
        {
          "semantic": "bounded_quantity",
          "row_index": 229,
          "absent_reason": null,
          "note": "The row carries 0.4 to 3.0 wt% for RC2, against 0.04 to 0.7 wt% on the RC3 row."
        },
        {
          "semantic": "concentration_unit",
          "row_index": 229,
          "absent_reason": null,
          "note": "The unit field carries wt% on both rows."
        }
      ],
      "source_locators": [
        "page:5:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "sample:melt-inclusions"
        },
        {
          "row_index": 33,
          "witness_key": "sample:morb-obs-network"
        },
        {
          "row_index": 34,
          "witness_key": "sample:morb-rc2"
        },
        {
          "row_index": 35,
          "witness_key": "sample:morb-rc3"
        },
        {
          "row_index": 36,
          "witness_key": "sample:popping-rocks"
        },
        {
          "row_index": 37,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 38,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 39,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 40,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 41,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 42,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 43,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 44,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 45,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 46,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 47,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 48,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 49,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 50,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 51,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 52,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 53,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 54,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 55,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 56,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 57,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 58,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 59,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 60,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 61,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 62,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 63,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 64,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 65,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 66,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 67,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 68,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 69,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 70,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 71,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 72,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 73,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 74,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 75,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 76,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 77,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 78,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 79,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 80,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 81,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 82,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 83,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 84,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 85,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 86,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 87,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 88,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 89,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 90,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 91,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 92,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 93,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 94,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 95,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 96,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 97,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 98,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 99,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 100,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 111,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 112,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 113,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 114,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 115,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 116,
          "witness_key": "ratio:co2-ba"
        },
        {
          "row_index": 117,
          "witness_key": "ratio:co2-rb"
        },
        {
          "row_index": 118,
          "witness_key": "ratio:vp-vs"
        },
        {
          "row_index": 119,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 120,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 121,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 122,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 123,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 124,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 125,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 126,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 127,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 128,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 129,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 130,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 131,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 132,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 133,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 134,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 135,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 136,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 137,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 138,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 139,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 140,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 141,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 142,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 143,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 144,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 145,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 146,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 147,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 148,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 149,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 150,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 151,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 152,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 153,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 154,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 155,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 156,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 157,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 158,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 159,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 160,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 161,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 162,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 163,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 164,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 165,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 166,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 167,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 168,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 169,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 170,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 171,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 172,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 173,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 174,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 175,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 176,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 177,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 178,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 179,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 180,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 181,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 182,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 183,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 184,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 185,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 186,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 187,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 188,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 189,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 190,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 191,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 192,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 193,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 194,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 195,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 196,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 197,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 198,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 199,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 200,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 201,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 202,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 203,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 204,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 205,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 206,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 207,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 208,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 209,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 210,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 211,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 212,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 213,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 214,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 215,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 216,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 217,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 218,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 219,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 220,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 221,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 222,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 223,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 224,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 225,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 226,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 227,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 228,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 229,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 230,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 231,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 232,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 233,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 234,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 235,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 236,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 237,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 238,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 239,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 240,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 241,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 242,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 243,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 244,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 245,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 246,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 247,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 248,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 249,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 250,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 251,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 252,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 253,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 254,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 255,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 256,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 257,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 258,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 259,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 260,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 261,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 262,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 263,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 264,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 265,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 266,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 267,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 268,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 269,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 270,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 271,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 272,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 273,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 274,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 275,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 276,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 277,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-T5-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The four subsections, an observed maximum depth, the expected depth for the spreading rate and the claim that the deep events far exceed it are carried by four separate rows that nothing in the result joins.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "subsection_set",
          "row_index": 53,
          "absent_reason": null,
          "note": "The name field names RC1, NTD1, RC2 and NTD2."
        },
        {
          "semantic": "maximum_depth_claim",
          "row_index": 252,
          "absent_reason": null,
          "note": "The row carries the maximum depth of less than 10 km observed beneath NTD2."
        },
        {
          "semantic": "expected_depth_claim",
          "row_index": 151,
          "absent_reason": null,
          "note": "The row carries the less than 10 km expected from microseismicity studies for this spreading rate."
        },
        {
          "semantic": "comparison_relation",
          "row_index": 50,
          "absent_reason": null,
          "note": "The name field says the earthquakes far exceed the suggested maximum depth range."
        }
      ],
      "source_locators": [
        "page:2:block:003",
        "page:2:block:005",
        "page:2:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 33,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 34,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 35,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 36,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 37,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 38,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 39,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 40,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 41,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 42,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 43,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 44,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 45,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 46,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 47,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 48,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 49,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 50,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 51,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 52,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 53,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 54,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 55,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 56,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 57,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 58,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 59,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 60,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 61,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 62,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 63,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 64,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 65,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 66,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 67,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 68,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 69,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 70,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 71,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 72,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 73,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 74,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 75,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 76,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 77,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 78,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 79,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 80,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 81,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 83,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 84,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 85,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 86,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 87,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 88,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 89,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 90,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 91,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 92,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 93,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 94,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 95,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 96,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 100,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 111,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 112,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 113,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 114,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 115,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 116,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 117,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 118,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 119,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 120,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 121,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 122,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 123,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 124,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 125,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 126,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 127,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 128,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 129,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 130,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 131,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 132,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 133,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 134,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 135,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 136,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 137,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 138,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 139,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 140,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 141,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 142,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 143,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 144,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 145,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 146,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 147,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 148,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 149,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 150,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 151,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 152,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 153,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 154,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 155,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 156,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 157,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 158,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 159,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 160,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 161,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 162,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 163,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 164,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 165,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 166,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 167,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 168,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 169,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 170,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 171,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 172,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 173,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 174,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 175,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 176,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 177,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 178,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 179,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 180,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 181,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 182,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 183,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 184,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 185,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 186,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 187,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 188,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 189,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 190,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 191,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 192,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 193,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 194,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 195,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 196,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 197,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 198,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 199,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 200,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 201,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 202,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 203,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 204,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 205,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 206,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 207,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 208,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 209,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 210,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 211,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 212,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 213,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 214,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 215,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 216,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 217,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 218,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 219,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 220,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 221,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 222,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 223,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 224,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 225,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 226,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 227,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 228,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 229,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 230,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 231,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 232,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 233,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 234,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 235,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 236,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 237,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 238,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 239,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 240,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 241,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 242,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 243,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 244,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 245,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 246,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 247,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 248,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 249,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 250,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 251,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 252,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 253,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 254,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 255,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 256,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 257,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 258,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 259,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 260,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 261,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 262,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 263,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 264,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 265,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 266,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 267,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 268,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 269,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 270,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-T5-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One count row carries the number of categories and names them in its scope, a claim row carries which are used for interpretation and a further count row carries the catalogue. Nothing joins them in the result.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "category_set",
          "row_index": 80,
          "absent_reason": null,
          "note": "The count scope names categories A, B, C and D."
        },
        {
          "semantic": "category_count",
          "row_index": 80,
          "absent_reason": null,
          "note": "The count field carries four."
        },
        {
          "semantic": "selection_for_interpretation",
          "row_index": 13,
          "absent_reason": null,
          "note": "The row says categories A and B are of good quality and are used for interpretation."
        },
        {
          "semantic": "earthquake_catalog",
          "row_index": 78,
          "absent_reason": null,
          "note": "The row carries the 514 earthquakes of the final catalogue; the dataset record for the catalogue is outside this question's type set."
        }
      ],
      "source_locators": [
        "page:2:block:003",
        "page:6:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "method:cross-correlation"
        },
        {
          "row_index": 1,
          "witness_key": "method:depth-resolution-tests"
        },
        {
          "row_index": 2,
          "witness_key": "method:double-difference"
        },
        {
          "row_index": 3,
          "witness_key": "method:fc-correction"
        },
        {
          "row_index": 4,
          "witness_key": "method:first-motion"
        },
        {
          "row_index": 5,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 6,
          "witness_key": "method:location-criteria"
        },
        {
          "row_index": 7,
          "witness_key": "method:ml-formula"
        },
        {
          "row_index": 8,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 9,
          "witness_key": "method:stalta"
        },
        {
          "row_index": 10,
          "witness_key": "method:station-corrections"
        },
        {
          "row_index": 11,
          "witness_key": "method:swave-delay-removal"
        },
        {
          "row_index": 12,
          "witness_key": "method:wadati"
        },
        {
          "row_index": 13,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 14,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 15,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 16,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 17,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 18,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 19,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 20,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 21,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 22,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 23,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 24,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 25,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 26,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 27,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 28,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 29,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 30,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 31,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 32,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 33,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 34,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 35,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 36,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 37,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 38,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 39,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 40,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 41,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 42,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 43,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 44,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 45,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 46,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 47,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 48,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 49,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 50,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 51,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 52,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 53,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 54,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 55,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 56,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 57,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 58,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 59,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 60,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 61,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 62,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 63,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 64,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 65,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 66,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 67,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 68,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 69,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 70,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 71,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 72,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 73,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 74,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 75,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 76,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 77,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 79,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 80,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 81,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 82,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 83,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 84,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 85,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 86,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 87,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 88,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 89,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 90,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 91,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 92,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 93,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 94,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 95,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 96,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 97,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 98,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 99,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 100,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 101,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 102,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 103,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 104,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 105,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 106,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 107,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 108,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 109,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 110,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 111,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 112,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 113,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 114,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 115,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 116,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 117,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 118,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 119,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 120,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 121,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 122,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 123,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 124,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 125,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 126,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 127,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 128,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 129,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 130,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 131,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 132,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 133,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 134,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 135,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 136,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 137,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 138,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 139,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 140,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 141,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 142,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 143,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 144,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 145,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 146,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 147,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 148,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 149,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 150,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 151,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 152,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 153,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 154,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 155,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 156,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 157,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 158,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 159,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 160,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 161,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 162,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 163,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 164,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 165,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 166,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 167,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 168,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 169,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 170,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 171,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 172,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 173,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 174,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 175,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 176,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 177,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 178,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 179,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 180,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 181,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 182,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 183,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 184,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 185,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 186,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 187,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 188,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 189,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 190,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 191,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 192,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 193,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 194,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 195,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 196,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 197,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 198,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 199,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 200,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 201,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 202,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 203,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 204,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 205,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 206,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 207,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 208,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 209,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 210,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 211,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 212,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 213,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 214,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 215,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 216,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 217,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 218,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 219,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 220,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 221,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 222,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 223,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 224,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 225,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 226,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 227,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 228,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 229,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 230,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 231,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 232,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 233,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 234,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 235,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 236,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 237,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 238,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 239,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 240,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 241,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 242,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 243,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 244,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 245,
          "witness_key": "obs:thermal-model-temp"
        }
      ]
    },
    {
      "question_id": "CQ-T5-05",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The cold and thick lithosphere explanation, its refusal, the morphological observation and the off-axis seismic observation are all returned, but nothing in the result ties either observation to the explanation it argues against.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "candidate_explanation",
          "row_index": 188,
          "absent_reason": null,
          "note": "The row states the extremely cold and thick lithosphere explanation and labels itself a candidate explanation."
        },
        {
          "semantic": "morphological_observation",
          "row_index": 202,
          "absent_reason": null,
          "note": "The row carries the hummocky volcanic morphology, the volcanic cones and the neo-volcanic ridge that indicate a magmatic origin."
        },
        {
          "semantic": "seismic_observation",
          "row_index": 255,
          "absent_reason": null,
          "note": "The row carries the shallow, under 10 km, brittle-ductile boundary read from the off-axis microseismicity west of the RC2 axis."
        },
        {
          "semantic": "evidence_relation",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "No evidence record and no relation between an observation and a claim exists in the graph."
        },
        {
          "semantic": "declined_disposition",
          "row_index": 188,
          "absent_reason": null,
          "note": "The hypothesis disposition field reads not supported."
        }
      ],
      "source_locators": [
        "page:3:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 33,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 34,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 35,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 36,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 37,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 38,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 39,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 40,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 41,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 42,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 43,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 44,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 45,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 46,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 47,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 48,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 49,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 50,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 51,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 52,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 53,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 54,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 55,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 56,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 57,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 58,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 59,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 60,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 61,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 62,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 63,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 64,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 65,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 66,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 67,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 68,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 69,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 70,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 71,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 72,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 73,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 74,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 75,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 76,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 77,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 78,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 79,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 80,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 81,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 83,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 84,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 85,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 86,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 87,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 88,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 89,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 90,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 91,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 92,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 93,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 94,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 95,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 96,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 97,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 98,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 99,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 100,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 111,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 112,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 113,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 114,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 115,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 116,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 117,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 118,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 119,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 120,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 121,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 122,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 123,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 124,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 125,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 126,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 127,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 128,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 129,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 130,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 131,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 132,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 133,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 134,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 135,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 136,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 137,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 138,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 139,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 140,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 141,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 142,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 143,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 144,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 145,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 146,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 147,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 148,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 149,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 150,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 151,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 152,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 153,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 154,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 155,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 156,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 157,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 158,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 159,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 160,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 161,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 162,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 163,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 164,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 165,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 166,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 167,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 168,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 169,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 170,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 171,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 172,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 173,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 174,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 175,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 176,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 177,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 178,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 179,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 180,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 181,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 182,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 183,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 184,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 185,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 186,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 187,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 188,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 189,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 190,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 191,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 192,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 193,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 194,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 195,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 196,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 197,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 198,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 199,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 200,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 201,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 202,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 203,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 204,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 205,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 206,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 207,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 208,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 209,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 210,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 211,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 212,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 213,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 214,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 215,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 216,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 217,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 218,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 219,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 220,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 221,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 222,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 223,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 224,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 225,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 226,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 227,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 228,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 229,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 230,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 231,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 232,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 233,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 234,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 235,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 236,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 237,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 238,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 239,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 240,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 241,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 242,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 243,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 244,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 245,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 246,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 247,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 248,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 249,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 250,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 251,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 252,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 253,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 254,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 255,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 256,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 257,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 258,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 259,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 260,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 261,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 262,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 263,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 264,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 265,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 266,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 267,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 268,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 269,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 270,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-C-01",
      "question_responsiveness": "NONE",
      "responsiveness_rationale": "No returned row carries a sulfur or chlorine concentration, and no record in the graph carries either analyte. Each required semantic is read as an item of this question's answer, so the sample sets that are returned belong to the CO2 estimation and are not the sample set of a sulfur and chlorine report, which the reading never makes.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading reports no sulfur or chlorine concentration anywhere."
        },
        {
          "semantic": "concentration_unit",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "With no such concentration stated, no unit for one is stated either."
        },
        {
          "semantic": "sample_set",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "Sample-set rows are returned, but they are the sets of the CO2 estimation; the reading names no sample set for a sulfur and chlorine measurement."
        },
        {
          "semantic": "measurement_status",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "No measurement of these analytes is described, so no status for one is stated."
        }
      ],
      "source_locators": [
        "page:5:block:004"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "sample:melt-inclusions"
        },
        {
          "row_index": 1,
          "witness_key": "sample:morb-obs-network"
        },
        {
          "row_index": 2,
          "witness_key": "sample:morb-rc2"
        },
        {
          "row_index": 3,
          "witness_key": "sample:morb-rc3"
        },
        {
          "row_index": 4,
          "witness_key": "sample:popping-rocks"
        },
        {
          "row_index": 5,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 6,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 7,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 8,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 9,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 10,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 11,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 12,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 13,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 14,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 15,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 16,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 17,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 18,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 19,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 20,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 21,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 22,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 23,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 24,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 25,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 26,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 27,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 28,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 29,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 30,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 31,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 32,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 33,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 34,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 35,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 36,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 37,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 38,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 39,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 40,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 41,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 42,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 43,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 44,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 45,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 46,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 47,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 48,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 49,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 50,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 51,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 52,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 53,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 54,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 55,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 56,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 57,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 58,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 59,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 60,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 61,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 62,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 63,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 64,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 65,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 66,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 67,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 68,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 69,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 70,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 71,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 72,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 73,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 74,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 75,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 76,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 77,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 79,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 80,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 81,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 82,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 83,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 84,
          "witness_key": "ratio:co2-ba"
        },
        {
          "row_index": 85,
          "witness_key": "ratio:co2-rb"
        },
        {
          "row_index": 86,
          "witness_key": "ratio:vp-vs"
        },
        {
          "row_index": 87,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 88,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 89,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 90,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 91,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 92,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 93,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 94,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 95,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 96,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 97,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 98,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 99,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 100,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 101,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 102,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 103,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 104,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 105,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 106,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 107,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 108,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 109,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 110,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 111,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 112,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 113,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 114,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 115,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 116,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 117,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 118,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 119,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 120,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 121,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 122,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 123,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 124,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 125,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 126,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 127,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 128,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 129,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 130,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 131,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 132,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 133,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 134,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 135,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 136,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 137,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 138,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 139,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 140,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 141,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 142,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 143,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 144,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 145,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 146,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 147,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 148,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 149,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 150,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 151,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 152,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 153,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 154,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 155,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 156,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 157,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 158,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 159,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 160,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 161,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 162,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 163,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 164,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 165,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 166,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 167,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 168,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 169,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 170,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 171,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 172,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 173,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 174,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 175,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 176,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 177,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 178,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 179,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 180,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 181,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 182,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 183,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 184,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 185,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 186,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 187,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 188,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 189,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 190,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 191,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 192,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 193,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 194,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 195,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 196,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 197,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 198,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 199,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 200,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 201,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 202,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 203,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 204,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 205,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 206,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 207,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 208,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 209,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 210,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 211,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 212,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 213,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 214,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 215,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 216,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 217,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 218,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 219,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 220,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 221,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 222,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 223,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 224,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 225,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 226,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 227,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 228,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 229,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 230,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 231,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 232,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 233,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 234,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 235,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 236,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 237,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 238,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 239,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 240,
          "witness_key": "obs:thermal-model-temp"
        }
      ]
    },
    {
      "question_id": "CQ-C-02",
      "question_responsiveness": "NONE",
      "responsiveness_rationale": "No returned row carries a recurrence interval and no record in the graph carries one. Read as items of this question's answer, the event population is the population whose recurrence interval is reported, and the reading reports none.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "temporal_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading states no recurrence interval for the deep earthquakes."
        },
        {
          "semantic": "time_unit",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "With no interval stated, no unit for one is stated."
        },
        {
          "semantic": "event_population",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "Rows carry the deep earthquakes as a depth observation, but the reading names no population as the subject of a recurrence interval."
        },
        {
          "semantic": "measurement_status",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "No determination of such an interval is described."
        }
      ],
      "source_locators": [
        "page:3:block:004"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 1,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 2,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 3,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 4,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 5,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 6,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 7,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 8,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 9,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 10,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 11,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 12,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 13,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 14,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 15,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 16,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 17,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 18,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 19,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 20,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 21,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 22,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 23,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 24,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 25,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 26,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 27,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 28,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 29,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 30,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 31,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 32,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 33,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 34,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 35,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 36,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 37,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 38,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 39,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 40,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 41,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 42,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 43,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 44,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 45,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 46,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 47,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 48,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 49,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 50,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 51,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 52,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 53,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 54,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 55,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 56,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 57,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 58,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 59,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 60,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 61,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 62,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 63,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 64,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 65,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 66,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 67,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 68,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 69,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 70,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 71,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 72,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 73,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 74,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 75,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 76,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 77,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 79,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 80,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 81,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 82,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 83,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 84,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 85,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 86,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 87,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 88,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 89,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 90,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 91,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 92,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 93,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 94,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 95,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 96,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 97,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 98,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 99,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 100,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 101,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 102,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 103,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 104,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 105,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 106,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 107,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 108,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 109,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 110,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 111,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 112,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 113,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 114,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 115,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 116,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 117,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 118,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 119,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 120,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 121,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 122,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 123,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 124,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 125,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 126,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 127,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 128,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 129,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 130,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 131,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 132,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 133,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 134,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 135,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 136,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 137,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 138,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 139,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 140,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 141,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 142,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 143,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 144,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 145,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 146,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 147,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 148,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 149,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 150,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 151,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 152,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 153,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 154,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 155,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 156,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 157,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 158,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 159,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 160,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 161,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 162,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 163,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 164,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 165,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 166,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 167,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 168,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 169,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 170,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 171,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 172,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 173,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 174,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 175,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 176,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 177,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 178,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 179,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 180,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 181,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 182,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 183,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 184,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 185,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 186,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 187,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 188,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 189,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 190,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 191,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 192,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 193,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 194,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 195,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 196,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 197,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 198,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 199,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 200,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 201,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 202,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 203,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 204,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 205,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 206,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 207,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 208,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 209,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 210,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 211,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 212,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 213,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 214,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 215,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 216,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 217,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 218,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 219,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 220,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 221,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 222,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 223,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 224,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 225,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 226,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 227,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 228,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 229,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 230,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 231,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 232,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 233,
          "witness_key": "obs:thermal-model-temp"
        }
      ]
    },
    {
      "question_id": "CQ-C-03",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "One claim row carries the compilation itself, but the per-site contents it points to are in a figure and a supplementary table that the reading does not contain, so no row carries the site set or either per-site quantity.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "site_set",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The reading names a few sites in passing, in the note on updated data and the note on the Rainbow massif, but never the set of sites compiled for the comparison."
        },
        {
          "semantic": "maximum_depth_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The per-site maximum depths are only in the figure and the supplementary table, neither of which is in the reading."
        },
        {
          "semantic": "spreading_rate_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "The per-site spreading rates are in the same excluded places; the only rate in the reading is the one for the study area."
        },
        {
          "semantic": "compilation_source",
          "row_index": 142,
          "absent_reason": null,
          "note": "The row states that this study compiled the maximum depths and the full spreading rate on each site, which is the compilation the answer would cite."
        }
      ],
      "source_locators": [
        "page:8:block:004"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "work:article"
        },
        {
          "row_index": 33,
          "witness_key": "work:cruise-portal"
        },
        {
          "row_index": 34,
          "witness_key": "work:eq-catalog"
        },
        {
          "row_index": 35,
          "witness_key": "work:petdb"
        },
        {
          "row_index": 36,
          "witness_key": "work:ref-001"
        },
        {
          "row_index": 37,
          "witness_key": "work:ref-002"
        },
        {
          "row_index": 38,
          "witness_key": "work:ref-003"
        },
        {
          "row_index": 39,
          "witness_key": "work:ref-004"
        },
        {
          "row_index": 40,
          "witness_key": "work:ref-005"
        },
        {
          "row_index": 41,
          "witness_key": "work:ref-006"
        },
        {
          "row_index": 42,
          "witness_key": "work:ref-007"
        },
        {
          "row_index": 43,
          "witness_key": "work:ref-008"
        },
        {
          "row_index": 44,
          "witness_key": "work:ref-009"
        },
        {
          "row_index": 45,
          "witness_key": "work:ref-010"
        },
        {
          "row_index": 46,
          "witness_key": "work:ref-011"
        },
        {
          "row_index": 47,
          "witness_key": "work:ref-012"
        },
        {
          "row_index": 48,
          "witness_key": "work:ref-013"
        },
        {
          "row_index": 49,
          "witness_key": "work:ref-014"
        },
        {
          "row_index": 50,
          "witness_key": "work:ref-015"
        },
        {
          "row_index": 51,
          "witness_key": "work:ref-016"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref-017"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref-018"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref-019"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref-020"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref-021"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref-022"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref-023"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref-024"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref-025"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref-026"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref-027"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref-028"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref-029"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref-030"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref-031"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref-032"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref-033"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref-034"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref-035"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref-036"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref-037"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref-038"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref-039"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref-040"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref-041"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref-042"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref-043"
        },
        {
          "row_index": 79,
          "witness_key": "work:ref-044"
        },
        {
          "row_index": 80,
          "witness_key": "work:ref-045"
        },
        {
          "row_index": 81,
          "witness_key": "work:ref-046"
        },
        {
          "row_index": 82,
          "witness_key": "work:ref-047"
        },
        {
          "row_index": 83,
          "witness_key": "work:ref-048"
        },
        {
          "row_index": 84,
          "witness_key": "work:ref-049"
        },
        {
          "row_index": 85,
          "witness_key": "work:ref-050"
        },
        {
          "row_index": 86,
          "witness_key": "work:ref-051"
        },
        {
          "row_index": 87,
          "witness_key": "work:ref-052"
        },
        {
          "row_index": 88,
          "witness_key": "work:ref-053"
        },
        {
          "row_index": 89,
          "witness_key": "work:ref-054"
        },
        {
          "row_index": 90,
          "witness_key": "work:ref-055"
        },
        {
          "row_index": 91,
          "witness_key": "work:ref-056"
        },
        {
          "row_index": 92,
          "witness_key": "work:ref-057"
        },
        {
          "row_index": 93,
          "witness_key": "work:ref-058"
        },
        {
          "row_index": 94,
          "witness_key": "work:ref-059"
        },
        {
          "row_index": 95,
          "witness_key": "work:ref-060"
        },
        {
          "row_index": 96,
          "witness_key": "work:ref-061"
        },
        {
          "row_index": 97,
          "witness_key": "work:ref-062"
        },
        {
          "row_index": 98,
          "witness_key": "work:ref-063"
        },
        {
          "row_index": 99,
          "witness_key": "work:ref-064"
        },
        {
          "row_index": 100,
          "witness_key": "work:ref-065"
        },
        {
          "row_index": 101,
          "witness_key": "work:ref-066"
        },
        {
          "row_index": 102,
          "witness_key": "work:ref-067"
        },
        {
          "row_index": 103,
          "witness_key": "work:ref-068"
        },
        {
          "row_index": 104,
          "witness_key": "work:ref-069"
        },
        {
          "row_index": 105,
          "witness_key": "work:ref-070"
        },
        {
          "row_index": 106,
          "witness_key": "work:ref-071"
        },
        {
          "row_index": 107,
          "witness_key": "work:ref-072"
        },
        {
          "row_index": 108,
          "witness_key": "work:ref-073"
        },
        {
          "row_index": 109,
          "witness_key": "work:ref-074"
        },
        {
          "row_index": 110,
          "witness_key": "work:ref-075"
        },
        {
          "row_index": 111,
          "witness_key": "work:ref-076"
        },
        {
          "row_index": 112,
          "witness_key": "work:ref-077"
        },
        {
          "row_index": 113,
          "witness_key": "work:ref-078"
        },
        {
          "row_index": 114,
          "witness_key": "work:ref-079"
        },
        {
          "row_index": 115,
          "witness_key": "work:zenodo"
        },
        {
          "row_index": 116,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 117,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 118,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 119,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 120,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 121,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 122,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 123,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 124,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 125,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 126,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 127,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 128,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 129,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 130,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 131,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 132,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 133,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 134,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 135,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 136,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 137,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 138,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 139,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 140,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 141,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 142,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 143,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 144,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 145,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 146,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 147,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 148,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 149,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 150,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 151,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 152,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 153,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 154,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 155,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 156,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 157,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 158,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 159,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 160,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 161,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 162,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 163,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 164,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 165,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 166,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 167,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 168,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 169,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 170,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 171,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 172,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 173,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 174,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 175,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 176,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 177,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 178,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 179,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 180,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 181,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 182,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 183,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 184,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 185,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 186,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 187,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 188,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 189,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 190,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 191,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 192,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 193,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 194,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 195,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 196,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 197,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 198,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 199,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 200,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 201,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 202,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 203,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 204,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 205,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 206,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 207,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 208,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 209,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 210,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 211,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 212,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 213,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 214,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 215,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 216,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 217,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 218,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 219,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 220,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 221,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 222,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 223,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 224,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 225,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 226,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 227,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 228,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 229,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 230,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 231,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 232,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 233,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 234,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 235,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 236,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 237,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 238,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 239,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 240,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 241,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 242,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 243,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 244,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 245,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 246,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 247,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 248,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 249,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 250,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 251,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 252,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 253,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 254,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 255,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 256,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 257,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 258,
          "witness_key": "rel:catalog-in-zenodo"
        },
        {
          "row_index": 259,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 260,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 261,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 262,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 263,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 264,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 265,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 266,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 267,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 268,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 269,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 270,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 271,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 272,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 273,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 274,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 275,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 276,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 277,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 278,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 279,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 280,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 281,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 282,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 283,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 284,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 285,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 286,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 287,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 288,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 289,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 290,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 291,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 292,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 293,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 294,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 295,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 296,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 297,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 298,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 299,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 300,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 301,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 302,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 303,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 304,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 305,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 306,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 307,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 308,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 309,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 310,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 311,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 312,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 313,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 314,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 315,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 316,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 317,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 318,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 319,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 320,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 321,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 322,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 323,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 324,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 325,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 326,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 327,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 328,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 329,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 330,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 331,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 332,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 333,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 334,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 335,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 336,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 337,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 338,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 339,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 340,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 341,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 342,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 343,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 344,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 345,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 346,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 347,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 348,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 349,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 350,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 351,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 352,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 353,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 354,
          "witness_key": "cnt:useful-obs"
        }
      ]
    },
    {
      "question_id": "CQ-C-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The same three rows answer this as answer the question it paraphrases: the count of instruments, the network they belong to and the experiment they were deployed for, none of them joined to another in the result.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "instrument_count",
          "row_index": 76,
          "absent_reason": null,
          "note": "The count field carries nineteen."
        },
        {
          "semantic": "observing_system",
          "row_index": 1,
          "absent_reason": null,
          "note": "The instrument row names the ocean-bottom seismometers."
        },
        {
          "semantic": "deployment_event",
          "row_index": 0,
          "absent_reason": null,
          "note": "The cruise row is the experiment the deployment sentence derives; its fields name the campaign and describe the experiment rather than the act of placing the instruments."
        }
      ],
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "cruise:smarties"
        },
        {
          "row_index": 1,
          "witness_key": "instr:obs"
        },
        {
          "row_index": 2,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 3,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 4,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 5,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 6,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 7,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 8,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 9,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 10,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 11,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 12,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 13,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 14,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 15,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 16,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 17,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 18,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 19,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 20,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 21,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 22,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 23,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 24,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 25,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 26,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 27,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 28,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 29,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 30,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 31,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 32,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 33,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 34,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 35,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 36,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 37,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 38,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 39,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 40,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 41,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 42,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 43,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 44,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 45,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 46,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 47,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 48,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 49,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 50,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 51,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 52,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 53,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 54,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 55,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 56,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 57,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 58,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 59,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 60,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 61,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 62,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 63,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 64,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 65,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 66,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 67,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 68,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 69,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 70,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 71,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 72,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 73,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 74,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 75,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 76,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 77,
          "witness_key": "cnt:useful-obs"
        },
        {
          "row_index": 78,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 79,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 80,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 81,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 82,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 83,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 84,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 85,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 86,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 87,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 88,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 89,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 90,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 91,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 92,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 93,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 94,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 95,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 96,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 97,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 98,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 99,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 100,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 101,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 102,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 103,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 104,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 105,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 106,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 107,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 108,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 109,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 110,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 111,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 112,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 113,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 114,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 115,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 116,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 117,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 118,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 119,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 120,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 121,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 122,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 123,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 124,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 125,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 126,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 127,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 128,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 129,
          "witness_key": "obs:thermal-model-temp"
        }
      ]
    },
    {
      "question_id": "CQ-C-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One geochemical row carries the range, the unit, the segment and the calculated determination, the same row that answers the question this paraphrases.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 229,
          "absent_reason": null,
          "note": "The row carries 0.4 to 3.0 wt%."
        },
        {
          "semantic": "concentration_unit",
          "row_index": 229,
          "absent_reason": null,
          "note": "The unit field carries wt%."
        },
        {
          "semantic": "quantity_subject",
          "row_index": 229,
          "absent_reason": null,
          "note": "The subject reference resolves to the segment RC2."
        },
        {
          "semantic": "calculated_or_measured_status",
          "row_index": 229,
          "absent_reason": null,
          "note": "The quantity kind is written as CO2 calculated and the determination is derived."
        }
      ],
      "source_locators": [
        "page:5:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "geo:askja"
        },
        {
          "row_index": 1,
          "witness_key": "geo:bdb"
        },
        {
          "row_index": 2,
          "witness_key": "geo:chain-tf"
        },
        {
          "row_index": 3,
          "witness_key": "geo:detachment-east"
        },
        {
          "row_index": 4,
          "witness_key": "geo:equatorial-atlantic"
        },
        {
          "row_index": 5,
          "witness_key": "geo:extinct-vent-field"
        },
        {
          "row_index": 6,
          "witness_key": "geo:fagradalsfjall"
        },
        {
          "row_index": 7,
          "witness_key": "geo:gakkel"
        },
        {
          "row_index": 8,
          "witness_key": "geo:iceland"
        },
        {
          "row_index": 9,
          "witness_key": "geo:inactive-mound"
        },
        {
          "row_index": 10,
          "witness_key": "geo:juan-de-fuca"
        },
        {
          "row_index": 11,
          "witness_key": "geo:knipovich"
        },
        {
          "row_index": 12,
          "witness_key": "geo:lab"
        },
        {
          "row_index": 13,
          "witness_key": "geo:logachev"
        },
        {
          "row_index": 14,
          "witness_key": "geo:mar"
        },
        {
          "row_index": 15,
          "witness_key": "geo:mayotte"
        },
        {
          "row_index": 16,
          "witness_key": "geo:moho"
        },
        {
          "row_index": 17,
          "witness_key": "geo:neovolcanic-ridge"
        },
        {
          "row_index": 18,
          "witness_key": "geo:ntd1"
        },
        {
          "row_index": 19,
          "witness_key": "geo:ntd1-faults"
        },
        {
          "row_index": 20,
          "witness_key": "geo:ntd2"
        },
        {
          "row_index": 21,
          "witness_key": "geo:ntd2-faults"
        },
        {
          "row_index": 22,
          "witness_key": "geo:occ"
        },
        {
          "row_index": 23,
          "witness_key": "geo:occ-normal-faults"
        },
        {
          "row_index": 24,
          "witness_key": "geo:rainbow"
        },
        {
          "row_index": 25,
          "witness_key": "geo:rc1"
        },
        {
          "row_index": 26,
          "witness_key": "geo:rc2"
        },
        {
          "row_index": 27,
          "witness_key": "geo:rc2-bounding-faults"
        },
        {
          "row_index": 28,
          "witness_key": "geo:rc3"
        },
        {
          "row_index": 29,
          "witness_key": "geo:romanche-tf"
        },
        {
          "row_index": 30,
          "witness_key": "geo:rti"
        },
        {
          "row_index": 31,
          "witness_key": "geo:swir"
        },
        {
          "row_index": 32,
          "witness_key": "sample:melt-inclusions"
        },
        {
          "row_index": 33,
          "witness_key": "sample:morb-obs-network"
        },
        {
          "row_index": 34,
          "witness_key": "sample:morb-rc2"
        },
        {
          "row_index": 35,
          "witness_key": "sample:morb-rc3"
        },
        {
          "row_index": 36,
          "witness_key": "sample:popping-rocks"
        },
        {
          "row_index": 37,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 38,
          "witness_key": "claim:acknowledgement-crew"
        },
        {
          "row_index": 39,
          "witness_key": "claim:acknowledgement-discussions"
        },
        {
          "row_index": 40,
          "witness_key": "claim:all-authors-discussed"
        },
        {
          "row_index": 41,
          "witness_key": "claim:axial-valley-floor-basaltic"
        },
        {
          "row_index": 42,
          "witness_key": "claim:both-perturbations-deep"
        },
        {
          "row_index": 43,
          "witness_key": "claim:brittle-10km-at-ntds"
        },
        {
          "row_index": 44,
          "witness_key": "claim:category-definitions"
        },
        {
          "row_index": 45,
          "witness_key": "claim:co2-behaves-incompatible"
        },
        {
          "row_index": 46,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 47,
          "witness_key": "claim:compilation-covariates"
        },
        {
          "row_index": 48,
          "witness_key": "claim:correlations-used-globally"
        },
        {
          "row_index": 49,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 50,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 51,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 52,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 53,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 54,
          "witness_key": "claim:eq-in-mantle-below-10km"
        },
        {
          "row_index": 55,
          "witness_key": "claim:fig3-panel-content"
        },
        {
          "row_index": 56,
          "witness_key": "claim:fixed-depth-rms-worse"
        },
        {
          "row_index": 57,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 58,
          "witness_key": "claim:h3-mylonite"
        },
        {
          "row_index": 59,
          "witness_key": "claim:h4-magmatic-tectonic"
        },
        {
          "row_index": 60,
          "witness_key": "claim:long-period-events"
        },
        {
          "row_index": 61,
          "witness_key": "claim:magmatic-tectonic-contexts-differ"
        },
        {
          "row_index": 62,
          "witness_key": "claim:manual-check"
        },
        {
          "row_index": 63,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 64,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 65,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 66,
          "witness_key": "claim:max-depths-affected"
        },
        {
          "row_index": 67,
          "witness_key": "claim:mechanism-similar-volcanoes"
        },
        {
          "row_index": 68,
          "witness_key": "claim:melt-focused-narrow-zone"
        },
        {
          "row_index": 69,
          "witness_key": "claim:melt-migration-not-understood"
        },
        {
          "row_index": 70,
          "witness_key": "claim:melt-movement-not-applicable"
        },
        {
          "row_index": 71,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 72,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 73,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 74,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 75,
          "witness_key": "claim:no-current-eruption"
        },
        {
          "row_index": 76,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 77,
          "witness_key": "claim:occ-exhumed-mantle"
        },
        {
          "row_index": 78,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 79,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 80,
          "witness_key": "claim:preexisting-faults-favor-migration"
        },
        {
          "row_index": 81,
          "witness_key": "claim:primary-vs-preeruptive"
        },
        {
          "row_index": 82,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 83,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 84,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 85,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 86,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 87,
          "witness_key": "claim:shear-zone-with-detachment"
        },
        {
          "row_index": 88,
          "witness_key": "claim:shiptime-funded"
        },
        {
          "row_index": 89,
          "witness_key": "claim:station-corrections-iterated"
        },
        {
          "row_index": 90,
          "witness_key": "claim:swave-delays-removed"
        },
        {
          "row_index": 91,
          "witness_key": "claim:tests-support-deep"
        },
        {
          "row_index": 92,
          "witness_key": "claim:tf-deep-eq-mylonite"
        },
        {
          "row_index": 93,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 94,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 95,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 96,
          "witness_key": "claim:velocity-model-matters"
        },
        {
          "row_index": 97,
          "witness_key": "claim:volatile-controls-magma"
        },
        {
          "row_index": 98,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 99,
          "witness_key": "claim:volatiles-extend-melting-depth"
        },
        {
          "row_index": 100,
          "witness_key": "claim:vpvs-reasonable"
        },
        {
          "row_index": 101,
          "witness_key": "cnt:catalog-links"
        },
        {
          "row_index": 102,
          "witness_key": "cnt:final-located"
        },
        {
          "row_index": 103,
          "witness_key": "cnt:identified-earthquakes"
        },
        {
          "row_index": 104,
          "witness_key": "cnt:location-categories"
        },
        {
          "row_index": 105,
          "witness_key": "cnt:magnitude-groups"
        },
        {
          "row_index": 106,
          "witness_key": "cnt:new-focal-mechanisms"
        },
        {
          "row_index": 107,
          "witness_key": "cnt:ntds"
        },
        {
          "row_index": 108,
          "witness_key": "cnt:relocated-events"
        },
        {
          "row_index": 109,
          "witness_key": "cnt:relocation-iterations"
        },
        {
          "row_index": 110,
          "witness_key": "cnt:subsections"
        },
        {
          "row_index": 111,
          "witness_key": "cnt:total-focal-mechanisms"
        },
        {
          "row_index": 112,
          "witness_key": "cnt:velest-iterations"
        },
        {
          "row_index": 113,
          "witness_key": "cnt:velest-subdataset"
        },
        {
          "row_index": 114,
          "witness_key": "cnt:velocity-models"
        },
        {
          "row_index": 115,
          "witness_key": "cnt:well-relocated"
        },
        {
          "row_index": 116,
          "witness_key": "ratio:co2-ba"
        },
        {
          "row_index": 117,
          "witness_key": "ratio:co2-rb"
        },
        {
          "row_index": 118,
          "witness_key": "ratio:vp-vs"
        },
        {
          "row_index": 119,
          "witness_key": "gchem:abstract-co2-primary"
        },
        {
          "row_index": 120,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 121,
          "witness_key": "obs:axial-event-depth-stability"
        },
        {
          "row_index": 122,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 123,
          "witness_key": "obs:brittle-thickness"
        },
        {
          "row_index": 124,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 125,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 126,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 127,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 128,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 129,
          "witness_key": "obs:criterion-azimuthal-gap"
        },
        {
          "row_index": 130,
          "witness_key": "obs:criterion-swave-distance"
        },
        {
          "row_index": 131,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 132,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 133,
          "witness_key": "obs:degassing-eq-depth-range"
        },
        {
          "row_index": 134,
          "witness_key": "obs:depth-uncertainty-bound"
        },
        {
          "row_index": 135,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 136,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 137,
          "witness_key": "obs:expected-max-depth-slow"
        },
        {
          "row_index": 138,
          "witness_key": "obs:expected-max-depth-ultraslow"
        },
        {
          "row_index": 139,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 140,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 141,
          "witness_key": "obs:focal-selection-criteria"
        },
        {
          "row_index": 142,
          "witness_key": "obs:fraction-two-criteria"
        },
        {
          "row_index": 143,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 144,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 145,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 146,
          "witness_key": "obs:horizontal-uncertainty-bound"
        },
        {
          "row_index": 147,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 148,
          "witness_key": "obs:lithosphere-age-45ma"
        },
        {
          "row_index": 149,
          "witness_key": "obs:lithospheric-age-contours"
        },
        {
          "row_index": 150,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 151,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 152,
          "witness_key": "obs:mean-horizontal-uncertainty"
        },
        {
          "row_index": 153,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 154,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 155,
          "witness_key": "obs:model1-vp"
        },
        {
          "row_index": 156,
          "witness_key": "obs:offaxis-cluster-depth"
        },
        {
          "row_index": 157,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 158,
          "witness_key": "obs:predicted-max-depth"
        },
        {
          "row_index": 159,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 160,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 161,
          "witness_key": "obs:quality-abc-uncertainty"
        },
        {
          "row_index": 162,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 163,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 164,
          "witness_key": "obs:relocation-obs-threshold"
        },
        {
          "row_index": 165,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 166,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 167,
          "witness_key": "obs:rms-residual-bound"
        },
        {
          "row_index": 168,
          "witness_key": "obs:solubility-calc-temperature"
        },
        {
          "row_index": 169,
          "witness_key": "obs:station-gap-bound"
        },
        {
          "row_index": 170,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 171,
          "witness_key": "obs:triggering-pore-pressure"
        },
        {
          "row_index": 172,
          "witness_key": "obs:updated-horizontal-uncertainty"
        },
        {
          "row_index": 173,
          "witness_key": "obs:velocity-constraint-depth"
        },
        {
          "row_index": 174,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 175,
          "witness_key": "obs:vpvs-test-range"
        },
        {
          "row_index": 176,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 177,
          "witness_key": "rel:mar-in-atlantic"
        },
        {
          "row_index": 178,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 179,
          "witness_key": "rel:rc2-adjacent-ntd1"
        },
        {
          "row_index": 180,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 181,
          "witness_key": "rel:rc3-adjacent-ntd2"
        },
        {
          "row_index": 182,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 183,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 184,
          "witness_key": "claim:co2-degassing-deep-eq"
        },
        {
          "row_index": 185,
          "witness_key": "claim:co2-influences-lab-melt"
        },
        {
          "row_index": 186,
          "witness_key": "claim:deep-eq-aligned"
        },
        {
          "row_index": 187,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 188,
          "witness_key": "claim:depths-not-artifact"
        },
        {
          "row_index": 189,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 190,
          "witness_key": "claim:enriched-basalts-low-melting"
        },
        {
          "row_index": 191,
          "witness_key": "claim:extinct-vent-too-far"
        },
        {
          "row_index": 192,
          "witness_key": "claim:fig3-panels"
        },
        {
          "row_index": 193,
          "witness_key": "claim:fig6-panels"
        },
        {
          "row_index": 194,
          "witness_key": "claim:five-models-enumerated"
        },
        {
          "row_index": 195,
          "witness_key": "claim:h1-cold-lithosphere"
        },
        {
          "row_index": 196,
          "witness_key": "claim:h2-hydrothermal-cooling"
        },
        {
          "row_index": 197,
          "witness_key": "claim:higher-temp-hinders-nucleation"
        },
        {
          "row_index": 198,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 199,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 200,
          "witness_key": "claim:magmatism-dominates-rc2"
        },
        {
          "row_index": 201,
          "witness_key": "claim:mantle-hot"
        },
        {
          "row_index": 202,
          "witness_key": "claim:max-depth-not-following-relationship"
        },
        {
          "row_index": 203,
          "witness_key": "claim:melt-lens-defines-bdb"
        },
        {
          "row_index": 204,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 205,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 206,
          "witness_key": "claim:ntd2-bdb-normal"
        },
        {
          "row_index": 207,
          "witness_key": "claim:occ-recent-deformation"
        },
        {
          "row_index": 208,
          "witness_key": "claim:occ-shallow-ruptures"
        },
        {
          "row_index": 209,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 210,
          "witness_key": "claim:rc2-no-detachment"
        },
        {
          "row_index": 211,
          "witness_key": "claim:rc2-rc3-analysed"
        },
        {
          "row_index": 212,
          "witness_key": "claim:rc2-robust"
        },
        {
          "row_index": 213,
          "witness_key": "claim:rti-amagmatic"
        },
        {
          "row_index": 214,
          "witness_key": "claim:small-pressure-increase-induces"
        },
        {
          "row_index": 215,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 216,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 217,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 218,
          "witness_key": "cnt:events-mar"
        },
        {
          "row_index": 219,
          "witness_key": "cnt:events-romanche"
        },
        {
          "row_index": 220,
          "witness_key": "cnt:forced-depth-subset"
        },
        {
          "row_index": 221,
          "witness_key": "cnt:located-earthquakes"
        },
        {
          "row_index": 222,
          "witness_key": "gchem:eq-atlantic-co2-avg"
        },
        {
          "row_index": 223,
          "witness_key": "gchem:eq-atlantic-co2-max"
        },
        {
          "row_index": 224,
          "witness_key": "gchem:rc2-ba"
        },
        {
          "row_index": 225,
          "witness_key": "gchem:rc2-co2-ba"
        },
        {
          "row_index": 226,
          "witness_key": "gchem:rc2-co2-ba90"
        },
        {
          "row_index": 227,
          "witness_key": "gchem:rc2-co2-minimum"
        },
        {
          "row_index": 228,
          "witness_key": "gchem:rc2-co2-preeruptive"
        },
        {
          "row_index": 229,
          "witness_key": "gchem:rc2-co2-primary-calc"
        },
        {
          "row_index": 230,
          "witness_key": "gchem:rc2-co2-rb"
        },
        {
          "row_index": 231,
          "witness_key": "gchem:rc2-co2-rb90"
        },
        {
          "row_index": 232,
          "witness_key": "gchem:rc2-rb"
        },
        {
          "row_index": 233,
          "witness_key": "gchem:rc3-co2-ba"
        },
        {
          "row_index": 234,
          "witness_key": "gchem:rc3-co2-ba90"
        },
        {
          "row_index": 235,
          "witness_key": "gchem:rc3-co2-primary-calc"
        },
        {
          "row_index": 236,
          "witness_key": "gchem:rc3-co2-rb"
        },
        {
          "row_index": 237,
          "witness_key": "gchem:rc3-co2-rb90"
        },
        {
          "row_index": 238,
          "witness_key": "gchem:swir-co2-highest"
        },
        {
          "row_index": 239,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 240,
          "witness_key": "obs:bdb-isotherm"
        },
        {
          "row_index": 241,
          "witness_key": "obs:coverage-mar"
        },
        {
          "row_index": 242,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 243,
          "witness_key": "obs:deep-eq-rc2"
        },
        {
          "row_index": 244,
          "witness_key": "obs:deep-micro-rc2"
        },
        {
          "row_index": 245,
          "witness_key": "obs:forced-depths"
        },
        {
          "row_index": 246,
          "witness_key": "obs:h1-bdb-depth"
        },
        {
          "row_index": 247,
          "witness_key": "obs:h1-isotherms"
        },
        {
          "row_index": 248,
          "witness_key": "obs:iceland-magmatic-depths"
        },
        {
          "row_index": 249,
          "witness_key": "obs:interpreted-deep-eq-depth"
        },
        {
          "row_index": 250,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 251,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 252,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 253,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 254,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 255,
          "witness_key": "obs:no-eq-below-20km"
        },
        {
          "row_index": 256,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 257,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 258,
          "witness_key": "obs:ntd2-depth-10"
        },
        {
          "row_index": 259,
          "witness_key": "obs:ntd2-depth-range"
        },
        {
          "row_index": 260,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 261,
          "witness_key": "obs:occ-depth-range"
        },
        {
          "row_index": 262,
          "witness_key": "obs:offaxis-bdb-depth"
        },
        {
          "row_index": 263,
          "witness_key": "obs:offaxis-crustal-age"
        },
        {
          "row_index": 264,
          "witness_key": "obs:rc2-crust-thickness"
        },
        {
          "row_index": 265,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 266,
          "witness_key": "obs:rc2-valley-width"
        },
        {
          "row_index": 267,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 268,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 269,
          "witness_key": "obs:thermal-model-temp"
        },
        {
          "row_index": 270,
          "witness_key": "claim:focal-not-robust"
        },
        {
          "row_index": 271,
          "witness_key": "claim:model5-selected"
        },
        {
          "row_index": 272,
          "witness_key": "claim:one-obs-no-data"
        },
        {
          "row_index": 273,
          "witness_key": "claim:refraction-profile-used"
        },
        {
          "row_index": 274,
          "witness_key": "claim:selected-model-more-events"
        },
        {
          "row_index": 275,
          "witness_key": "cnt:min-obs-per-event"
        },
        {
          "row_index": 276,
          "witness_key": "cnt:obs-deployed"
        },
        {
          "row_index": 277,
          "witness_key": "cnt:useful-obs"
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

Each `witnesses` entry has this shape on a `STRUCTURED_ROWS` cell:

```
{
  "witness_key": "invoice:I1",
  "source_support": "SUPPORTED | PARTIAL | UNSUPPORTED | NOT_EVALUABLE",
  "resolution": "VALUE_MATCHES_ROW | VALUE_DERIVED_FROM_ROW | VALUE_DIFFERS_FROM_ROW | LOCATOR_NOT_RESOLVABLE",
  "source_locators": ["source:small-shop:invoices#row:0:invoice_id"],
  "rationale": "one or two sentences in your own words"
}
```

and this shape on a `SELECTED_READING_TEXT_LAYER` cell, with no `resolution`
key and the fixed tokens the task defines at the head of the `rationale`:

```
{
  "witness_key": "obs:instrument-count",
  "source_support": "SUPPORTED | PARTIAL | UNSUPPORTED | NOT_EVALUABLE",
  "source_locators": ["page:2:block:004"],
  "rationale": "DIGEST_OK SUBJECT_IN_BLOCK one or two sentences in your own words"
}
```

Each `rows` entry names a returned row and the witness it shares:

```
{
  "row_index": 0,
  "witness_key": "invoice:I1"
}
```

Each `coverage` entry names one required semantic and either the row that
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
  "absent_reason": "NOT_MODELLED | WITHHELD_STATEMENT | UNREACHED_RECORD | NOT_IN_SOURCE | LOCATOR_NOT_RESOLVABLE",
  "note": "why, in your own words"
}
```
