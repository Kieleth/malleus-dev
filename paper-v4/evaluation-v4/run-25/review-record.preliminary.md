# Malleus paper v4 source-grounded review record, protocol v3

This is run-25's blank record, written by
`paper-v4/evaluation-v4/run-25/build_review_inputs.py` from the frozen v3
template. The question ids are this cell's frozen competency question file's,
in that file's order. The row and witness counts are figures of a producer
that has not run and are filled by the same script at freeze; no other
placeholder survives either stage.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

The `questions` block below carries one entry per question of the cell's
competency question file, 30 of them, in that file's order. Write one
`witnesses` entry per distinct witness the query result returns,
505 in all, and reference it from every row that shares it.
Rows: 153 rows for `CQ-T1-01`, 153 for `CQ-T1-02`, 207 for `CQ-T1-03`, 205 for
`CQ-T1-04`, 153 for `CQ-T1-05`, 179 for `CQ-T2-01`, 385 for `CQ-T2-02`, 329
for `CQ-T2-03`, 416 for `CQ-T2-04`, 37 for `CQ-T2-05`, 330 for `CQ-T3-01`,
335 for `CQ-T3-02`, 335 for `CQ-T3-03`, 299 for `CQ-T3-04`, 291 for
`CQ-T3-05`, 180 for `CQ-T4-01`, 180 for `CQ-T4-02`, 137 for `CQ-T4-03`, 329
for `CQ-T4-04`, 119 for `CQ-T4-05`, 268 for `CQ-T5-01`, 335 for `CQ-T5-02`,
330 for `CQ-T5-03`, 281 for `CQ-T5-04`, 330 for `CQ-T5-05`, 274 for
`CQ-C-01`, 269 for `CQ-C-02`, 416 for `CQ-C-03`, 153 for `CQ-C-04`, 335 for
`CQ-C-05`,
7743 in all.

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
    "review_input_manifest_sha256": "sha256:af9df250ec191266e15840b703ad7e79121d00a3903447fb2c9a3bc4301b7b5c"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-preliminary-run-25",
    "completed_at": "2026-09-12T03:23:31Z"
  },
  "witnesses": [
    {
      "witness_key": "sample:basalt",
      "source_support": "PARTIAL",
      "rationale": "NO_SUBJECT_IN_ROW the cited block carries only the map legend word for this sample material, which names the set and its material, but the projected description of samples plotted as coloured hexagons on the bathymetric map is not stated there",
      "source_locators": [
        "page:3:block:003"
      ]
    },
    {
      "witness_key": "sample:morb-obs-network",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited block states the compilation of all published geochemical analyses of MORB samples within the bounds of the OBS network, which is the name, the material and the description the row projects",
      "source_locators": [
        "page:5:block:004",
        "page:8:block:005",
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "sample:morb-rc2",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited figure-caption block names the MORB samples along segments RC2 and RC3, matching the projected name and material",
      "source_locators": [
        "page:6:block:005"
      ]
    },
    {
      "witness_key": "sample:peridotite",
      "source_support": "PARTIAL",
      "rationale": "NO_SUBJECT_IN_ROW the cited block carries only the legend word for this material, so the name and material are supported while the projected description of coloured hexagons on the bathymetric map is not stated in that block",
      "source_locators": [
        "page:3:block:003"
      ]
    },
    {
      "witness_key": "claim:ab-good-quality",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states that categories A and B are of good quality and are used for interpretation, which is what the projected claim kind says",
      "source_locators": [
        "page:2:block:003"
      ]
    },
    {
      "witness_key": "claim:aml-defines-bdb",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states that axial melt lenses are used to define the brittle-ductile boundary at fast- and intermediate-spreading ridges",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "claim:amplitude-measurement",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the maximum amplitude is measured on a simulated Wood-Anderson seismogram using the named package",
      "source_locators": [
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "claim:arrivals-checked-manually",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the manual check, and the automatic detection it qualifies is stated two sentences earlier in the same block",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "claim:axial-valley-floor",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence describes the axial valley floor and its basaltic constructions as the projected claim kind says",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "claim:axis-relocating",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence suggests the axis is being relocated east beneath the OCC faulted dome, and the hypothesised modality matches the suggesting verb",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "claim:bdb-shallower-southward",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the expectation that the boundary shallows southward with distance from the RTI",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "claim:brittle-ductile-patches",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited block states that the brown and gray patches are the brittle and ductile lithospheres, and it continues the figure caption opened at the end of the preceding block",
      "source_locators": [
        "page:7:block:011"
      ]
    },
    {
      "witness_key": "claim:category-criteria",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence maps categories A, B-C and D onto the number of criteria met",
      "source_locators": [
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "claim:co2-from-rb90-ba90",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the calculation of CO2 in melts in equilibrium with the mantle source from both proxies, and the calculated modality matches",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "claim:co2-like-incompatible",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the similarity of CO2 behaviour to highly incompatible trace elements",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "claim:co2-solubility-pressure",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the pressure dependence of solubility and the saturation and gas nucleation that follow",
      "source_locators": [
        "page:5:block:003"
      ]
    },
    {
      "witness_key": "claim:cold-thick-lithosphere",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the first derivation carries the cold and thick lithosphere explanation and the second carries the however sentence that withholds support, which is the projected disposition",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "claim:contexts-differ",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states that the Iceland and Mayotte settings differ from a mid-ocean ridge",
      "source_locators": [
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "claim:copyright",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited block is the copyright line itself",
      "source_locators": [
        "page:11:block:006"
      ]
    },
    {
      "witness_key": "claim:correspondence",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence names the two addressees for correspondence and requests for materials",
      "source_locators": [
        "page:11:block:002"
      ]
    },
    {
      "witness_key": "claim:criteria-followed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states that well-established criteria were followed to assess location reliability",
      "source_locators": [
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "claim:crust-from-mantle-melt",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states that oceanic crust forms from mantle-derived melt at spreading centers",
      "source_locators": [
        "page:1:block:002"
      ]
    },
    {
      "witness_key": "claim:deep-eq-alignment",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the alignment of the deep earthquakes beneath the RC2 axis and its parallelism with the main axial normal faults",
      "source_locators": [
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "claim:deep-long-period",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence says the mechanism may result in deep long-period volcanic earthquakes, and the hypothesised modality matches the may",
      "source_locators": [
        "page:5:block:008"
      ]
    },
    {
      "witness_key": "claim:deeper-eq-observed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence reports the earlier observations of deeper earthquakes and the two associations the claim kind names",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "claim:deepest-documented",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence ranks the observed depths above every earlier report at a ridge spreading this slowly, which is the comparison the claim kind describes",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "claim:degassing-volume-change",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence carries the whole chain from degassing through volume change and high strain rates to deep earthquakes",
      "source_locators": [
        "page:5:block:003"
      ]
    },
    {
      "witness_key": "claim:depth-resolution-tests",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states that depth resolution tests were carried out to assess location reliability",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "claim:detachment-inactive",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence suggests the detachment fault is inactive, and the hypothesised modality matches the suggesting verb",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "claim:enriched-mantle-source",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence reports the prior interpretation as low degrees of partial melting of an enriched source near the Romanche transform",
      "source_locators": [
        "page:5:block:005"
      ]
    },
    {
      "witness_key": "claim:eq-in-mantle",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence carries the inference that the earthquakes mostly occur in the mantle below the crust",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "claim:events-with-eruptions",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence associates the named magmatic-tectonic events with volcanic eruptions",
      "source_locators": [
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "claim:faults-favor-migration",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives older breaks in the rock over a deep reservoir a part in letting melt rise and set off earthquakes, which is the role the claim kind projects",
      "source_locators": [
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "claim:fig3a-content",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited caption sentence lists the tectonic information marked on the map of the RTI area",
      "source_locators": [
        "page:4:block:006"
      ]
    },
    {
      "witness_key": "claim:fig5-estimated-primary",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited caption sentence states that the dashed blue lines and numbers give the estimated primary-melt CO2 contents on each map",
      "source_locators": [
        "page:6:block:005"
      ]
    },
    {
      "witness_key": "claim:fixed-depth-rms",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states how the RMS residuals behaved when the depths were held fixed",
      "source_locators": [
        "page:8:block:001"
      ]
    },
    {
      "witness_key": "claim:focal-mechanisms-shown",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited caption sentence states that focal mechanisms are shown as blue and white beach balls",
      "source_locators": [
        "page:3:block:004"
      ]
    },
    {
      "witness_key": "claim:focus-on-segments",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the scope of the interpretation along the named segments and discontinuities",
      "source_locators": [
        "page:2:block:003"
      ]
    },
    {
      "witness_key": "claim:forced-depths-values",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence lists the four depths at which the subset events were held fixed",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "claim:global-trends",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the definition of the global volatile to non-volatile ratios from undegassed basalts and melt inclusions",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "claim:hydrothermal-cooling",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the first derivation carries the hydrothermal cooling hypothesis and the second carries the taken-together sentence that withholds support, which is the projected disposition",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "claim:hypocentral-distance",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence defines D as the hypocentral distance in kilometres",
      "source_locators": [
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "claim:ipgp-contribution",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the contribution number",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "claim:licence-terms",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited block states the licence and the terms the claim kind describes",
      "source_locators": [
        "page:11:block:005"
      ]
    },
    {
      "witness_key": "claim:local-magnitudes",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states that local magnitudes were determined",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "claim:magmatic-tectonic",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence carries the magmatic-tectonic explanation and the second derivation carries the sentence that sets the melt-movement mechanism aside; the record calls it the fourth explanation considered, which is its place in the order of the four explanations in the reading, while this sentence labels it the third possibility",
      "source_locators": [
        "page:4:block:002",
        "page:5:block:001"
      ]
    },
    {
      "witness_key": "claim:max-depth-compilation",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the compilation of maximum depths and full spreading rates for slow- and ultraslow-spreading ridges",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "claim:max-depth-covariates",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence lists the additional information included in the compilation",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "claim:max-depth-influences",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited caption sentence lists the processes that affect the maximum depths",
      "source_locators": [
        "page:5:block:010"
      ]
    },
    {
      "witness_key": "claim:max-depth-not-following",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the two derivations carry the two halves of one sentence broken across a page, and together they state the departure from the depth and spreading-rate relationship",
      "source_locators": [
        "page:2:block:007",
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "claim:max-depth-other-factors",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the dependence of maximum earthquake depth on tectonic, hydrothermal and petrological processes",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "claim:max-depth-selection",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the selection rule for the compiled maximum depths",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "claim:max-likelihood-preferred",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states that the maximum likelihood solution was the preferred result",
      "source_locators": [
        "page:7:block:004"
      ]
    },
    {
      "witness_key": "claim:measured-near-solubility",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states that the existing measurements lie very close to the calculated solubility",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "claim:melt-continues-degassing",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states continued degassing producing earthquakes over the depth range the record carries, and the hypothesised modality matches the conditional",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "claim:melt-focusing",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the focusing of melt in a narrow zone beneath the ridge axis",
      "source_locators": [
        "page:1:block:002"
      ]
    },
    {
      "witness_key": "claim:melt-freeze-lithosphere",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the possible freezing of melt at the base of the lithosphere and the reflections it would produce",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "claim:melt-movement-strain",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states that melt movement introduces high strain rates producing brittle failure in the ductile lower crust",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "claim:melt-resides-fractionates",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the residence, fractionation and evolution of ascending melt at those depths",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "claim:migration-unknown",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the gap in understanding of melt migration and the negated modality matches its no clear understanding",
      "source_locators": [
        "page:1:block:003"
      ]
    },
    {
      "witness_key": "claim:model-selection",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the criterion used to select among the five velocity models",
      "source_locators": [
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "claim:model1-inappropriate",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence rules that velocity model out for events under the ridge axis, which is the unsuitability the claim kind states",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "claim:more-events-needed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states both halves of the limitation, that not all events are low-frequency and that more earthquakes would be required",
      "source_locators": [
        "page:5:block:008"
      ]
    },
    {
      "witness_key": "claim:no-competing-interests",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence declares no competing interests and the negated modality matches",
      "source_locators": [
        "page:10:block:047"
      ]
    },
    {
      "witness_key": "claim:no-detachment-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the absence of evidence for detachment faults at this segment and the negated modality matches",
      "source_locators": [
        "page:4:block:001"
      ]
    },
    {
      "witness_key": "claim:not-location-artifact",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence carries the inference that the unexpected depths are not an artifact of location errors",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "claim:ntd1-origin",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence infers a magmatic and tectonic origin from the seafloor basalts and peridotites",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "claim:nucleation-similar-volcanoes",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the similarity of the proposed nucleation mechanism to rapid CO2 degassing beneath active volcanoes",
      "source_locators": [
        "page:5:block:008"
      ]
    },
    {
      "witness_key": "claim:occ-dome-ruptures",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence proposes ruptures on high-angle normal faults as the origin of the shallow earthquakes beneath the dome",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "claim:offaxis-magmatism",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence relates the off-axis shallow microseismicity to off-axis magmatism in the crust",
      "source_locators": [
        "page:5:block:001"
      ]
    },
    {
      "witness_key": "claim:peer-review",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited block carries the thanks to the anonymous reviewers and the availability of a peer review file",
      "source_locators": [
        "page:11:block:003"
      ]
    },
    {
      "witness_key": "claim:peridotites-exhumed-mantle",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the two derivations carry the two halves of one sentence broken across a page, the seafloor peridotites and the inference to exhumed mantle and a tectonic origin",
      "source_locators": [
        "page:1:block:006",
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "claim:polarity-picking",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the use of P-phase first-motion polarities picked from unfiltered vertical-component data",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "claim:primary-vs-pre-eruptive",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence draws the distinction between primary and pre-eruptive melts",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "claim:publisher-note",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence is the publisher neutrality note itself",
      "source_locators": [
        "page:11:block:004"
      ]
    },
    {
      "witness_key": "claim:ratios-good-proxy",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states that the two ratios of melt inclusions are a good proxy for CO2 concentration",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "claim:rb90-ba90-calculation",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the calculation of the two proxy concentrations in melts in equilibrium with Fo 90 olivine",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "claim:rc1-amagmatic",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states that the RTI segment is amagmatic and how it is bounded",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "claim:rc2-basalts",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the further support from the extensive seafloor basalts",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "claim:rc2-magmatic-origin",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence infers a magmatic origin for the segment from the axial morphology",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "claim:rc2-magmatically-robust",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence infers a magmatically robust segment from the median valley and the neo-volcanic ridge",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "claim:rc2-rc3-analyzed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the analysis of the samples in the two named segments",
      "source_locators": [
        "page:8:block:005"
      ]
    },
    {
      "witness_key": "claim:recent-tectonic-deformation",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence infers recent active tectonic deformation from the faulting of the OCC surface, and the recorded gap explains why no relation is derived from it",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "claim:reduced-velocity-preferred",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the preference for a normal or slightly decreased velocity model",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "claim:relocation-inputs",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence names both inputs of the relocation",
      "source_locators": [
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "claim:s-wave-delays-removed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the removal of the S-wave delays before inversion",
      "source_locators": [
        "page:7:block:005"
      ]
    },
    {
      "witness_key": "claim:samples-degassed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence carries both the closeness of solubility to measured contents and the conclusion that the samples are degassed",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "claim:seafloor-basalts-degassed",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the expectation that seafloor basalts are mostly degassed",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "claim:selected-model-preferred",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the preference for the selected model over the minimum model, which the preceding sentence of the same block names",
      "source_locators": [
        "page:6:block:004"
      ]
    },
    {
      "witness_key": "claim:shear-zone",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the first derivation carries the shear-zone hypothesis, stated as another hypothesis after two earlier ones in the reading, and the second carries the sentence that says the observations do not support it",
      "source_locators": [
        "page:3:block:003"
      ]
    },
    {
      "witness_key": "claim:shear-zone-detachment",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the expectation of a deep-mantle high-strain shear zone during detachment faulting",
      "source_locators": [
        "page:3:block:003"
      ]
    },
    {
      "witness_key": "claim:snapshot-limitation",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the snapshot limitation of the microseismicity record",
      "source_locators": [
        "page:2:block:004"
      ]
    },
    {
      "witness_key": "claim:solutions-not-robust",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states that the solutions are not very robust and gives the OBS spacing as the main reason, with the ray path limitation in the next sentence of the same block",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "claim:station-corrections",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the calculation of station corrections and the removal of the S-wave delays",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "claim:station-corrections-applied",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states that the station corrections from that program were successfully applied",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "claim:station-corrections-iterative",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the iterative station corrections and both purposes the claim kind names",
      "source_locators": [
        "page:7:block:005"
      ]
    },
    {
      "witness_key": "claim:tests-support-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states that the depth resolution tests further support the deep events",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "claim:tf-deep-eq",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence reports the deep earthquakes along transform faults and the deformation they are linked to",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "claim:trace-element-assumption",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the assumption behind estimating CO2 from trace element abundances",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "claim:ultraslow-co2-high",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence proposes a likely high CO2 content at the named ultraslow-spreading ridges",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "claim:updated-depth-data",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence names the three sites whose reported data were updated",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "claim:velocity-structure-matters",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the importance of the velocity structure for location precision",
      "source_locators": [
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "claim:vent-field-too-far",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states that the extinct vent field is relatively far from the present-day axial valley and would not affect the lithosphere beneath the segment",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "claim:volatile-role-unknown",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states that the role of volatiles during melt migration remains unknown",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "claim:volatiles-control-magma",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the control of volatile concentration over magma properties and eruption dynamics",
      "source_locators": [
        "page:5:block:002"
      ]
    },
    {
      "witness_key": "claim:volatiles-extend-melting",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states that abundant volatiles would extend the depth of incipient melting",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "claim:zero-position-rti",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited block is the continuation of the figure caption and states that the zero position is the RTI location",
      "source_locators": [
        "page:3:block:005"
      ]
    },
    {
      "witness_key": "obs:events-identified-760",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence carries the count and the scope of earthquakes identified and registered in the database",
      "source_locators": [
        "page:6:block:002"
      ]
    },
    {
      "witness_key": "obs:fm-new-3",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the three new well-constrained focal mechanism solutions obtained in this study",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "obs:fm-previous-3",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the same sentence states the three previous solutions for earthquake swarms, which is the scope this record projects",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "obs:fm-total-6",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the same sentence states that the new and previous solutions together provide six focal mechanisms",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "obs:forced-depth-subset",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the subset of events and the depth range the scope names",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "obs:located-514",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW both derivations state the located count, and the measured determination matches a count obtained by locating the events",
      "source_locators": [
        "page:2:block:003",
        "page:6:block:005"
      ]
    },
    {
      "witness_key": "obs:magnitude-groups",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the division into three groups and names them",
      "source_locators": [
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "obs:obs-deployed-19",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the first derivation states the instrument network that acquired the data and the second states its deployment, both with the count the record carries",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ]
    },
    {
      "witness_key": "obs:obs-useful-17",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW both derivations state the seventeen useful instruments from which arrivals were detected automatically",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ]
    },
    {
      "witness_key": "obs:quality-categories",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW both derivations state the classification of the locations into four categories",
      "source_locators": [
        "page:2:block:003",
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "obs:relocated-364",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the count of well-constrained events that were relocated and the program used",
      "source_locators": [
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "obs:romanche-2016-subevents",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited caption sentence states the subevents of the named earthquake, and the recorded gap explains why neither is given its own record",
      "source_locators": [
        "page:3:block:004"
      ]
    },
    {
      "witness_key": "obs:subsection-count",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the subdivision into four subsections and names them",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "obs:velest-subdataset",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the size and purpose of the sub-dataset",
      "source_locators": [
        "page:6:block:004"
      ]
    },
    {
      "witness_key": "obs:velocity-models-five",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the five one-dimensional velocity models and the profile they derive from",
      "source_locators": [
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "obs:well-relocated-276",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the count of well relocated events and that they replaced the earlier locations in the final catalogue",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "ratio:co2-ba",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW both derivations carry the ratio, its value and its uncertainty, and the projected numerator and denominator are the two sides of the ratio as written",
      "source_locators": [
        "page:5:block:004",
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "ratio:co2-rb",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW both derivations carry the ratio, its value and its uncertainty, and the projected numerator and denominator are the two sides of the ratio as written",
      "source_locators": [
        "page:5:block:004",
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "obs:abstract-co2-primary",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited abstract sentence carries the analyte, the bounds, the unit and the primary-melt stage, the tilde supports the approximate qualification and the indicating verb supports the estimated determination",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "obs:co2-gas-loss",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence carries the percentage loss to the nucleated gas phase by the time the melt reaches the seafloor",
      "source_locators": [
        "page:5:block:003"
      ]
    },
    {
      "witness_key": "obs:eq-atlantic-co2-average",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence carries the average concentration, the unit and the proxy, and the suggesting verb of the previous studies supports the hypothesised modality",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "obs:eq-atlantic-co2-max",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence carries the upper figure in the same unit and the same proxy; the record keeps the bound and drops the source tilde, which weakens no claim",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "obs:average-depth-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the average depth uncertainty and the tilde supports the approximate qualification",
      "source_locators": [
        "page:7:block:009"
      ]
    },
    {
      "witness_key": "obs:avg-horizontal-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the three derivations carry the legend value, the caption sentence naming it the average horizontal uncertainty after relocation, and the methods sentence giving the updated value",
      "source_locators": [
        "page:3:block:003",
        "page:3:block:004",
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "obs:axial-event-depth-stable",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states that most axial event depths remain between the two bounds across the velocity models",
      "source_locators": [
        "page:7:block:009"
      ]
    },
    {
      "witness_key": "obs:b-value",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the b value and that it was calculated with the named software",
      "source_locators": [
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "obs:brittle-thickness-ntds",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the upper bound on brittle lithospheric thickness at the segment boundaries and the suggesting verb supports the hypothesised modality",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "obs:cluster-depth-west",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the shallow focal depths of the cluster west of the axial valley",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "obs:co2-saturation-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the saturation depth and names the solubility model, which is the modelled determination",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "obs:co2-saturation-pressure",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the saturation pressure and names the solubility model",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "obs:co2-saturation-temperature",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the saturation temperature and names the solubility model",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "obs:cold-lithosphere-age",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the age of the cold lithosphere in parentheses as the record projects it",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "obs:criteria-met-fraction",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the proportion of located earthquakes meeting at least two criteria",
      "source_locators": [
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "obs:criterion-arrivals",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the more-than-eight arrivals criterion, which is the open lower bound projected",
      "source_locators": [
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "obs:criterion-gap",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the azimuthal station gap criterion",
      "source_locators": [
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "obs:criterion-s-distance",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence states the multiple of the focal depth distance for the S-wave arrival criterion",
      "source_locators": [
        "page:7:block:008"
      ]
    },
    {
      "witness_key": "obs:crust-age-west-flank",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the age of the western flank crust",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "obs:crust-thickness-west-flank",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the thickness of that crust with its uncertainty",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "obs:crustal-age-offaxis",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the crustal age up to which the boundary remains shallow",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "obs:degassing-depth-range",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the depth range in which the degassing melt would produce earthquakes",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "obs:depth-uncertainty-cap",
      "source_support": "PARTIAL",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited block carries the bound and the unit but the sentence begins on the previous page, so nothing in the block the derivation reaches says the bound is the depth uncertainty of the located earthquakes and the record cites no second locator",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "obs:dry-melting-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the depths at which extensive dry melting commences",
      "source_locators": [
        "page:1:block:002"
      ]
    },
    {
      "witness_key": "obs:error-ellipsoid-confidence",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the confidence level of the error ellipsoid",
      "source_locators": [
        "page:7:block:005"
      ]
    },
    {
      "witness_key": "obs:expected-brittle-thickness",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the corresponding brittle lithospheric thickness bound",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "obs:expected-depth-slow",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the expected depth bound beneath slow-spreading ridges, names the seafloor reference and attributes it to thermal models",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "obs:expected-depth-ultraslow",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the same sentence gives the expected depth bound beneath ultraslow-spreading ridges with the same reference surface and basis",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "obs:expected-max-depth-32",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the expected maximum earthquake depth for that full spreading rate",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "obs:fig3-shading-threshold",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited caption sentence gives the depth that separates the two shadings",
      "source_locators": [
        "page:4:block:007"
      ]
    },
    {
      "witness_key": "obs:fig3e-elevation-scale",
      "source_support": "PARTIAL",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited block carries the two elevation numbers, the unit and the panel they belong to, but nothing in it says the range is the colour scale of a bathymetric map",
      "source_locators": [
        "page:4:block:005"
      ]
    },
    {
      "witness_key": "obs:fig4-isotherm",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited block is the figure caption and states the isotherm the dashed black line indicates",
      "source_locators": [
        "page:5:block:010"
      ]
    },
    {
      "witness_key": "obs:fm-fault-plane-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence lists this selection criterion with its bound",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "obs:fm-gap",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence lists the azimuthal gap criterion with its bound",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "obs:fm-misfit",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence lists the average misfit criterion with its bound",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "obs:fm-polarities",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence lists the P-wave polarity criterion as an open lower bound",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "obs:fm-probability",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence lists the mechanism probability criterion with its unit and bound",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "obs:fm-station-ratio",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence lists the station distribution ratio criterion with its bound",
      "source_locators": [
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "obs:forced-depth-range",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the depth range of the subset events",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "obs:full-spreading-rate",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the full spreading rate with its unit and the tilde the approximate qualification records",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "obs:group-b-values",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the range of the b values of the three groups and says they were determined",
      "source_locators": [
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "obs:high-frequency-threshold",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the frequency above which energy is absent from some deep earthquakes and attributes it to spectral analyses",
      "source_locators": [
        "page:5:block:008"
      ]
    },
    {
      "witness_key": "obs:horizontal-uncertainty-cap",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence names the horizontal uncertainties and gives their bound and unit",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "obs:lithospheric-age-interval",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited caption sentence gives the interval of the lithospheric age contours",
      "source_locators": [
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "obs:magnitude-completeness",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the magnitude completeness and says it was calculated",
      "source_locators": [
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "obs:mar-segment-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the length of the segment between the two transform faults",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "obs:max-event-separation",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the maximum event separation used",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "obs:mean-horizontal-error",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the mean horizontal error with its tilde",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "obs:mean-vertical-error",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the same sentence gives the mean vertical error with its tilde",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "obs:median-valley-width",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the width of the median valley of that segment",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "obs:melting-initiation-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the depths at which melting initiates in the presence of volatiles",
      "source_locators": [
        "page:1:block:002"
      ]
    },
    {
      "witness_key": "obs:min-catalog-links",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the minimum catalog links per event pair",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "obs:min-obs-per-event",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the minimum number of instruments on which each event had to be detected",
      "source_locators": [
        "page:6:block:002"
      ]
    },
    {
      "witness_key": "obs:model1-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the depth at which that model's P-wave velocity exceeds the quoted value",
      "source_locators": [
        "page:7:block:009"
      ]
    },
    {
      "witness_key": "obs:model1-p-velocity",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the P-wave velocity bound at that depth, and a velocity a model shows is a modelled determination",
      "source_locators": [
        "page:7:block:009"
      ]
    },
    {
      "witness_key": "obs:occ-transect-halfwidth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited caption sentence gives the half-width of the band around the profile for those transects",
      "source_locators": [
        "page:4:block:006"
      ]
    },
    {
      "witness_key": "obs:offaxis-swarm-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the depth bound of the off-axis shallow microseismicity west of the axis",
      "source_locators": [
        "page:5:block:001"
      ]
    },
    {
      "witness_key": "obs:perturbed-deep-events",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the depth bound of the deep events located under both perturbed velocity models",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "obs:pore-pressure-trigger",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the pore pressure increase that can trigger earthquakes with its unit",
      "source_locators": [
        "page:5:block:003"
      ]
    },
    {
      "witness_key": "obs:profile-halfwidth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited caption sentence gives the half-width of the band within which depths are plotted",
      "source_locators": [
        "page:3:block:005"
      ]
    },
    {
      "witness_key": "obs:profile-tick-interval",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited caption sentence gives the interval marked on the top of the profile",
      "source_locators": [
        "page:3:block:005"
      ]
    },
    {
      "witness_key": "obs:quality-a-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited legend text gives the uncertainty bound for this quality class as the reading carries it",
      "source_locators": [
        "page:3:block:004"
      ]
    },
    {
      "witness_key": "obs:quality-b-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited legend text gives the uncertainty bound for this quality class as the reading carries it",
      "source_locators": [
        "page:3:block:004"
      ]
    },
    {
      "witness_key": "obs:quality-c-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited legend text gives the uncertainty bound for this quality class as the reading carries it",
      "source_locators": [
        "page:3:block:004"
      ]
    },
    {
      "witness_key": "obs:quality-d-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited legend text gives the lower and upper uncertainty bounds for this quality class",
      "source_locators": [
        "page:3:block:004"
      ]
    },
    {
      "witness_key": "obs:recording-duration",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the continuous recording duration with its unit and tilde",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "obs:refraction-constraint-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the depth to which the profile constrains velocity and names the sea-level reference",
      "source_locators": [
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "obs:relocation-gap",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the azimuthal gap bound of those earthquakes",
      "source_locators": [
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "obs:relocation-iterations",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the number of iterations carried out",
      "source_locators": [
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "obs:relocation-obs-count",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the number of instruments on which all those earthquakes were detected as an open lower bound",
      "source_locators": [
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "obs:relocation-rms",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the RMS residual bound of those earthquakes",
      "source_locators": [
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "obs:relocation-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the uncertainty bound of those earthquakes",
      "source_locators": [
        "page:7:block:006"
      ]
    },
    {
      "witness_key": "obs:rms-residual-cap",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence names the RMS residuals and gives their bound and unit",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "obs:solubility-temperature",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence names the temperature among the parameters of the solubility calculation",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "obs:station-gap-cap",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence names the station gaps and gives their bound",
      "source_locators": [
        "page:7:block:001"
      ]
    },
    {
      "witness_key": "obs:studied-portion-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the length of the studied portion of the ridge, and the recorded gap explains why the offsetting discontinuities yield no relation here",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "obs:subdataset-arrivals",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the arrivals required per earthquake in the sub-dataset",
      "source_locators": [
        "page:6:block:004"
      ]
    },
    {
      "witness_key": "obs:subdataset-gap",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the station gap required per earthquake in the sub-dataset",
      "source_locators": [
        "page:6:block:004"
      ]
    },
    {
      "witness_key": "obs:subsection-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the length range of the four subsections",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "obs:velest-iterations",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the number of iterations after which the two models' residuals are close",
      "source_locators": [
        "page:6:block:004"
      ]
    },
    {
      "witness_key": "obs:velocity-perturbation",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the velocity perturbation applied at all depths and its purpose",
      "source_locators": [
        "page:7:block:010"
      ]
    },
    {
      "witness_key": "obs:young-crust-age",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK NO_SUBJECT_IN_ROW the cited sentence gives the age bound for a magmatically accreted young crust",
      "source_locators": [
        "page:7:block:009"
      ]
    },
    {
      "witness_key": "claim:cruise-thanks",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited acknowledgement sentence names the cruise and the people thanked, and the subject cruise is named in that block",
      "source_locators": [
        "page:10:block:043"
      ]
    },
    {
      "witness_key": "claim:co2-degassing-mechanism",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the first derivation carries the proposed mechanism and the second names the segment and says it is the preferred possibility, which is the projected disposition and subject",
      "source_locators": [
        "page:1:block:001",
        "page:5:block:002"
      ]
    },
    {
      "witness_key": "claim:co2-lab-melt",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited abstract sentence states the influence of primitive-melt CO2 on melt beneath the boundary, which the block writes out in full rather than by the subject's short name",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "claim:deep-eq-interpretation",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited caption sentence interprets the deep earthquakes as volume change from degassing and names the ridge by its abbreviation, which is the subject's tag",
      "source_locators": [
        "page:7:block:012"
      ]
    },
    {
      "witness_key": "claim:deep-events-not-artifacts",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence states that the deep events beneath that segment are well constrained and not artifacts, and names the segment",
      "source_locators": [
        "page:8:block:001"
      ]
    },
    {
      "witness_key": "claim:keller-volatiles-flush",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence reports the prior proposal and names the boundary it accumulates at",
      "source_locators": [
        "page:5:block:010"
      ]
    },
    {
      "witness_key": "claim:lab-melt-co2-h2o",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence proposes the combination of the two volatiles behind melt at the boundary it names",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "claim:magmatism-dominates",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence states that magmatism dominates crustal accretion at the named segment",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "claim:no-active-vents-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence states the absence of observations of active vents on that segment axis and the negated modality matches",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "claim:no-eq-below-20km",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence states the absence of earthquakes below that depth beneath the named axis and gives the temperature reason",
      "source_locators": [
        "page:5:block:007"
      ]
    },
    {
      "witness_key": "claim:no-eruption-evidence",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence states the absence of evidence for a current eruption in the axial valley it names",
      "source_locators": [
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "claim:small-pressure-increase",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence proposes the small pressure increase from degassing as the trigger of the earthquakes beneath the named ridge axis",
      "source_locators": [
        "page:5:block:003"
      ]
    },
    {
      "witness_key": "claim:tomography-normal-vpvs",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence reports the normal ratios found by tomography in the named segment",
      "source_locators": [
        "page:7:block:003"
      ]
    },
    {
      "witness_key": "claim:volatiles-reduce-solidus",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the two derivations carry the two halves of one sentence broken across a page, the reported reduction of the solidus and the melt at the boundary the subject names",
      "source_locators": [
        "page:5:block:010",
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "claim:vp-vs-reasonable",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence states that the chosen ratio gives the lowest residuals and the most located earthquakes and is therefore reasonable, and it names the ratio that is the subject",
      "source_locators": [
        "page:7:block:003"
      ]
    },
    {
      "witness_key": "obs:mar-events-317",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the figure text carries the total and the methods sentence states the same count along the ridge, naming the subject",
      "source_locators": [
        "page:3:block:004",
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "obs:obs-no-data",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited caption sentence names one instrument that generated no data, and its singular definite phrasing is the count of one the record carries",
      "source_locators": [
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "obs:romanche-events-197",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the figure text carries the total and the methods sentence states the same count along the transform fault, naming the subject",
      "source_locators": [
        "page:3:block:003",
        "page:7:block:007"
      ]
    },
    {
      "witness_key": "obs:co2-ba-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives this proxy estimate for that segment with its bounds and unit, and the pre-eruptive stage is the one the surrounding sentence of the block sets",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "obs:co2-ba-rc3",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives this proxy estimate for that segment with its bounds and unit",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "obs:co2-ba90-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the primary-melt estimate from this proxy for that segment",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "obs:co2-ba90-rc3",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the same sentence gives the primary-melt estimate from this proxy for the other segment",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "obs:co2-calc-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the calculated content for the melts of that segment with its bounds and unit",
      "source_locators": [
        "page:5:block:005"
      ]
    },
    {
      "witness_key": "obs:co2-calc-rc3",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the same sentence gives the calculated content for the other segment",
      "source_locators": [
        "page:5:block:005"
      ]
    },
    {
      "witness_key": "obs:co2-pre-eruptive-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the estimated pre-eruptive concentrations for that segment",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "obs:co2-primary-rc2-floor",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence states the at-least value for the primary melts of that segment, which is the open lower bound projected, and its suggesting verb matches the hypothesised modality",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "obs:co2-rb-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives this proxy estimate for that segment",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "obs:co2-rb-rc3",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives this proxy estimate for the other segment",
      "source_locators": [
        "page:8:block:006"
      ]
    },
    {
      "witness_key": "obs:co2-rb90-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the primary-melt estimate from this proxy for that segment",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "obs:co2-rb90-rc3",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the same sentence gives the primary-melt estimate from this proxy for the other segment",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "obs:lab-water-content",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the water content at the base of the boundary as an upper bound",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "obs:rc2-ba",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the barium content of the samples in that segment as an open lower bound",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "obs:rc2-rb",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the rubidium content of the samples in that segment as an open lower bound",
      "source_locators": [
        "page:5:block:004"
      ]
    },
    {
      "witness_key": "obs:swir-highest-co2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the highest reported melt content at that ridge",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "obs:abstract-deep-eq-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited abstract sentence gives the depth range of the deep earthquakes along the named ridge axis",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "obs:bdb-at-ntd2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence puts the boundary at that depth beneath the named discontinuity",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "obs:bdb-depth-if-cold",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the depth the boundary would have under the cold and thick lithosphere explanation, and the hypothesised modality matches",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "obs:bdb-isotherm-fig6",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited caption sentence gives the isotherm the boundary corresponds to",
      "source_locators": [
        "page:7:block:011"
      ]
    },
    {
      "witness_key": "obs:bdb-isotherm-slow",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the isotherm with its uncertainty that the maximum earthquake depth corresponds to",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "obs:bdb-isotherms-cold",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the same sentence gives the isotherm range a boundary at that depth would correspond to",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "obs:bdb-shallow-offaxis",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the depth below which the boundary remains off-axis",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "obs:coverage-mar-axis",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the length of ridge axis the network covered and names the ridge by the abbreviation that is the subject's tag",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "obs:coverage-romanche",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the length of the eastern transform fault the network covered and names it",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "obs:crust-thickness-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited caption sentence gives the crustal thickness beneath the named segment with its uncertainty",
      "source_locators": [
        "page:7:block:011"
      ]
    },
    {
      "witness_key": "obs:deep-eq-bsf",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited caption sentence gives the depth range of the deep earthquakes below the seafloor beneath the axis it names by the subject's abbreviation",
      "source_locators": [
        "page:7:block:012"
      ]
    },
    {
      "witness_key": "obs:deep-eq-rc2-1619",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the observed depth range of the deep earthquakes beneath the named segment axis",
      "source_locators": [
        "page:2:block:006"
      ]
    },
    {
      "witness_key": "obs:deep-microseismicity-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the depth of the deep microseismicity beneath the named segment axis as the second key observation",
      "source_locators": [
        "page:2:block:004"
      ]
    },
    {
      "witness_key": "obs:depth-range-ntd2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the depth bound beneath the named discontinuity",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "obs:depth-range-occ",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the same sentence gives the depth bound beneath the core complex it names",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "obs:hot-mantle-temperature",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the mantle temperature bound at the named segment",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "obs:iceland-depths",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the depth bound of the events at the place it names, which the reading hyphenates across a line",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "obs:instrument-spacing",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the three derivations give the same spacing, and the second names the instrument network that is the subject",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002",
        "page:8:block:003"
      ]
    },
    {
      "witness_key": "obs:lab-melt-fraction",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the melt fraction required at the base of the boundary and attributes it to a proposal",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "obs:mantle-temperature-rc2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the modelled temperature range at that depth beneath the named segment axis",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "obs:mar-half-spreading-rate",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the half-spreading rate of the ridge it names",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "obs:mayotte-depths",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the depth bound of the events offshore the island it names",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "obs:normal-depth-ntd2",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the normal-depth range beneath the named discontinuity as the third key observation",
      "source_locators": [
        "page:2:block:004"
      ]
    },
    {
      "witness_key": "obs:ntd1-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the length of the named discontinuity",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "obs:ntd2-eq-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the depth to which the earthquakes reach beneath the named discontinuity",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "obs:ntd2-offset",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the ridge offset of the named discontinuity",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "obs:offaxis-microseismicity-depth",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the depth to which the off-axis shallow microseismicity west of the named segment axis reaches",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "obs:rc2-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the length of the named segment",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "obs:rc3-length",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the length of the named segment",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "obs:shallow-eq-rti",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the depth range of the shallow earthquakes on the outside corner of the intersection it names",
      "source_locators": [
        "page:2:block:004"
      ]
    },
    {
      "witness_key": "obs:subsolidus-temperature",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the sub-solidus temperature for anhydrous peridotites at the boundary it names",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "obs:temperature-below-20km",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the temperature bound below that depth beneath the named ridge axis and says it would hinder nucleation",
      "source_locators": [
        "page:5:block:007"
      ]
    },
    {
      "witness_key": "obs:vp-vs-test-range",
      "source_support": "SUPPORTED",
      "rationale": "DIGEST_OK SUBJECT_IN_BLOCK the cited sentence gives the range of ratios used in the test and names the ratio that is the subject",
      "source_locators": [
        "page:7:block:002"
      ]
    },
    {
      "witness_key": "event:romanche-2016",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited caption sentence names the earthquake with its year and magnitude, and the recorded gap explains why the subevents get no records",
      "source_locators": [
        "page:3:block:004"
      ]
    },
    {
      "witness_key": "feature:askja",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the volcano and its kind",
      "source_locators": [
        "page:4:block:002",
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "feature:axial-melt-lens",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the melt lenses and what they are used for",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "feature:axial-valley",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the axial valley",
      "source_locators": [
        "page:2:block:005"
      ]
    },
    {
      "witness_key": "feature:bdb",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the boundary, its abbreviation and the separation the projected description gives",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "feature:chain-tf",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the transform fault as one of the two bounding the segment",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "feature:eq-atlantic",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the ocean region of the study",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "feature:extinct-vent-field",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the extinct vent field and its kind",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "feature:fagradalsfjall",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the peninsula and its kind",
      "source_locators": [
        "page:4:block:002",
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "feature:fracture-zone",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited block carries the map legend entry that names this feature",
      "source_locators": [
        "page:3:block:003"
      ]
    },
    {
      "witness_key": "feature:gakkel",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the ridge among the ultraslow-spreading ones",
      "source_locators": [
        "page:5:block:009"
      ]
    },
    {
      "witness_key": "feature:hummocky",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited legend text names this seafloor kind and the caption derivation confirms what it marks",
      "source_locators": [
        "page:4:block:004",
        "page:4:block:007"
      ]
    },
    {
      "witness_key": "feature:iceland",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the island, which the reading hyphenates across a line, and its kind follows from the places it locates there",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "feature:inactive-mound",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited caption sentence names the inactive hydrothermal mound and the legend derivation repeats it",
      "source_locators": [
        "page:2:block:007",
        "page:4:block:004"
      ]
    },
    {
      "witness_key": "feature:juan-de-fuca",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the plate beneath which the reflections were observed",
      "source_locators": [
        "page:6:block:001"
      ]
    },
    {
      "witness_key": "feature:knipovich",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the ridge whose seamount data were updated",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "feature:lab",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the second derivation gives the abbreviation the record uses as its name and the first carries the spelled-out form",
      "source_locators": [
        "page:1:block:001",
        "page:5:block:010"
      ]
    },
    {
      "witness_key": "feature:logachev",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the seamount and its kind",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "feature:mar",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW both derivations name the ridge, and the caption line gives the abbreviation the record keeps as a tag",
      "source_locators": [
        "page:1:block:001",
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "feature:mar-segment",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the first derivation carries the description of the segment between the two transform faults and the second gives the name the record uses",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:004"
      ]
    },
    {
      "witness_key": "feature:mayotte",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the island and its kind",
      "source_locators": [
        "page:4:block:002",
        "page:4:block:003"
      ]
    },
    {
      "witness_key": "feature:median-valley",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the median valley",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "feature:moho",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the schematic text names it and the caption sentence names the expected interface",
      "source_locators": [
        "page:7:block:010",
        "page:7:block:011"
      ]
    },
    {
      "witness_key": "feature:neo-volcanic-ridge",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the neo-volcanic ridge and gives its orientation",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "feature:ntd1",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the first derivation names the discontinuity and the second gives its orientation",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "feature:ntd1-faults",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence gives the striking directions and the characterisation the projected description repeats",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "feature:ntd2",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the first derivation names the discontinuity and the second gives its orientation",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "feature:ntd2-faults",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence gives the normal faults, their pattern and their two striking directions",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "feature:occ",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the core complex and its abbreviation",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "feature:occ-corrugated-surface",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the legend text names the corrugated surface and the caption derivation ties it to the core complex",
      "source_locators": [
        "page:4:block:004",
        "page:4:block:006"
      ]
    },
    {
      "witness_key": "feature:occ-surface-faults",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence gives the normal faults cutting the surface and their two striking directions, and the recorded gap explains why the cutting yields no relation",
      "source_locators": [
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "feature:occ-termination",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the first derivation names the termination and the caption derivation repeats it",
      "source_locators": [
        "page:2:block:005",
        "page:4:block:006"
      ]
    },
    {
      "witness_key": "feature:rainbow",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the massif, and the recorded gap explains why its unnamed discontinuity yields no relation",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "feature:rc1",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names this subsection",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "feature:rc2",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names this subsection",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "feature:rc2-bounding-faults",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence gives the bounding faults, their dip sense and their orientation",
      "source_locators": [
        "page:4:block:001"
      ]
    },
    {
      "witness_key": "feature:rc3",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the first derivation names the segment south of the second discontinuity and the second gives its orientation",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:001"
      ]
    },
    {
      "witness_key": "feature:romanche-faults",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited caption sentence states that the white lines show faults along the transform, which is the projected description",
      "source_locators": [
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "feature:romanche-tf",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the derivations give the kind, the name in the form the record uses and the alternative wording it keeps as a tag",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:002",
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "feature:romanche-transform-valley",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited map text names the transform valley",
      "source_locators": [
        "page:3:block:003"
      ]
    },
    {
      "witness_key": "feature:rti",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the intersection in full and by its abbreviation",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "feature:rti-detachment",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the westward dipping detachment fault",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "feature:suspended-valley",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited map text names the suspended valley",
      "source_locators": [
        "page:3:block:003"
      ]
    },
    {
      "witness_key": "feature:swir",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the ridge in full and by its abbreviation",
      "source_locators": [
        "page:3:block:001"
      ]
    },
    {
      "witness_key": "feature:swir-oblique",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names this supersegment",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "feature:swir-segment-8",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names this segment",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "feature:tf",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names oceanic transform faults and their abbreviation",
      "source_locators": [
        "page:1:block:004"
      ]
    },
    {
      "witness_key": "feature:transverse-ridge",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited map text names the transverse ridge",
      "source_locators": [
        "page:3:block:003"
      ]
    },
    {
      "witness_key": "feature:volcanic-cones",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the legend text names the volcanoes and the caption derivation confirms the volcanic cones it marks",
      "source_locators": [
        "page:4:block:004",
        "page:4:block:007"
      ]
    },
    {
      "witness_key": "feature:west-indian-ocean",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the ocean region",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "work:cruise-data",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the raw data and reports and gives the website address, which the record carries with the ligature of the reading resolved to plain letters",
      "source_locators": [
        "page:8:block:008"
      ]
    },
    {
      "witness_key": "work:earthquake-catalog",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the two derivations carry the deposited catalogue and arrivals and the two halves of the identifier the reading breaks across a block boundary",
      "source_locators": [
        "page:8:block:008",
        "page:8:block:009"
      ]
    },
    {
      "witness_key": "work:petdb",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the methods derivation names the database and gives its address and the caption derivation shows what was taken from it",
      "source_locators": [
        "page:6:block:005",
        "page:8:block:005"
      ]
    },
    {
      "witness_key": "work:ref-1",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the two derivations carry the reference entry, its author, title, journal, volume, pages and year, and the recorded gap explains why no citing relation is derived from a reference entry",
      "source_locators": [
        "page:8:block:012",
        "page:8:block:013"
      ]
    },
    {
      "witness_key": "work:ref-10",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the author, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:9:block:007"
      ]
    },
    {
      "witness_key": "work:ref-11",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the author, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:9:block:008"
      ]
    },
    {
      "witness_key": "work:ref-12",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the author, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:9:block:009"
      ]
    },
    {
      "witness_key": "work:ref-13",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the author, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:9:block:010"
      ]
    },
    {
      "witness_key": "work:ref-14",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the entry is split across two blocks and the two derivations together carry the author, title, journal, volume, pages and year",
      "source_locators": [
        "page:9:block:011",
        "page:9:block:012"
      ]
    },
    {
      "witness_key": "work:ref-15",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the author, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:9:block:013"
      ]
    },
    {
      "witness_key": "work:ref-16",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the two derivations carry the chapter, the monograph series, the pages and the identifier and year, and a chapter in an edited series is the projected kind",
      "source_locators": [
        "page:9:block:014",
        "page:9:block:015"
      ]
    },
    {
      "witness_key": "work:ref-17",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the author, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:9:block:016"
      ]
    },
    {
      "witness_key": "work:ref-18",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the entry is split across two blocks and the two derivations together carry the author, title, journal, article number and year",
      "source_locators": [
        "page:9:block:017",
        "page:9:block:018"
      ]
    },
    {
      "witness_key": "work:ref-19",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the author, title, journal, volume, pages and year, which the reading spaces out letter by letter",
      "source_locators": [
        "page:9:block:019"
      ]
    },
    {
      "witness_key": "work:ref-2",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the author, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:8:block:014"
      ]
    },
    {
      "witness_key": "work:ref-20",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the entry is split across two blocks and the two derivations together carry the author, title, journal, volume, pages and year",
      "source_locators": [
        "page:9:block:020",
        "page:9:block:021"
      ]
    },
    {
      "witness_key": "work:ref-21",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, the abstract title, the conference series, the abstract number, the identifier and the year",
      "source_locators": [
        "page:9:block:022"
      ]
    },
    {
      "witness_key": "work:ref-22",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the two derivations carry the cruise reference, its authors and its identifier and year, and the recorded gap explains why the kind is left unset",
      "source_locators": [
        "page:9:block:023",
        "page:9:block:024"
      ]
    },
    {
      "witness_key": "work:ref-23",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the entry is split across two blocks and the two derivations together carry the authors, title, journal, volume, pages and year",
      "source_locators": [
        "page:9:block:025",
        "page:9:block:026"
      ]
    },
    {
      "witness_key": "work:ref-24",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the entry is split across two blocks and the two derivations together carry the authors, title, journal, volume, pages and year",
      "source_locators": [
        "page:9:block:027",
        "page:9:block:028"
      ]
    },
    {
      "witness_key": "work:ref-25",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, the chapter title, the book it appears in, the pages and the year",
      "source_locators": [
        "page:9:block:029"
      ]
    },
    {
      "witness_key": "work:ref-26",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:9:block:030"
      ]
    },
    {
      "witness_key": "work:ref-27",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, the resource it appears in, the pages, the identifier and the year",
      "source_locators": [
        "page:9:block:031"
      ]
    },
    {
      "witness_key": "work:ref-28",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the entry is split across two blocks and the two derivations together carry the authors, title, journal, volume, pages and year",
      "source_locators": [
        "page:9:block:031",
        "page:9:block:032"
      ]
    },
    {
      "witness_key": "work:ref-29",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:9:block:033"
      ]
    },
    {
      "witness_key": "work:ref-3",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:8:block:015"
      ]
    },
    {
      "witness_key": "work:ref-30",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:9:block:034"
      ]
    },
    {
      "witness_key": "work:ref-31",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:9:block:035"
      ]
    },
    {
      "witness_key": "work:ref-32",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, article number and year the row projects",
      "source_locators": [
        "page:9:block:036"
      ]
    },
    {
      "witness_key": "work:ref-33",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the entry is split across two blocks and the two derivations together carry the authors, title, journal, volume, pages and year",
      "source_locators": [
        "page:9:block:037",
        "page:9:block:038"
      ]
    },
    {
      "witness_key": "work:ref-34",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:9:block:039"
      ]
    },
    {
      "witness_key": "work:ref-35",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, article number and year the row projects",
      "source_locators": [
        "page:9:block:040"
      ]
    },
    {
      "witness_key": "work:ref-36",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, article number and year the row projects",
      "source_locators": [
        "page:9:block:041"
      ]
    },
    {
      "witness_key": "work:ref-37",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the author, title, journal, volume, article number and year the row projects",
      "source_locators": [
        "page:9:block:042"
      ]
    },
    {
      "witness_key": "work:ref-38",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, article number and year the row projects",
      "source_locators": [
        "page:9:block:043"
      ]
    },
    {
      "witness_key": "work:ref-39",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the entry is split across two blocks and the two derivations together carry the authors, title, journal, volume, article number and year",
      "source_locators": [
        "page:9:block:044",
        "page:9:block:045"
      ]
    },
    {
      "witness_key": "work:ref-4",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, page and year the row projects",
      "source_locators": [
        "page:8:block:016"
      ]
    },
    {
      "witness_key": "work:ref-40",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the entry is split across two blocks and the two derivations together carry the authors, title, journal, volume, article number and year",
      "source_locators": [
        "page:9:block:046",
        "page:9:block:047"
      ]
    },
    {
      "witness_key": "work:ref-41",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:9:block:048"
      ]
    },
    {
      "witness_key": "work:ref-42",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:9:block:049"
      ]
    },
    {
      "witness_key": "work:ref-43",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, article number and year the row projects",
      "source_locators": [
        "page:9:block:050"
      ]
    },
    {
      "witness_key": "work:ref-44",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:9:block:051"
      ]
    },
    {
      "witness_key": "work:ref-45",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:9:block:052"
      ]
    },
    {
      "witness_key": "work:ref-46",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the entry is split across two blocks and the two derivations together carry the authors, title, journal, volume, pages and year",
      "source_locators": [
        "page:9:block:053",
        "page:9:block:054"
      ]
    },
    {
      "witness_key": "work:ref-47",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:9:block:055"
      ]
    },
    {
      "witness_key": "work:ref-48",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the entry runs across the page break and the two derivations together carry the authors, the full title, the journal, volume, pages and year",
      "source_locators": [
        "page:9:block:056",
        "page:10:block:001"
      ]
    },
    {
      "witness_key": "work:ref-49",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the author, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:10:block:002"
      ]
    },
    {
      "witness_key": "work:ref-5",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:8:block:017"
      ]
    },
    {
      "witness_key": "work:ref-50",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:10:block:003"
      ]
    },
    {
      "witness_key": "work:ref-51",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the entry is split across two blocks and the two derivations together carry the authors, title, journal, volume, pages and year",
      "source_locators": [
        "page:10:block:004",
        "page:10:block:005"
      ]
    },
    {
      "witness_key": "work:ref-52",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the entry is split across two blocks and the two derivations together carry the authors, title, journal, volume, article number and year",
      "source_locators": [
        "page:10:block:006",
        "page:10:block:007"
      ]
    },
    {
      "witness_key": "work:ref-53",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:10:block:008"
      ]
    },
    {
      "witness_key": "work:ref-54",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:10:block:009"
      ]
    },
    {
      "witness_key": "work:ref-55",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:10:block:010"
      ]
    },
    {
      "witness_key": "work:ref-56",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:10:block:011"
      ]
    },
    {
      "witness_key": "work:ref-57",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:10:block:012"
      ]
    },
    {
      "witness_key": "work:ref-58",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the entry is split across two blocks and the two derivations together carry the authors, title, journal, volume, pages and year",
      "source_locators": [
        "page:10:block:013",
        "page:10:block:014"
      ]
    },
    {
      "witness_key": "work:ref-59",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:10:block:015"
      ]
    },
    {
      "witness_key": "work:ref-6",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the entry is split across two blocks and the two derivations together carry the authors, title, journal, volume, page and year",
      "source_locators": [
        "page:9:block:001",
        "page:9:block:002"
      ]
    },
    {
      "witness_key": "work:ref-60",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:10:block:016"
      ]
    },
    {
      "witness_key": "work:ref-61",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, article number and year the row projects",
      "source_locators": [
        "page:10:block:017"
      ]
    },
    {
      "witness_key": "work:ref-62",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:10:block:018"
      ]
    },
    {
      "witness_key": "work:ref-63",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:10:block:019"
      ]
    },
    {
      "witness_key": "work:ref-64",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, article number and year the row projects",
      "source_locators": [
        "page:10:block:020"
      ]
    },
    {
      "witness_key": "work:ref-65",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:10:block:021"
      ]
    },
    {
      "witness_key": "work:ref-66",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the entry is split across two blocks and the two derivations together carry the authors, title, journal, volume, pages and year",
      "source_locators": [
        "page:10:block:022",
        "page:10:block:023"
      ]
    },
    {
      "witness_key": "work:ref-67",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, article number and year the row projects",
      "source_locators": [
        "page:10:block:024"
      ]
    },
    {
      "witness_key": "work:ref-68",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the author, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:10:block:025"
      ]
    },
    {
      "witness_key": "work:ref-69",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:10:block:026"
      ]
    },
    {
      "witness_key": "work:ref-7",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the entry is split across two blocks and the two derivations together carry the authors, the chapter title, the series, the pages, the identifier and the year",
      "source_locators": [
        "page:9:block:003",
        "page:9:block:004"
      ]
    },
    {
      "witness_key": "work:ref-70",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the entry is split across two blocks and the two derivations together carry the authors, title, journal, volume, pages and year",
      "source_locators": [
        "page:10:block:027",
        "page:10:block:028"
      ]
    },
    {
      "witness_key": "work:ref-71",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the author, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:10:block:029"
      ]
    },
    {
      "witness_key": "work:ref-72",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:10:block:030"
      ]
    },
    {
      "witness_key": "work:ref-73",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the three derivations carry the authors, the title and the address the record joins from the two blocks the reading splits it across, with the year",
      "source_locators": [
        "page:10:block:031",
        "page:10:block:032",
        "page:10:block:033"
      ]
    },
    {
      "witness_key": "work:ref-74",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, article number and year the row projects",
      "source_locators": [
        "page:10:block:034"
      ]
    },
    {
      "witness_key": "work:ref-75",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the entry is split across two blocks and the two derivations together carry the authors, title, journal, volume, identifier and year",
      "source_locators": [
        "page:10:block:035",
        "page:10:block:036"
      ]
    },
    {
      "witness_key": "work:ref-76",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:10:block:037"
      ]
    },
    {
      "witness_key": "work:ref-77",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the entry is split across two blocks and the two derivations together carry the authors, title, journal, volume, pages and year",
      "source_locators": [
        "page:10:block:038",
        "page:10:block:039"
      ]
    },
    {
      "witness_key": "work:ref-78",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:10:block:040"
      ]
    },
    {
      "witness_key": "work:ref-79",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the entry is split across two blocks and the two derivations together carry the authors, title, journal, volume, pages and year",
      "source_locators": [
        "page:10:block:041",
        "page:10:block:042"
      ]
    },
    {
      "witness_key": "work:ref-8",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the author, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:9:block:005"
      ]
    },
    {
      "witness_key": "work:ref-9",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited reference entry carries the authors, title, journal, volume, pages and year the row projects",
      "source_locators": [
        "page:9:block:006"
      ]
    },
    {
      "witness_key": "work:reprints",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the reprints information and gives its address",
      "source_locators": [
        "page:11:block:004"
      ]
    },
    {
      "witness_key": "work:self",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the derivations carry the title, the author line, the identifier, the licence sentence and the running header with journal, volume, article number and year, so every projected field of the article itself is cited, and the recorded gap explains why the superscript affiliations yield no relation",
      "source_locators": [
        "page:1:block:001",
        "page:1:block:006",
        "page:11:block:001",
        "page:11:block:003",
        "page:11:block:005",
        "page:11:block:006",
        "page:10:block:048",
        "page:2:block:008",
        "page:3:block:006",
        "page:4:block:008",
        "page:5:block:011",
        "page:6:block:006",
        "page:7:block:013",
        "page:8:block:018",
        "page:9:block:056"
      ]
    },
    {
      "witness_key": "work:supplementary",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the supplementary information and gives its address",
      "source_locators": [
        "page:11:block:001"
      ]
    },
    {
      "witness_key": "work:zenodo",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the database the catalogue was deposited in",
      "source_locators": [
        "page:8:block:008"
      ]
    },
    {
      "witness_key": "rel:askja-in-iceland",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the cited sentence places the volcano in the island country, and both endpoints are named in that same block",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "rel:fagradalsfjall-in-iceland",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the same sentence places the peninsula in the island country and names both endpoints",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "rel:logachev-of-knipovich",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the cited sentence names the seamount of that ridge, which is the part-of relation projected, and both endpoints appear in the block",
      "source_locators": [
        "page:8:block:004"
      ]
    },
    {
      "witness_key": "rel:mar-in-eq-atlantic",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the cited sentence places the ridge in the ocean region and names both endpoints",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "rel:marseg-bounded-chain",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the cited sentence puts the segment between the two transform faults, which bounds it by the one this row names",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "rel:marseg-bounded-romanche",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the same sentence bounds the segment by the other transform fault it names",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "rel:mayotte-in-indian-ocean",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the cited sentence places the island in the ocean region and names both endpoints",
      "source_locators": [
        "page:4:block:002"
      ]
    },
    {
      "witness_key": "rel:occ-on-mar",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the cited caption sentence puts the core complex on the outside corner of the ridge and names both endpoints",
      "source_locators": [
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "rel:rc1-bounded-detachment",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the cited sentence bounds the intersection segment by the detachment fault, and the same block gives the segment the name this row uses",
      "source_locators": [
        "page:1:block:005"
      ]
    },
    {
      "witness_key": "rel:rc2-bounded-faults",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the cited sentence bounds the segment by those inward dipping faults, and the block names both endpoints",
      "source_locators": [
        "page:4:block:001"
      ]
    },
    {
      "witness_key": "rel:romanche-faults-in-tf",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the cited caption sentence places the faults along the transform and names both endpoints",
      "source_locators": [
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "rel:vent-field-on-ntd1",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the cited sentence places the extinct vent field on the eastern flank of the discontinuity and names both endpoints",
      "source_locators": [
        "page:3:block:002"
      ]
    },
    {
      "witness_key": "rel:catalog-in-zenodo",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the cited sentence states the deposit of the catalogue in the named database, and both endpoints are in that block",
      "source_locators": [
        "page:8:block:008"
      ]
    },
    {
      "witness_key": "cruise:smarties",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the derivations name the cruise, the passive seismic experiment conducted during it, the vessel from the reference entry and the identifier, and the recorded gaps explain the unset span and kind",
      "source_locators": [
        "page:2:block:002",
        "page:2:block:007",
        "page:6:block:002",
        "page:9:block:023",
        "page:9:block:024",
        "page:10:block:043",
        "page:10:block:044",
        "page:10:block:046"
      ]
    },
    {
      "witness_key": "instrument:nautile",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited caption sentence names the submersible and the dive observations the projected description repeats",
      "source_locators": [
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "instrument:obs",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the derivations name the instruments in full and give the abbreviation the record keeps as a tag",
      "source_locators": [
        "page:1:block:001",
        "page:2:block:002",
        "page:2:block:007"
      ]
    },
    {
      "witness_key": "instant:accepted",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited line gives the acceptance label and date, and the day precision matches a date given to the day",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "instant:received",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited line gives the receipt label and date, and the day precision matches a date given to the day",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "method:1d-inversion",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names what the program is used for, which is the method name projected",
      "source_locators": [
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "method:catalog-analysis",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the analysis and its two outputs; the record keeps the reading's line-break hyphen inside the name",
      "source_locators": [
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "method:dd-relocation",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the relocation the program performs; the record keeps the reading's line-break hyphen inside the name",
      "source_locators": [
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "method:double-difference",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the relocation method used after the initial locations",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "method:earthquake-location",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names what the code is used for",
      "source_locators": [
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "method:focal-mechanism",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names what the software is used for",
      "source_locators": [
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "method:graphing",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names what the toolbox is used for",
      "source_locators": [
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "method:local-magnitude",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the magnitude scale used, and the recorded gap explains why the formula itself is left unformalized",
      "source_locators": [
        "page:8:block:002"
      ]
    },
    {
      "witness_key": "method:nonlinear-location",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the algorithm used to obtain the hypocentres",
      "source_locators": [
        "page:2:block:002"
      ]
    },
    {
      "witness_key": "method:oct-tree",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the search algorithm of the location program",
      "source_locators": [
        "page:7:block:004"
      ]
    },
    {
      "witness_key": "method:phase-picking",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names what the software is used for, and the record keeps that wording",
      "source_locators": [
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "method:sta-lta",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW both derivations name the trigger algorithm used for automatic detection",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ]
    },
    {
      "witness_key": "method:structural-analysis",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names what the mapping program is used for",
      "source_locators": [
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "software:global-mapper",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the program and gives the address where it is available",
      "source_locators": [
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "software:gmt",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the two derivations name the toolbox and carry the two halves of the address the reading splits across a block boundary",
      "source_locators": [
        "page:8:block:010",
        "page:8:block:011"
      ]
    },
    {
      "witness_key": "software:hash",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the derivations name the package, its version and the address where it is available",
      "source_locators": [
        "page:8:block:003",
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "software:hypodd",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the derivations name the program, its version and the address where it is available",
      "source_locators": [
        "page:7:block:006",
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "software:nonlinloc",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the derivations name the program and give the address where the code is available",
      "source_locators": [
        "page:7:block:004",
        "page:7:block:007",
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "software:seisan",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the derivations name the package and give the address where it is available",
      "source_locators": [
        "page:6:block:002",
        "page:8:block:002",
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "software:velest",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the derivations name the program and give the address where it is available",
      "source_locators": [
        "page:6:block:004",
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "software:zmap",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the derivations name the software and give the address where it is available",
      "source_locators": [
        "page:8:block:002",
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "rel:globalmapper-used-for-structural",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the cited sentence says the program is used for that analysis and names both endpoints",
      "source_locators": [
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "rel:gmt-used-for-graphing",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the cited sentence says the toolbox is used for graphing and names both endpoints",
      "source_locators": [
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "rel:hash-used-for-fm",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the cited sentence says the software is used for determining the solutions and names both endpoints",
      "source_locators": [
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "rel:hypodd-used-for-relocation",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the cited sentence says the program is used for that relocation and names both endpoints",
      "source_locators": [
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "rel:nonlinloc-used-for-octtree",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the cited sentence ties the search algorithm to the program and names both endpoints",
      "source_locators": [
        "page:7:block:004"
      ]
    },
    {
      "witness_key": "rel:seisan-used-for-picking",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the cited sentence says the software is used to pick phases and names both endpoints",
      "source_locators": [
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "rel:seisan-used-for-stalta",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the cited sentence puts the trigger algorithm within that package and names both endpoints",
      "source_locators": [
        "page:6:block:002"
      ]
    },
    {
      "witness_key": "rel:velest-used-for-inversion",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the cited sentence says the program is used for inverting the model and names both endpoints",
      "source_locators": [
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "rel:zmap-used-for-catalog",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the cited sentence says the software is used for that analysis and names both endpoints",
      "source_locators": [
        "page:8:block:010"
      ]
    },
    {
      "witness_key": "award:erc-advanced",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited funding sentence names the grant and its agreement number, and the recorded gap explains why three other awards yield no relation",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "award:fp7",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited funding sentence names the framework programme with its span",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "award:investissements",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited funding sentence names the programme",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "award:isblue",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited funding sentence names the project, the graduate school and the grant number, which the record carries with the reading's line-break dash removed",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "award:nsfc",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited funding sentence gives the two grant numbers of that foundation",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "award:sad",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited funding sentence names the programme of the regional council",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "award:zjnsf",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited funding sentence gives the grant number of that provincial foundation",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "agent:briais",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited author line names this person, and the recorded gap explains why the superscript affiliation yields no relation",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "agent:brunelli",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited author line names this person",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "agent:cartigny",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited acknowledgement sentence names this person",
      "source_locators": [
        "page:10:block:043"
      ]
    },
    {
      "witness_key": "agent:geli",
      "source_support": "PARTIAL",
      "rationale": "NO_SUBJECT_IN_ROW the cited block carries the surname but the initial the record projects is in the preceding block, which the sentence runs on from and which this record does not cite",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "agent:grenet",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited author line names this person",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "agent:hamelin",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited author line names this person",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "agent:maia",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited author line names this person",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "agent:petracchini",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited author line names this person",
      "source_locators": [
        "page:1:block:001"
      ]
    },
    {
      "witness_key": "agent:singh",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the author line and the correspondence sentence name this person and the e-mail line gives the address the record projects",
      "source_locators": [
        "page:1:block:001",
        "page:1:block:006",
        "page:10:block:044",
        "page:11:block:002"
      ]
    },
    {
      "witness_key": "agent:wang",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited acknowledgement sentence names this person, with the reading's letter spacing",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "agent:yang",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited acknowledgement sentence names this person, with the reading's letter spacing",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "agent:yu",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the author line and the correspondence sentence name this person and the e-mail line gives the address the record projects",
      "source_locators": [
        "page:1:block:001",
        "page:1:block:006",
        "page:10:block:044",
        "page:11:block:002"
      ]
    },
    {
      "witness_key": "org:brittany",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited funding sentence names this body",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "org:cnr-igag",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited affiliation line names this institute with the city and country the projected description repeats, and the recorded gap explains the affiliation that names no institution",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "org:erc",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited funding sentence names this body",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "org:eu",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited funding sentence names this body",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "org:french-government",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited funding sentence names this body",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "org:geo-ocean",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited affiliation line names this unit with the place the projected description repeats",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "org:ipgp",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited affiliation line names this institute with the university and place, and the contribution sentence gives the abbreviation kept as a tag",
      "source_locators": [
        "page:1:block:006",
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "org:nsfc",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited funding sentence names this foundation",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "org:sio",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited affiliation line names this institute with the laboratory, ministry and place the projected description repeats",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "org:tgir",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the fleet that funded the shipping time",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "org:unimore",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited affiliation line names this university with the department and place the projected description repeats",
      "source_locators": [
        "page:1:block:006"
      ]
    },
    {
      "witness_key": "org:zjnsf",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited funding sentence names this foundation",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "rel:singh-funded-erc",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the cited funding sentence attributes that grant to this author by his initials, and both endpoints are in the block",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "rel:singh-funded-fp7",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the same sentence attributes the framework programme funding to this author by his initials",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "rel:yu-funded-nsfc",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the cited funding sentence attributes the two grant numbers to this author by his initials, and both endpoints are in the block",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "rel:yu-funded-zjnsf",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the same sentence attributes the provincial grant to this author by his initials",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "rel:yu-funded-nsfc-body",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the same sentence names the funding body and the funded author, which is the relation this row projects",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "rel:yu-funded-zjnsf-body",
      "source_support": "SUPPORTED",
      "rationale": "DERIVATION_LOCAL the same sentence names the provincial funding body and the funded author",
      "source_locators": [
        "page:10:block:044"
      ]
    },
    {
      "witness_key": "model:co2-solubility",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the solubility model used for the saturation calculation",
      "source_locators": [
        "page:5:block:006"
      ]
    },
    {
      "witness_key": "model:iacono-marziano",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the model the theoretical solubility was calculated from and what it computes",
      "source_locators": [
        "page:8:block:007"
      ]
    },
    {
      "witness_key": "model:low-velocity",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names this model among the five and says where it applies",
      "source_locators": [
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "model:minimum-1d",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the model searched for with that program",
      "source_locators": [
        "page:6:block:004"
      ]
    },
    {
      "witness_key": "model:model-1",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names the model, calls it the fastest and says where it derives from",
      "source_locators": [
        "page:7:block:009"
      ]
    },
    {
      "witness_key": "model:north-flank",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names this model among the five, and the preceding sentence of the same block gives the kind the record projects",
      "source_locators": [
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "model:selected-1d",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the derivations name the selected model, describe it as the average model across the transform and give the kind",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:003",
        "page:6:block:004"
      ]
    },
    {
      "witness_key": "model:south-flank",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names this model among the five, with the kind given earlier in the same block",
      "source_locators": [
        "page:6:block:003"
      ]
    },
    {
      "witness_key": "model:thermal-model",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited caption sentence names the model the isotherms were extracted from",
      "source_locators": [
        "page:7:block:012"
      ]
    },
    {
      "witness_key": "model:transform-valley",
      "source_support": "SUPPORTED",
      "rationale": "NO_SUBJECT_IN_ROW the cited sentence names this model among the five, with the kind given earlier in the same block",
      "source_locators": [
        "page:6:block:003"
      ]
    }
  ],
  "questions": [
    {
      "question_id": "CQ-T1-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The cruise row names the campaign and states that the OBS passive seismic experiment was conducted during it, and the count row names the instrument network that acquired the microseismicity data; nothing in the result joins the two rows.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "campaign_name",
          "row_index": 0,
          "absent_reason": null,
          "note": "the cruise record's name"
        },
        {
          "semantic": "observing_system",
          "row_index": 10,
          "absent_reason": null,
          "note": "the count scope names the ocean-bottom seismometer network that acquired the microseismicity data"
        },
        {
          "semantic": "data_acquisition",
          "row_index": 0,
          "absent_reason": null,
          "note": "the cruise record's description states the OBS passive seismic experiment conducted during the cruise"
        }
      ],
      "source_locators": [
        "page:2:block:002",
        "page:2:block:007",
        "page:6:block:002",
        "page:9:block:023",
        "page:9:block:024",
        "page:10:block:043",
        "page:10:block:044",
        "page:10:block:046"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "cruise:smarties"
        },
        {
          "row_index": 1,
          "witness_key": "instrument:nautile"
        },
        {
          "row_index": 2,
          "witness_key": "instrument:obs"
        },
        {
          "row_index": 3,
          "witness_key": "obs:events-identified-760"
        },
        {
          "row_index": 4,
          "witness_key": "obs:fm-new-3"
        },
        {
          "row_index": 5,
          "witness_key": "obs:fm-previous-3"
        },
        {
          "row_index": 6,
          "witness_key": "obs:fm-total-6"
        },
        {
          "row_index": 7,
          "witness_key": "obs:forced-depth-subset"
        },
        {
          "row_index": 8,
          "witness_key": "obs:located-514"
        },
        {
          "row_index": 9,
          "witness_key": "obs:magnitude-groups"
        },
        {
          "row_index": 10,
          "witness_key": "obs:obs-deployed-19"
        },
        {
          "row_index": 11,
          "witness_key": "obs:obs-useful-17"
        },
        {
          "row_index": 12,
          "witness_key": "obs:quality-categories"
        },
        {
          "row_index": 13,
          "witness_key": "obs:relocated-364"
        },
        {
          "row_index": 14,
          "witness_key": "obs:romanche-2016-subevents"
        },
        {
          "row_index": 15,
          "witness_key": "obs:subsection-count"
        },
        {
          "row_index": 16,
          "witness_key": "obs:velest-subdataset"
        },
        {
          "row_index": 17,
          "witness_key": "obs:velocity-models-five"
        },
        {
          "row_index": 18,
          "witness_key": "obs:well-relocated-276"
        },
        {
          "row_index": 19,
          "witness_key": "obs:abstract-co2-primary"
        },
        {
          "row_index": 20,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 21,
          "witness_key": "obs:eq-atlantic-co2-average"
        },
        {
          "row_index": 22,
          "witness_key": "obs:eq-atlantic-co2-max"
        },
        {
          "row_index": 23,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 24,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 25,
          "witness_key": "obs:axial-event-depth-stable"
        },
        {
          "row_index": 26,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 27,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 28,
          "witness_key": "obs:cluster-depth-west"
        },
        {
          "row_index": 29,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 30,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 31,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 32,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 33,
          "witness_key": "obs:criteria-met-fraction"
        },
        {
          "row_index": 34,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 35,
          "witness_key": "obs:criterion-gap"
        },
        {
          "row_index": 36,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 37,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 38,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 39,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 40,
          "witness_key": "obs:degassing-depth-range"
        },
        {
          "row_index": 41,
          "witness_key": "obs:depth-uncertainty-cap"
        },
        {
          "row_index": 42,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 43,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 44,
          "witness_key": "obs:expected-brittle-thickness"
        },
        {
          "row_index": 45,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 46,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 47,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 48,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 49,
          "witness_key": "obs:fig3e-elevation-scale"
        },
        {
          "row_index": 50,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 51,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 52,
          "witness_key": "obs:fm-gap"
        },
        {
          "row_index": 53,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 54,
          "witness_key": "obs:fm-polarities"
        },
        {
          "row_index": 55,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 56,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 57,
          "witness_key": "obs:forced-depth-range"
        },
        {
          "row_index": 58,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 59,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 60,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 61,
          "witness_key": "obs:horizontal-uncertainty-cap"
        },
        {
          "row_index": 62,
          "witness_key": "obs:lithospheric-age-interval"
        },
        {
          "row_index": 63,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 64,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 65,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 66,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 67,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 68,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 69,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 70,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 71,
          "witness_key": "obs:min-obs-per-event"
        },
        {
          "row_index": 72,
          "witness_key": "obs:model1-depth"
        },
        {
          "row_index": 73,
          "witness_key": "obs:model1-p-velocity"
        },
        {
          "row_index": 74,
          "witness_key": "obs:occ-transect-halfwidth"
        },
        {
          "row_index": 75,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 76,
          "witness_key": "obs:perturbed-deep-events"
        },
        {
          "row_index": 77,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 78,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 79,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 80,
          "witness_key": "obs:quality-a-uncertainty"
        },
        {
          "row_index": 81,
          "witness_key": "obs:quality-b-uncertainty"
        },
        {
          "row_index": 82,
          "witness_key": "obs:quality-c-uncertainty"
        },
        {
          "row_index": 83,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 84,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 85,
          "witness_key": "obs:refraction-constraint-depth"
        },
        {
          "row_index": 86,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 87,
          "witness_key": "obs:relocation-iterations"
        },
        {
          "row_index": 88,
          "witness_key": "obs:relocation-obs-count"
        },
        {
          "row_index": 89,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 90,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 91,
          "witness_key": "obs:rms-residual-cap"
        },
        {
          "row_index": 92,
          "witness_key": "obs:solubility-temperature"
        },
        {
          "row_index": 93,
          "witness_key": "obs:station-gap-cap"
        },
        {
          "row_index": 94,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 95,
          "witness_key": "obs:subdataset-arrivals"
        },
        {
          "row_index": 96,
          "witness_key": "obs:subdataset-gap"
        },
        {
          "row_index": 97,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 98,
          "witness_key": "obs:velest-iterations"
        },
        {
          "row_index": 99,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 100,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 101,
          "witness_key": "obs:obs-no-data"
        },
        {
          "row_index": 102,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 103,
          "witness_key": "obs:mar-events-317"
        },
        {
          "row_index": 104,
          "witness_key": "obs:romanche-events-197"
        },
        {
          "row_index": 105,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 106,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 107,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 108,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 109,
          "witness_key": "obs:co2-calc-rc2"
        },
        {
          "row_index": 110,
          "witness_key": "obs:co2-calc-rc3"
        },
        {
          "row_index": 111,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 112,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 113,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 114,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 115,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 116,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 117,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 118,
          "witness_key": "obs:rc2-ba"
        },
        {
          "row_index": 119,
          "witness_key": "obs:rc2-rb"
        },
        {
          "row_index": 120,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 121,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 122,
          "witness_key": "obs:bdb-at-ntd2"
        },
        {
          "row_index": 123,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 124,
          "witness_key": "obs:bdb-isotherm-fig6"
        },
        {
          "row_index": 125,
          "witness_key": "obs:bdb-isotherm-slow"
        },
        {
          "row_index": 126,
          "witness_key": "obs:bdb-isotherms-cold"
        },
        {
          "row_index": 127,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 128,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 129,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 130,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 131,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 132,
          "witness_key": "obs:deep-eq-rc2-1619"
        },
        {
          "row_index": 133,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 134,
          "witness_key": "obs:depth-range-ntd2"
        },
        {
          "row_index": 135,
          "witness_key": "obs:depth-range-occ"
        },
        {
          "row_index": 136,
          "witness_key": "obs:hot-mantle-temperature"
        },
        {
          "row_index": 137,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 138,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 139,
          "witness_key": "obs:mantle-temperature-rc2"
        },
        {
          "row_index": 140,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 141,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 142,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 143,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 144,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 145,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 146,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 147,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 148,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 149,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 150,
          "witness_key": "obs:subsolidus-temperature"
        },
        {
          "row_index": 151,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 152,
          "witness_key": "obs:vp-vs-test-range"
        }
      ]
    },
    {
      "question_id": "CQ-T1-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The count row carries the number and names the network, and the cruise row carries the deployment during which that network was put in place; nothing in the result joins them.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "instrument_count",
          "row_index": 10,
          "absent_reason": null,
          "note": "the count of ocean-bottom seismometers"
        },
        {
          "semantic": "observing_system",
          "row_index": 10,
          "absent_reason": null,
          "note": "the count scope names the network that acquired the microseismicity data"
        },
        {
          "semantic": "deployment_event",
          "row_index": 0,
          "absent_reason": null,
          "note": "the cruise record's description states the OBS passive seismic experiment conducted during the 2019 cruise"
        }
      ],
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002",
        "page:2:block:007",
        "page:9:block:023",
        "page:9:block:024",
        "page:10:block:043",
        "page:10:block:044",
        "page:10:block:046"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "cruise:smarties"
        },
        {
          "row_index": 1,
          "witness_key": "instrument:nautile"
        },
        {
          "row_index": 2,
          "witness_key": "instrument:obs"
        },
        {
          "row_index": 3,
          "witness_key": "obs:events-identified-760"
        },
        {
          "row_index": 4,
          "witness_key": "obs:fm-new-3"
        },
        {
          "row_index": 5,
          "witness_key": "obs:fm-previous-3"
        },
        {
          "row_index": 6,
          "witness_key": "obs:fm-total-6"
        },
        {
          "row_index": 7,
          "witness_key": "obs:forced-depth-subset"
        },
        {
          "row_index": 8,
          "witness_key": "obs:located-514"
        },
        {
          "row_index": 9,
          "witness_key": "obs:magnitude-groups"
        },
        {
          "row_index": 10,
          "witness_key": "obs:obs-deployed-19"
        },
        {
          "row_index": 11,
          "witness_key": "obs:obs-useful-17"
        },
        {
          "row_index": 12,
          "witness_key": "obs:quality-categories"
        },
        {
          "row_index": 13,
          "witness_key": "obs:relocated-364"
        },
        {
          "row_index": 14,
          "witness_key": "obs:romanche-2016-subevents"
        },
        {
          "row_index": 15,
          "witness_key": "obs:subsection-count"
        },
        {
          "row_index": 16,
          "witness_key": "obs:velest-subdataset"
        },
        {
          "row_index": 17,
          "witness_key": "obs:velocity-models-five"
        },
        {
          "row_index": 18,
          "witness_key": "obs:well-relocated-276"
        },
        {
          "row_index": 19,
          "witness_key": "obs:abstract-co2-primary"
        },
        {
          "row_index": 20,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 21,
          "witness_key": "obs:eq-atlantic-co2-average"
        },
        {
          "row_index": 22,
          "witness_key": "obs:eq-atlantic-co2-max"
        },
        {
          "row_index": 23,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 24,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 25,
          "witness_key": "obs:axial-event-depth-stable"
        },
        {
          "row_index": 26,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 27,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 28,
          "witness_key": "obs:cluster-depth-west"
        },
        {
          "row_index": 29,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 30,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 31,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 32,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 33,
          "witness_key": "obs:criteria-met-fraction"
        },
        {
          "row_index": 34,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 35,
          "witness_key": "obs:criterion-gap"
        },
        {
          "row_index": 36,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 37,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 38,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 39,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 40,
          "witness_key": "obs:degassing-depth-range"
        },
        {
          "row_index": 41,
          "witness_key": "obs:depth-uncertainty-cap"
        },
        {
          "row_index": 42,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 43,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 44,
          "witness_key": "obs:expected-brittle-thickness"
        },
        {
          "row_index": 45,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 46,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 47,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 48,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 49,
          "witness_key": "obs:fig3e-elevation-scale"
        },
        {
          "row_index": 50,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 51,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 52,
          "witness_key": "obs:fm-gap"
        },
        {
          "row_index": 53,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 54,
          "witness_key": "obs:fm-polarities"
        },
        {
          "row_index": 55,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 56,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 57,
          "witness_key": "obs:forced-depth-range"
        },
        {
          "row_index": 58,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 59,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 60,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 61,
          "witness_key": "obs:horizontal-uncertainty-cap"
        },
        {
          "row_index": 62,
          "witness_key": "obs:lithospheric-age-interval"
        },
        {
          "row_index": 63,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 64,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 65,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 66,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 67,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 68,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 69,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 70,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 71,
          "witness_key": "obs:min-obs-per-event"
        },
        {
          "row_index": 72,
          "witness_key": "obs:model1-depth"
        },
        {
          "row_index": 73,
          "witness_key": "obs:model1-p-velocity"
        },
        {
          "row_index": 74,
          "witness_key": "obs:occ-transect-halfwidth"
        },
        {
          "row_index": 75,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 76,
          "witness_key": "obs:perturbed-deep-events"
        },
        {
          "row_index": 77,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 78,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 79,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 80,
          "witness_key": "obs:quality-a-uncertainty"
        },
        {
          "row_index": 81,
          "witness_key": "obs:quality-b-uncertainty"
        },
        {
          "row_index": 82,
          "witness_key": "obs:quality-c-uncertainty"
        },
        {
          "row_index": 83,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 84,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 85,
          "witness_key": "obs:refraction-constraint-depth"
        },
        {
          "row_index": 86,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 87,
          "witness_key": "obs:relocation-iterations"
        },
        {
          "row_index": 88,
          "witness_key": "obs:relocation-obs-count"
        },
        {
          "row_index": 89,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 90,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 91,
          "witness_key": "obs:rms-residual-cap"
        },
        {
          "row_index": 92,
          "witness_key": "obs:solubility-temperature"
        },
        {
          "row_index": 93,
          "witness_key": "obs:station-gap-cap"
        },
        {
          "row_index": 94,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 95,
          "witness_key": "obs:subdataset-arrivals"
        },
        {
          "row_index": 96,
          "witness_key": "obs:subdataset-gap"
        },
        {
          "row_index": 97,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 98,
          "witness_key": "obs:velest-iterations"
        },
        {
          "row_index": 99,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 100,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 101,
          "witness_key": "obs:obs-no-data"
        },
        {
          "row_index": 102,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 103,
          "witness_key": "obs:mar-events-317"
        },
        {
          "row_index": 104,
          "witness_key": "obs:romanche-events-197"
        },
        {
          "row_index": 105,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 106,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 107,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 108,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 109,
          "witness_key": "obs:co2-calc-rc2"
        },
        {
          "row_index": 110,
          "witness_key": "obs:co2-calc-rc3"
        },
        {
          "row_index": 111,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 112,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 113,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 114,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 115,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 116,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 117,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 118,
          "witness_key": "obs:rc2-ba"
        },
        {
          "row_index": 119,
          "witness_key": "obs:rc2-rb"
        },
        {
          "row_index": 120,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 121,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 122,
          "witness_key": "obs:bdb-at-ntd2"
        },
        {
          "row_index": 123,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 124,
          "witness_key": "obs:bdb-isotherm-fig6"
        },
        {
          "row_index": 125,
          "witness_key": "obs:bdb-isotherm-slow"
        },
        {
          "row_index": 126,
          "witness_key": "obs:bdb-isotherms-cold"
        },
        {
          "row_index": 127,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 128,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 129,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 130,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 131,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 132,
          "witness_key": "obs:deep-eq-rc2-1619"
        },
        {
          "row_index": 133,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 134,
          "witness_key": "obs:depth-range-ntd2"
        },
        {
          "row_index": 135,
          "witness_key": "obs:depth-range-occ"
        },
        {
          "row_index": 136,
          "witness_key": "obs:hot-mantle-temperature"
        },
        {
          "row_index": 137,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 138,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 139,
          "witness_key": "obs:mantle-temperature-rc2"
        },
        {
          "row_index": 140,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 141,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 142,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 143,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 144,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 145,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 146,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 147,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 148,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 149,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 150,
          "witness_key": "obs:subsolidus-temperature"
        },
        {
          "row_index": 151,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 152,
          "witness_key": "obs:vp-vs-test-range"
        }
      ]
    },
    {
      "question_id": "CQ-T1-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The article record carries the publication record and the instant row carries both the acceptance event and its date; no returned relation joins them.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "publication_record",
          "row_index": 85,
          "absent_reason": null,
          "note": "the article record with its journal, volume, article number, year and identifier"
        },
        {
          "semantic": "acceptance_event",
          "row_index": 0,
          "absent_reason": null,
          "note": "the instant record named Accepted"
        },
        {
          "semantic": "calendar_date",
          "row_index": 0,
          "absent_reason": null,
          "note": "the same row's date, to day precision"
        }
      ],
      "source_locators": [
        "page:1:block:001",
        "page:1:block:006",
        "page:11:block:001",
        "page:11:block:003",
        "page:11:block:005",
        "page:11:block:006",
        "page:10:block:048",
        "page:2:block:008",
        "page:3:block:006",
        "page:4:block:008",
        "page:5:block:011",
        "page:6:block:006",
        "page:7:block:013",
        "page:8:block:018",
        "page:9:block:056"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "instant:accepted"
        },
        {
          "row_index": 1,
          "witness_key": "instant:received"
        },
        {
          "row_index": 2,
          "witness_key": "work:cruise-data"
        },
        {
          "row_index": 3,
          "witness_key": "work:earthquake-catalog"
        },
        {
          "row_index": 4,
          "witness_key": "work:petdb"
        },
        {
          "row_index": 5,
          "witness_key": "work:ref-1"
        },
        {
          "row_index": 6,
          "witness_key": "work:ref-10"
        },
        {
          "row_index": 7,
          "witness_key": "work:ref-11"
        },
        {
          "row_index": 8,
          "witness_key": "work:ref-12"
        },
        {
          "row_index": 9,
          "witness_key": "work:ref-13"
        },
        {
          "row_index": 10,
          "witness_key": "work:ref-14"
        },
        {
          "row_index": 11,
          "witness_key": "work:ref-15"
        },
        {
          "row_index": 12,
          "witness_key": "work:ref-16"
        },
        {
          "row_index": 13,
          "witness_key": "work:ref-17"
        },
        {
          "row_index": 14,
          "witness_key": "work:ref-18"
        },
        {
          "row_index": 15,
          "witness_key": "work:ref-19"
        },
        {
          "row_index": 16,
          "witness_key": "work:ref-2"
        },
        {
          "row_index": 17,
          "witness_key": "work:ref-20"
        },
        {
          "row_index": 18,
          "witness_key": "work:ref-21"
        },
        {
          "row_index": 19,
          "witness_key": "work:ref-22"
        },
        {
          "row_index": 20,
          "witness_key": "work:ref-23"
        },
        {
          "row_index": 21,
          "witness_key": "work:ref-24"
        },
        {
          "row_index": 22,
          "witness_key": "work:ref-25"
        },
        {
          "row_index": 23,
          "witness_key": "work:ref-26"
        },
        {
          "row_index": 24,
          "witness_key": "work:ref-27"
        },
        {
          "row_index": 25,
          "witness_key": "work:ref-28"
        },
        {
          "row_index": 26,
          "witness_key": "work:ref-29"
        },
        {
          "row_index": 27,
          "witness_key": "work:ref-3"
        },
        {
          "row_index": 28,
          "witness_key": "work:ref-30"
        },
        {
          "row_index": 29,
          "witness_key": "work:ref-31"
        },
        {
          "row_index": 30,
          "witness_key": "work:ref-32"
        },
        {
          "row_index": 31,
          "witness_key": "work:ref-33"
        },
        {
          "row_index": 32,
          "witness_key": "work:ref-34"
        },
        {
          "row_index": 33,
          "witness_key": "work:ref-35"
        },
        {
          "row_index": 34,
          "witness_key": "work:ref-36"
        },
        {
          "row_index": 35,
          "witness_key": "work:ref-37"
        },
        {
          "row_index": 36,
          "witness_key": "work:ref-38"
        },
        {
          "row_index": 37,
          "witness_key": "work:ref-39"
        },
        {
          "row_index": 38,
          "witness_key": "work:ref-4"
        },
        {
          "row_index": 39,
          "witness_key": "work:ref-40"
        },
        {
          "row_index": 40,
          "witness_key": "work:ref-41"
        },
        {
          "row_index": 41,
          "witness_key": "work:ref-42"
        },
        {
          "row_index": 42,
          "witness_key": "work:ref-43"
        },
        {
          "row_index": 43,
          "witness_key": "work:ref-44"
        },
        {
          "row_index": 44,
          "witness_key": "work:ref-45"
        },
        {
          "row_index": 45,
          "witness_key": "work:ref-46"
        },
        {
          "row_index": 46,
          "witness_key": "work:ref-47"
        },
        {
          "row_index": 47,
          "witness_key": "work:ref-48"
        },
        {
          "row_index": 48,
          "witness_key": "work:ref-49"
        },
        {
          "row_index": 49,
          "witness_key": "work:ref-5"
        },
        {
          "row_index": 50,
          "witness_key": "work:ref-50"
        },
        {
          "row_index": 51,
          "witness_key": "work:ref-51"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref-52"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref-53"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref-54"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref-55"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref-56"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref-57"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref-58"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref-59"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref-6"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref-60"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref-61"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref-62"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref-63"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref-64"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref-65"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref-66"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref-67"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref-68"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref-69"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref-7"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref-70"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref-71"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref-72"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref-73"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref-74"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref-75"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref-76"
        },
        {
          "row_index": 79,
          "witness_key": "work:ref-77"
        },
        {
          "row_index": 80,
          "witness_key": "work:ref-78"
        },
        {
          "row_index": 81,
          "witness_key": "work:ref-79"
        },
        {
          "row_index": 82,
          "witness_key": "work:ref-8"
        },
        {
          "row_index": 83,
          "witness_key": "work:ref-9"
        },
        {
          "row_index": 84,
          "witness_key": "work:reprints"
        },
        {
          "row_index": 85,
          "witness_key": "work:self"
        },
        {
          "row_index": 86,
          "witness_key": "work:supplementary"
        },
        {
          "row_index": 87,
          "witness_key": "work:zenodo"
        },
        {
          "row_index": 88,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 89,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 90,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 91,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 92,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 93,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 94,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 95,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 96,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 97,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 98,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 99,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 100,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 101,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 102,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 103,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 104,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 105,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 106,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 107,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 108,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 109,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 110,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 111,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 112,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 113,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 114,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 115,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 116,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 117,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 118,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 119,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 120,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 121,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 122,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 123,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 124,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 125,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 126,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 127,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 128,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 129,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 130,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 131,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 132,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 133,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 134,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 135,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 136,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 137,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 138,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 139,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 140,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 141,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 142,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 143,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 144,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 145,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 146,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 147,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 148,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 149,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 150,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 151,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 152,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 153,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 154,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 155,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 156,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 157,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 158,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 159,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 160,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 161,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 162,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 163,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 164,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 165,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 166,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 167,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 168,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 169,
          "witness_key": "claim:s-wave-delays-removed"
        },
        {
          "row_index": 170,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 171,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 172,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 173,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 174,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 175,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 176,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 177,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 178,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 179,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 180,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 181,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 182,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 183,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 184,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 185,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 186,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 187,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 188,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 189,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 190,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 191,
          "witness_key": "rel:catalog-in-zenodo"
        },
        {
          "row_index": 192,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 193,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 194,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 195,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 196,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 197,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 198,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 199,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 200,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 201,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 202,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 203,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 204,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 205,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 206,
          "witness_key": "claim:vp-vs-reasonable"
        }
      ]
    },
    {
      "question_id": "CQ-T1-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The dataset row carries the record and its identifier, the repository row carries the name, and a returned relation joins the two.",
      "assembly": "LINKED_ROWS",
      "coverage": [
        {
          "semantic": "dataset_record",
          "row_index": 1,
          "absent_reason": null,
          "note": "the deposited catalogue and picked arrivals"
        },
        {
          "semantic": "repository_name",
          "row_index": 85,
          "absent_reason": null,
          "note": "the repository record the dataset was deposited in"
        },
        {
          "semantic": "persistent_identifier",
          "row_index": 1,
          "absent_reason": null,
          "note": "the dataset row's identifier"
        }
      ],
      "source_locators": [
        "page:8:block:008",
        "page:8:block:009"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "work:cruise-data"
        },
        {
          "row_index": 1,
          "witness_key": "work:earthquake-catalog"
        },
        {
          "row_index": 2,
          "witness_key": "work:petdb"
        },
        {
          "row_index": 3,
          "witness_key": "work:ref-1"
        },
        {
          "row_index": 4,
          "witness_key": "work:ref-10"
        },
        {
          "row_index": 5,
          "witness_key": "work:ref-11"
        },
        {
          "row_index": 6,
          "witness_key": "work:ref-12"
        },
        {
          "row_index": 7,
          "witness_key": "work:ref-13"
        },
        {
          "row_index": 8,
          "witness_key": "work:ref-14"
        },
        {
          "row_index": 9,
          "witness_key": "work:ref-15"
        },
        {
          "row_index": 10,
          "witness_key": "work:ref-16"
        },
        {
          "row_index": 11,
          "witness_key": "work:ref-17"
        },
        {
          "row_index": 12,
          "witness_key": "work:ref-18"
        },
        {
          "row_index": 13,
          "witness_key": "work:ref-19"
        },
        {
          "row_index": 14,
          "witness_key": "work:ref-2"
        },
        {
          "row_index": 15,
          "witness_key": "work:ref-20"
        },
        {
          "row_index": 16,
          "witness_key": "work:ref-21"
        },
        {
          "row_index": 17,
          "witness_key": "work:ref-22"
        },
        {
          "row_index": 18,
          "witness_key": "work:ref-23"
        },
        {
          "row_index": 19,
          "witness_key": "work:ref-24"
        },
        {
          "row_index": 20,
          "witness_key": "work:ref-25"
        },
        {
          "row_index": 21,
          "witness_key": "work:ref-26"
        },
        {
          "row_index": 22,
          "witness_key": "work:ref-27"
        },
        {
          "row_index": 23,
          "witness_key": "work:ref-28"
        },
        {
          "row_index": 24,
          "witness_key": "work:ref-29"
        },
        {
          "row_index": 25,
          "witness_key": "work:ref-3"
        },
        {
          "row_index": 26,
          "witness_key": "work:ref-30"
        },
        {
          "row_index": 27,
          "witness_key": "work:ref-31"
        },
        {
          "row_index": 28,
          "witness_key": "work:ref-32"
        },
        {
          "row_index": 29,
          "witness_key": "work:ref-33"
        },
        {
          "row_index": 30,
          "witness_key": "work:ref-34"
        },
        {
          "row_index": 31,
          "witness_key": "work:ref-35"
        },
        {
          "row_index": 32,
          "witness_key": "work:ref-36"
        },
        {
          "row_index": 33,
          "witness_key": "work:ref-37"
        },
        {
          "row_index": 34,
          "witness_key": "work:ref-38"
        },
        {
          "row_index": 35,
          "witness_key": "work:ref-39"
        },
        {
          "row_index": 36,
          "witness_key": "work:ref-4"
        },
        {
          "row_index": 37,
          "witness_key": "work:ref-40"
        },
        {
          "row_index": 38,
          "witness_key": "work:ref-41"
        },
        {
          "row_index": 39,
          "witness_key": "work:ref-42"
        },
        {
          "row_index": 40,
          "witness_key": "work:ref-43"
        },
        {
          "row_index": 41,
          "witness_key": "work:ref-44"
        },
        {
          "row_index": 42,
          "witness_key": "work:ref-45"
        },
        {
          "row_index": 43,
          "witness_key": "work:ref-46"
        },
        {
          "row_index": 44,
          "witness_key": "work:ref-47"
        },
        {
          "row_index": 45,
          "witness_key": "work:ref-48"
        },
        {
          "row_index": 46,
          "witness_key": "work:ref-49"
        },
        {
          "row_index": 47,
          "witness_key": "work:ref-5"
        },
        {
          "row_index": 48,
          "witness_key": "work:ref-50"
        },
        {
          "row_index": 49,
          "witness_key": "work:ref-51"
        },
        {
          "row_index": 50,
          "witness_key": "work:ref-52"
        },
        {
          "row_index": 51,
          "witness_key": "work:ref-53"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref-54"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref-55"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref-56"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref-57"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref-58"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref-59"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref-6"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref-60"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref-61"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref-62"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref-63"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref-64"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref-65"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref-66"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref-67"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref-68"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref-69"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref-7"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref-70"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref-71"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref-72"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref-73"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref-74"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref-75"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref-76"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref-77"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref-78"
        },
        {
          "row_index": 79,
          "witness_key": "work:ref-79"
        },
        {
          "row_index": 80,
          "witness_key": "work:ref-8"
        },
        {
          "row_index": 81,
          "witness_key": "work:ref-9"
        },
        {
          "row_index": 82,
          "witness_key": "work:reprints"
        },
        {
          "row_index": 83,
          "witness_key": "work:self"
        },
        {
          "row_index": 84,
          "witness_key": "work:supplementary"
        },
        {
          "row_index": 85,
          "witness_key": "work:zenodo"
        },
        {
          "row_index": 86,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 87,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 88,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 89,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 90,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 91,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 92,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 93,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 94,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 95,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 96,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 97,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 98,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 99,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 100,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 101,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 102,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 103,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 104,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 105,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 106,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 107,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 108,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 109,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 110,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 111,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 112,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 113,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 114,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 115,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 116,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 117,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 118,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 119,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 120,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 121,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 122,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 123,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 124,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 125,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 126,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 127,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 128,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 129,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 130,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 131,
          "witness_key": "claim:max-depth-not-following"
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
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 135,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 136,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 137,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 138,
          "witness_key": "claim:melt-freeze-lithosphere"
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
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 142,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 143,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 144,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 145,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 146,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 147,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 148,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 149,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 150,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 151,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 152,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 153,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 154,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 155,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 156,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 157,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 158,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 159,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 160,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 161,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 162,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 163,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 164,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 165,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 166,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 167,
          "witness_key": "claim:s-wave-delays-removed"
        },
        {
          "row_index": 168,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 169,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 170,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 171,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 172,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 173,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 174,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 175,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 176,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 177,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 178,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 179,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 180,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 181,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 182,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 183,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 184,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 185,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 186,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 187,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 188,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 189,
          "witness_key": "rel:catalog-in-zenodo"
        },
        {
          "row_index": 190,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 191,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 192,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 193,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 194,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 195,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 196,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 197,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 198,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 199,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 200,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 201,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 202,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 203,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 204,
          "witness_key": "claim:vp-vs-reasonable"
        }
      ]
    },
    {
      "question_id": "CQ-T1-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The duration row carries the interval, its value and its unit, and the count row names the instrument network whose recordings they describe; nothing joins the two.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "recording_interval",
          "row_index": 84,
          "absent_reason": null,
          "note": "the quantity kind names the continuous recording of the seismic data"
        },
        {
          "semantic": "duration_value",
          "row_index": 84,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "time_unit",
          "row_index": 84,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "observing_system",
          "row_index": 10,
          "absent_reason": null,
          "note": "the count scope names the network that acquired the data"
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
          "witness_key": "instrument:nautile"
        },
        {
          "row_index": 2,
          "witness_key": "instrument:obs"
        },
        {
          "row_index": 3,
          "witness_key": "obs:events-identified-760"
        },
        {
          "row_index": 4,
          "witness_key": "obs:fm-new-3"
        },
        {
          "row_index": 5,
          "witness_key": "obs:fm-previous-3"
        },
        {
          "row_index": 6,
          "witness_key": "obs:fm-total-6"
        },
        {
          "row_index": 7,
          "witness_key": "obs:forced-depth-subset"
        },
        {
          "row_index": 8,
          "witness_key": "obs:located-514"
        },
        {
          "row_index": 9,
          "witness_key": "obs:magnitude-groups"
        },
        {
          "row_index": 10,
          "witness_key": "obs:obs-deployed-19"
        },
        {
          "row_index": 11,
          "witness_key": "obs:obs-useful-17"
        },
        {
          "row_index": 12,
          "witness_key": "obs:quality-categories"
        },
        {
          "row_index": 13,
          "witness_key": "obs:relocated-364"
        },
        {
          "row_index": 14,
          "witness_key": "obs:romanche-2016-subevents"
        },
        {
          "row_index": 15,
          "witness_key": "obs:subsection-count"
        },
        {
          "row_index": 16,
          "witness_key": "obs:velest-subdataset"
        },
        {
          "row_index": 17,
          "witness_key": "obs:velocity-models-five"
        },
        {
          "row_index": 18,
          "witness_key": "obs:well-relocated-276"
        },
        {
          "row_index": 19,
          "witness_key": "obs:abstract-co2-primary"
        },
        {
          "row_index": 20,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 21,
          "witness_key": "obs:eq-atlantic-co2-average"
        },
        {
          "row_index": 22,
          "witness_key": "obs:eq-atlantic-co2-max"
        },
        {
          "row_index": 23,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 24,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 25,
          "witness_key": "obs:axial-event-depth-stable"
        },
        {
          "row_index": 26,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 27,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 28,
          "witness_key": "obs:cluster-depth-west"
        },
        {
          "row_index": 29,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 30,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 31,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 32,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 33,
          "witness_key": "obs:criteria-met-fraction"
        },
        {
          "row_index": 34,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 35,
          "witness_key": "obs:criterion-gap"
        },
        {
          "row_index": 36,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 37,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 38,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 39,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 40,
          "witness_key": "obs:degassing-depth-range"
        },
        {
          "row_index": 41,
          "witness_key": "obs:depth-uncertainty-cap"
        },
        {
          "row_index": 42,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 43,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 44,
          "witness_key": "obs:expected-brittle-thickness"
        },
        {
          "row_index": 45,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 46,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 47,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 48,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 49,
          "witness_key": "obs:fig3e-elevation-scale"
        },
        {
          "row_index": 50,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 51,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 52,
          "witness_key": "obs:fm-gap"
        },
        {
          "row_index": 53,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 54,
          "witness_key": "obs:fm-polarities"
        },
        {
          "row_index": 55,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 56,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 57,
          "witness_key": "obs:forced-depth-range"
        },
        {
          "row_index": 58,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 59,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 60,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 61,
          "witness_key": "obs:horizontal-uncertainty-cap"
        },
        {
          "row_index": 62,
          "witness_key": "obs:lithospheric-age-interval"
        },
        {
          "row_index": 63,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 64,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 65,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 66,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 67,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 68,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 69,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 70,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 71,
          "witness_key": "obs:min-obs-per-event"
        },
        {
          "row_index": 72,
          "witness_key": "obs:model1-depth"
        },
        {
          "row_index": 73,
          "witness_key": "obs:model1-p-velocity"
        },
        {
          "row_index": 74,
          "witness_key": "obs:occ-transect-halfwidth"
        },
        {
          "row_index": 75,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 76,
          "witness_key": "obs:perturbed-deep-events"
        },
        {
          "row_index": 77,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 78,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 79,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 80,
          "witness_key": "obs:quality-a-uncertainty"
        },
        {
          "row_index": 81,
          "witness_key": "obs:quality-b-uncertainty"
        },
        {
          "row_index": 82,
          "witness_key": "obs:quality-c-uncertainty"
        },
        {
          "row_index": 83,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 84,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 85,
          "witness_key": "obs:refraction-constraint-depth"
        },
        {
          "row_index": 86,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 87,
          "witness_key": "obs:relocation-iterations"
        },
        {
          "row_index": 88,
          "witness_key": "obs:relocation-obs-count"
        },
        {
          "row_index": 89,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 90,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 91,
          "witness_key": "obs:rms-residual-cap"
        },
        {
          "row_index": 92,
          "witness_key": "obs:solubility-temperature"
        },
        {
          "row_index": 93,
          "witness_key": "obs:station-gap-cap"
        },
        {
          "row_index": 94,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 95,
          "witness_key": "obs:subdataset-arrivals"
        },
        {
          "row_index": 96,
          "witness_key": "obs:subdataset-gap"
        },
        {
          "row_index": 97,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 98,
          "witness_key": "obs:velest-iterations"
        },
        {
          "row_index": 99,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 100,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 101,
          "witness_key": "obs:obs-no-data"
        },
        {
          "row_index": 102,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 103,
          "witness_key": "obs:mar-events-317"
        },
        {
          "row_index": 104,
          "witness_key": "obs:romanche-events-197"
        },
        {
          "row_index": 105,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 106,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 107,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 108,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 109,
          "witness_key": "obs:co2-calc-rc2"
        },
        {
          "row_index": 110,
          "witness_key": "obs:co2-calc-rc3"
        },
        {
          "row_index": 111,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 112,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 113,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 114,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 115,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 116,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 117,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 118,
          "witness_key": "obs:rc2-ba"
        },
        {
          "row_index": 119,
          "witness_key": "obs:rc2-rb"
        },
        {
          "row_index": 120,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 121,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 122,
          "witness_key": "obs:bdb-at-ntd2"
        },
        {
          "row_index": 123,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 124,
          "witness_key": "obs:bdb-isotherm-fig6"
        },
        {
          "row_index": 125,
          "witness_key": "obs:bdb-isotherm-slow"
        },
        {
          "row_index": 126,
          "witness_key": "obs:bdb-isotherms-cold"
        },
        {
          "row_index": 127,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 128,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 129,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 130,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 131,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 132,
          "witness_key": "obs:deep-eq-rc2-1619"
        },
        {
          "row_index": 133,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 134,
          "witness_key": "obs:depth-range-ntd2"
        },
        {
          "row_index": 135,
          "witness_key": "obs:depth-range-occ"
        },
        {
          "row_index": 136,
          "witness_key": "obs:hot-mantle-temperature"
        },
        {
          "row_index": 137,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 138,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 139,
          "witness_key": "obs:mantle-temperature-rc2"
        },
        {
          "row_index": 140,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 141,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 142,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 143,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 144,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 145,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 146,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 147,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 148,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 149,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 150,
          "witness_key": "obs:subsolidus-temperature"
        },
        {
          "row_index": 151,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 152,
          "witness_key": "obs:vp-vs-test-range"
        }
      ]
    },
    {
      "question_id": "CQ-T2-01",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The subsection, the detachment fault and the bounding relation between them are all returned, and a relation row joins the first two. The side of the ridge axis on which the core complex sits is not a field of any returned row: the source states it in the same sentence, which the graph holds as an assertion locator and a statement digest.",
      "assembly": "LINKED_ROWS",
      "coverage": [
        {
          "semantic": "named_subsection",
          "row_index": 32,
          "absent_reason": null,
          "note": "the RTI subsection record"
        },
        {
          "semantic": "structural_feature",
          "row_index": 40,
          "absent_reason": null,
          "note": "the westward dipping detachment fault"
        },
        {
          "semantic": "bounding_relation",
          "row_index": 160,
          "absent_reason": null,
          "note": "the returned relation bounding the subsection by that fault"
        },
        {
          "semantic": "side_of_axis",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "the eastern side of the ridge axis is stated only inside the claim's words, which the graph carries as a locator and a digest"
        }
      ],
      "source_locators": [
        "page:1:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:axial-melt-lens"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 4,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 5,
          "witness_key": "feature:eq-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fracture-zone"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:hummocky"
        },
        {
          "row_index": 11,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 12,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 20,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 21,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 22,
          "witness_key": "feature:neo-volcanic-ridge"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 24,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 25,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 26,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 28,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 29,
          "witness_key": "feature:occ-surface-faults"
        },
        {
          "row_index": 30,
          "witness_key": "feature:occ-termination"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 36,
          "witness_key": "feature:romanche-faults"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:romanche-transform-valley"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rti-detachment"
        },
        {
          "row_index": 41,
          "witness_key": "feature:suspended-valley"
        },
        {
          "row_index": 42,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 43,
          "witness_key": "feature:swir-oblique"
        },
        {
          "row_index": 44,
          "witness_key": "feature:swir-segment-8"
        },
        {
          "row_index": 45,
          "witness_key": "feature:tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:transverse-ridge"
        },
        {
          "row_index": 47,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 48,
          "witness_key": "feature:west-indian-ocean"
        },
        {
          "row_index": 49,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 50,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 51,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 52,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 53,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 54,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 55,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 56,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 57,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 58,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 59,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 60,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 61,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 62,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 63,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 64,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 65,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 66,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 67,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 68,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 69,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 70,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 71,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 72,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 73,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 74,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 75,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 76,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 77,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 78,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 79,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 80,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 81,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 82,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 83,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 84,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 85,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 86,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 87,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 88,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 89,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 90,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 91,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 92,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 93,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 94,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 95,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 96,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 97,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 98,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 99,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 100,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 101,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 102,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 103,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 104,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 105,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 106,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 107,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 108,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 109,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 110,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 111,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 112,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 113,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 114,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 115,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 116,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 117,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 118,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 119,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 120,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 121,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 122,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 123,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 124,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 125,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 126,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 127,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 128,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 129,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 130,
          "witness_key": "claim:s-wave-delays-removed"
        },
        {
          "row_index": 131,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 132,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 133,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 134,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 135,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 136,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 137,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 138,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 139,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 140,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 141,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 142,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 143,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 144,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 145,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 146,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 147,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 148,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 149,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 150,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 151,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 152,
          "witness_key": "rel:askja-in-iceland"
        },
        {
          "row_index": 153,
          "witness_key": "rel:fagradalsfjall-in-iceland"
        },
        {
          "row_index": 154,
          "witness_key": "rel:logachev-of-knipovich"
        },
        {
          "row_index": 155,
          "witness_key": "rel:mar-in-eq-atlantic"
        },
        {
          "row_index": 156,
          "witness_key": "rel:marseg-bounded-chain"
        },
        {
          "row_index": 157,
          "witness_key": "rel:marseg-bounded-romanche"
        },
        {
          "row_index": 158,
          "witness_key": "rel:mayotte-in-indian-ocean"
        },
        {
          "row_index": 159,
          "witness_key": "rel:occ-on-mar"
        },
        {
          "row_index": 160,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 161,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 162,
          "witness_key": "rel:romanche-faults-in-tf"
        },
        {
          "row_index": 163,
          "witness_key": "rel:vent-field-on-ntd1"
        },
        {
          "row_index": 164,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 165,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 166,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 167,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 168,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 169,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 170,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 171,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 172,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 173,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 174,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 175,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 176,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 177,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 178,
          "witness_key": "claim:vp-vs-reasonable"
        }
      ]
    },
    {
      "question_id": "CQ-T2-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "Both programs are returned as their own records, the relocation row's scope states that the relocated events replaced the earlier locations in the final catalogue, which is the order the question asks for, and the deposited catalogue is returned; no relation joins the two programs to each other.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "initial_location_method",
          "row_index": 103,
          "absent_reason": null,
          "note": "the program that produced the initial hypocentres"
        },
        {
          "semantic": "relocation_method",
          "row_index": 102,
          "absent_reason": null,
          "note": "the program applied afterwards"
        },
        {
          "semantic": "method_sequence",
          "row_index": 225,
          "absent_reason": null,
          "note": "the count scope states that the well relocated events replaced the earlier locations in the final catalogue"
        },
        {
          "semantic": "earthquake_catalog",
          "row_index": 14,
          "absent_reason": null,
          "note": "the catalogue generated in the study"
        }
      ],
      "source_locators": [
        "page:7:block:004",
        "page:7:block:007",
        "page:8:block:010",
        "page:7:block:006",
        "page:8:block:008",
        "page:8:block:009"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "method:1d-inversion"
        },
        {
          "row_index": 1,
          "witness_key": "method:catalog-analysis"
        },
        {
          "row_index": 2,
          "witness_key": "method:dd-relocation"
        },
        {
          "row_index": 3,
          "witness_key": "method:double-difference"
        },
        {
          "row_index": 4,
          "witness_key": "method:earthquake-location"
        },
        {
          "row_index": 5,
          "witness_key": "method:focal-mechanism"
        },
        {
          "row_index": 6,
          "witness_key": "method:graphing"
        },
        {
          "row_index": 7,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 8,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 9,
          "witness_key": "method:oct-tree"
        },
        {
          "row_index": 10,
          "witness_key": "method:phase-picking"
        },
        {
          "row_index": 11,
          "witness_key": "method:sta-lta"
        },
        {
          "row_index": 12,
          "witness_key": "method:structural-analysis"
        },
        {
          "row_index": 13,
          "witness_key": "work:cruise-data"
        },
        {
          "row_index": 14,
          "witness_key": "work:earthquake-catalog"
        },
        {
          "row_index": 15,
          "witness_key": "work:petdb"
        },
        {
          "row_index": 16,
          "witness_key": "work:ref-1"
        },
        {
          "row_index": 17,
          "witness_key": "work:ref-10"
        },
        {
          "row_index": 18,
          "witness_key": "work:ref-11"
        },
        {
          "row_index": 19,
          "witness_key": "work:ref-12"
        },
        {
          "row_index": 20,
          "witness_key": "work:ref-13"
        },
        {
          "row_index": 21,
          "witness_key": "work:ref-14"
        },
        {
          "row_index": 22,
          "witness_key": "work:ref-15"
        },
        {
          "row_index": 23,
          "witness_key": "work:ref-16"
        },
        {
          "row_index": 24,
          "witness_key": "work:ref-17"
        },
        {
          "row_index": 25,
          "witness_key": "work:ref-18"
        },
        {
          "row_index": 26,
          "witness_key": "work:ref-19"
        },
        {
          "row_index": 27,
          "witness_key": "work:ref-2"
        },
        {
          "row_index": 28,
          "witness_key": "work:ref-20"
        },
        {
          "row_index": 29,
          "witness_key": "work:ref-21"
        },
        {
          "row_index": 30,
          "witness_key": "work:ref-22"
        },
        {
          "row_index": 31,
          "witness_key": "work:ref-23"
        },
        {
          "row_index": 32,
          "witness_key": "work:ref-24"
        },
        {
          "row_index": 33,
          "witness_key": "work:ref-25"
        },
        {
          "row_index": 34,
          "witness_key": "work:ref-26"
        },
        {
          "row_index": 35,
          "witness_key": "work:ref-27"
        },
        {
          "row_index": 36,
          "witness_key": "work:ref-28"
        },
        {
          "row_index": 37,
          "witness_key": "work:ref-29"
        },
        {
          "row_index": 38,
          "witness_key": "work:ref-3"
        },
        {
          "row_index": 39,
          "witness_key": "work:ref-30"
        },
        {
          "row_index": 40,
          "witness_key": "work:ref-31"
        },
        {
          "row_index": 41,
          "witness_key": "work:ref-32"
        },
        {
          "row_index": 42,
          "witness_key": "work:ref-33"
        },
        {
          "row_index": 43,
          "witness_key": "work:ref-34"
        },
        {
          "row_index": 44,
          "witness_key": "work:ref-35"
        },
        {
          "row_index": 45,
          "witness_key": "work:ref-36"
        },
        {
          "row_index": 46,
          "witness_key": "work:ref-37"
        },
        {
          "row_index": 47,
          "witness_key": "work:ref-38"
        },
        {
          "row_index": 48,
          "witness_key": "work:ref-39"
        },
        {
          "row_index": 49,
          "witness_key": "work:ref-4"
        },
        {
          "row_index": 50,
          "witness_key": "work:ref-40"
        },
        {
          "row_index": 51,
          "witness_key": "work:ref-41"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref-42"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref-43"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref-44"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref-45"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref-46"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref-47"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref-48"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref-49"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref-5"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref-50"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref-51"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref-52"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref-53"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref-54"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref-55"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref-56"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref-57"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref-58"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref-59"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref-6"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref-60"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref-61"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref-62"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref-63"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref-64"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref-65"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref-66"
        },
        {
          "row_index": 79,
          "witness_key": "work:ref-67"
        },
        {
          "row_index": 80,
          "witness_key": "work:ref-68"
        },
        {
          "row_index": 81,
          "witness_key": "work:ref-69"
        },
        {
          "row_index": 82,
          "witness_key": "work:ref-7"
        },
        {
          "row_index": 83,
          "witness_key": "work:ref-70"
        },
        {
          "row_index": 84,
          "witness_key": "work:ref-71"
        },
        {
          "row_index": 85,
          "witness_key": "work:ref-72"
        },
        {
          "row_index": 86,
          "witness_key": "work:ref-73"
        },
        {
          "row_index": 87,
          "witness_key": "work:ref-74"
        },
        {
          "row_index": 88,
          "witness_key": "work:ref-75"
        },
        {
          "row_index": 89,
          "witness_key": "work:ref-76"
        },
        {
          "row_index": 90,
          "witness_key": "work:ref-77"
        },
        {
          "row_index": 91,
          "witness_key": "work:ref-78"
        },
        {
          "row_index": 92,
          "witness_key": "work:ref-79"
        },
        {
          "row_index": 93,
          "witness_key": "work:ref-8"
        },
        {
          "row_index": 94,
          "witness_key": "work:ref-9"
        },
        {
          "row_index": 95,
          "witness_key": "work:reprints"
        },
        {
          "row_index": 96,
          "witness_key": "work:self"
        },
        {
          "row_index": 97,
          "witness_key": "work:supplementary"
        },
        {
          "row_index": 98,
          "witness_key": "work:zenodo"
        },
        {
          "row_index": 99,
          "witness_key": "software:global-mapper"
        },
        {
          "row_index": 100,
          "witness_key": "software:gmt"
        },
        {
          "row_index": 101,
          "witness_key": "software:hash"
        },
        {
          "row_index": 102,
          "witness_key": "software:hypodd"
        },
        {
          "row_index": 103,
          "witness_key": "software:nonlinloc"
        },
        {
          "row_index": 104,
          "witness_key": "software:seisan"
        },
        {
          "row_index": 105,
          "witness_key": "software:velest"
        },
        {
          "row_index": 106,
          "witness_key": "software:zmap"
        },
        {
          "row_index": 107,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 108,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 109,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 110,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 111,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 112,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 113,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 114,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 115,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 116,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 117,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 118,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 119,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 120,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 121,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 122,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 123,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 124,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 125,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 126,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 127,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 128,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 129,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 130,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 131,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 132,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 133,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 134,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 135,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 136,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 137,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 138,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 139,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 140,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 141,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 142,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 143,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 144,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 145,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 146,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 147,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 148,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 149,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 150,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 151,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 152,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 153,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 154,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 155,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 156,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 157,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 158,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 159,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 160,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 161,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 162,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 163,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 164,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 165,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 166,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 167,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 168,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 169,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 170,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 171,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 172,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 173,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 174,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 175,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 176,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 177,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 178,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 179,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 180,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 181,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 182,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 183,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 184,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 185,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 186,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 187,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 188,
          "witness_key": "claim:s-wave-delays-removed"
        },
        {
          "row_index": 189,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 190,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 191,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 192,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 193,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 194,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 195,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 196,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 197,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 198,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 199,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 200,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 201,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 202,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 203,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 204,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 205,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 206,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 207,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 208,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 209,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 210,
          "witness_key": "obs:events-identified-760"
        },
        {
          "row_index": 211,
          "witness_key": "obs:fm-new-3"
        },
        {
          "row_index": 212,
          "witness_key": "obs:fm-previous-3"
        },
        {
          "row_index": 213,
          "witness_key": "obs:fm-total-6"
        },
        {
          "row_index": 214,
          "witness_key": "obs:forced-depth-subset"
        },
        {
          "row_index": 215,
          "witness_key": "obs:located-514"
        },
        {
          "row_index": 216,
          "witness_key": "obs:magnitude-groups"
        },
        {
          "row_index": 217,
          "witness_key": "obs:obs-deployed-19"
        },
        {
          "row_index": 218,
          "witness_key": "obs:obs-useful-17"
        },
        {
          "row_index": 219,
          "witness_key": "obs:quality-categories"
        },
        {
          "row_index": 220,
          "witness_key": "obs:relocated-364"
        },
        {
          "row_index": 221,
          "witness_key": "obs:romanche-2016-subevents"
        },
        {
          "row_index": 222,
          "witness_key": "obs:subsection-count"
        },
        {
          "row_index": 223,
          "witness_key": "obs:velest-subdataset"
        },
        {
          "row_index": 224,
          "witness_key": "obs:velocity-models-five"
        },
        {
          "row_index": 225,
          "witness_key": "obs:well-relocated-276"
        },
        {
          "row_index": 226,
          "witness_key": "obs:abstract-co2-primary"
        },
        {
          "row_index": 227,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 228,
          "witness_key": "obs:eq-atlantic-co2-average"
        },
        {
          "row_index": 229,
          "witness_key": "obs:eq-atlantic-co2-max"
        },
        {
          "row_index": 230,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 231,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 232,
          "witness_key": "obs:axial-event-depth-stable"
        },
        {
          "row_index": 233,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 234,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 235,
          "witness_key": "obs:cluster-depth-west"
        },
        {
          "row_index": 236,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 237,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 238,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 239,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 240,
          "witness_key": "obs:criteria-met-fraction"
        },
        {
          "row_index": 241,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 242,
          "witness_key": "obs:criterion-gap"
        },
        {
          "row_index": 243,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 244,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 245,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 246,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 247,
          "witness_key": "obs:degassing-depth-range"
        },
        {
          "row_index": 248,
          "witness_key": "obs:depth-uncertainty-cap"
        },
        {
          "row_index": 249,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 250,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 251,
          "witness_key": "obs:expected-brittle-thickness"
        },
        {
          "row_index": 252,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 253,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 254,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 255,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 256,
          "witness_key": "obs:fig3e-elevation-scale"
        },
        {
          "row_index": 257,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 258,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 259,
          "witness_key": "obs:fm-gap"
        },
        {
          "row_index": 260,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 261,
          "witness_key": "obs:fm-polarities"
        },
        {
          "row_index": 262,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 263,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 264,
          "witness_key": "obs:forced-depth-range"
        },
        {
          "row_index": 265,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 266,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 267,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 268,
          "witness_key": "obs:horizontal-uncertainty-cap"
        },
        {
          "row_index": 269,
          "witness_key": "obs:lithospheric-age-interval"
        },
        {
          "row_index": 270,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 271,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 272,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 273,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 274,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 275,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 276,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 277,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 278,
          "witness_key": "obs:min-obs-per-event"
        },
        {
          "row_index": 279,
          "witness_key": "obs:model1-depth"
        },
        {
          "row_index": 280,
          "witness_key": "obs:model1-p-velocity"
        },
        {
          "row_index": 281,
          "witness_key": "obs:occ-transect-halfwidth"
        },
        {
          "row_index": 282,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 283,
          "witness_key": "obs:perturbed-deep-events"
        },
        {
          "row_index": 284,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 285,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 286,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 287,
          "witness_key": "obs:quality-a-uncertainty"
        },
        {
          "row_index": 288,
          "witness_key": "obs:quality-b-uncertainty"
        },
        {
          "row_index": 289,
          "witness_key": "obs:quality-c-uncertainty"
        },
        {
          "row_index": 290,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 291,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 292,
          "witness_key": "obs:refraction-constraint-depth"
        },
        {
          "row_index": 293,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 294,
          "witness_key": "obs:relocation-iterations"
        },
        {
          "row_index": 295,
          "witness_key": "obs:relocation-obs-count"
        },
        {
          "row_index": 296,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 297,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 298,
          "witness_key": "obs:rms-residual-cap"
        },
        {
          "row_index": 299,
          "witness_key": "obs:solubility-temperature"
        },
        {
          "row_index": 300,
          "witness_key": "obs:station-gap-cap"
        },
        {
          "row_index": 301,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 302,
          "witness_key": "obs:subdataset-arrivals"
        },
        {
          "row_index": 303,
          "witness_key": "obs:subdataset-gap"
        },
        {
          "row_index": 304,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 305,
          "witness_key": "obs:velest-iterations"
        },
        {
          "row_index": 306,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 307,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 308,
          "witness_key": "rel:catalog-in-zenodo"
        },
        {
          "row_index": 309,
          "witness_key": "rel:globalmapper-used-for-structural"
        },
        {
          "row_index": 310,
          "witness_key": "rel:gmt-used-for-graphing"
        },
        {
          "row_index": 311,
          "witness_key": "rel:hash-used-for-fm"
        },
        {
          "row_index": 312,
          "witness_key": "rel:hypodd-used-for-relocation"
        },
        {
          "row_index": 313,
          "witness_key": "rel:nonlinloc-used-for-octtree"
        },
        {
          "row_index": 314,
          "witness_key": "rel:seisan-used-for-picking"
        },
        {
          "row_index": 315,
          "witness_key": "rel:seisan-used-for-stalta"
        },
        {
          "row_index": 316,
          "witness_key": "rel:velest-used-for-inversion"
        },
        {
          "row_index": 317,
          "witness_key": "rel:zmap-used-for-catalog"
        },
        {
          "row_index": 318,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 319,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 320,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 321,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 322,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 323,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 324,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 325,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 326,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 327,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 328,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 329,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 330,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 331,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 332,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 333,
          "witness_key": "obs:mar-events-317"
        },
        {
          "row_index": 334,
          "witness_key": "obs:obs-no-data"
        },
        {
          "row_index": 335,
          "witness_key": "obs:romanche-events-197"
        },
        {
          "row_index": 336,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 337,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 338,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 339,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 340,
          "witness_key": "obs:co2-calc-rc2"
        },
        {
          "row_index": 341,
          "witness_key": "obs:co2-calc-rc3"
        },
        {
          "row_index": 342,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 343,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 344,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 345,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 346,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 347,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 348,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 349,
          "witness_key": "obs:rc2-ba"
        },
        {
          "row_index": 350,
          "witness_key": "obs:rc2-rb"
        },
        {
          "row_index": 351,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 352,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 353,
          "witness_key": "obs:bdb-at-ntd2"
        },
        {
          "row_index": 354,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 355,
          "witness_key": "obs:bdb-isotherm-fig6"
        },
        {
          "row_index": 356,
          "witness_key": "obs:bdb-isotherm-slow"
        },
        {
          "row_index": 357,
          "witness_key": "obs:bdb-isotherms-cold"
        },
        {
          "row_index": 358,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 359,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 360,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 361,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 362,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 363,
          "witness_key": "obs:deep-eq-rc2-1619"
        },
        {
          "row_index": 364,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 365,
          "witness_key": "obs:depth-range-ntd2"
        },
        {
          "row_index": 366,
          "witness_key": "obs:depth-range-occ"
        },
        {
          "row_index": 367,
          "witness_key": "obs:hot-mantle-temperature"
        },
        {
          "row_index": 368,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 369,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 370,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 371,
          "witness_key": "obs:mantle-temperature-rc2"
        },
        {
          "row_index": 372,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 373,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 374,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 375,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 376,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 377,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 378,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 379,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 380,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 381,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 382,
          "witness_key": "obs:subsolidus-temperature"
        },
        {
          "row_index": 383,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 384,
          "witness_key": "obs:vp-vs-test-range"
        }
      ]
    },
    {
      "question_id": "CQ-T2-03",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The vent field, the discontinuity and the relation placing the field on it are returned. Its position relative to the present-day axial valley is not a field of any returned row: the source states it in the same sentence, which the graph holds as a locator and a digest.",
      "assembly": "LINKED_ROWS",
      "coverage": [
        {
          "semantic": "named_feature",
          "row_index": 6,
          "absent_reason": null,
          "note": "the extinct hydrothermal vent field"
        },
        {
          "semantic": "host_discontinuity",
          "row_index": 23,
          "absent_reason": null,
          "note": "the discontinuity the field sits on"
        },
        {
          "semantic": "spatial_relation",
          "row_index": 261,
          "absent_reason": null,
          "note": "the returned relation placing the field on that discontinuity"
        },
        {
          "semantic": "present_day_axis",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "the distance from the present-day axial valley is stated only inside the claim's words, held as a locator and a digest"
        }
      ],
      "source_locators": [
        "page:3:block:002",
        "page:1:block:005",
        "page:2:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:axial-melt-lens"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 4,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 5,
          "witness_key": "feature:eq-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fracture-zone"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:hummocky"
        },
        {
          "row_index": 11,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 12,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 20,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 21,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 22,
          "witness_key": "feature:neo-volcanic-ridge"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 24,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 25,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 26,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 28,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 29,
          "witness_key": "feature:occ-surface-faults"
        },
        {
          "row_index": 30,
          "witness_key": "feature:occ-termination"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 36,
          "witness_key": "feature:romanche-faults"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:romanche-transform-valley"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rti-detachment"
        },
        {
          "row_index": 41,
          "witness_key": "feature:suspended-valley"
        },
        {
          "row_index": 42,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 43,
          "witness_key": "feature:swir-oblique"
        },
        {
          "row_index": 44,
          "witness_key": "feature:swir-segment-8"
        },
        {
          "row_index": 45,
          "witness_key": "feature:tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:transverse-ridge"
        },
        {
          "row_index": 47,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 48,
          "witness_key": "feature:west-indian-ocean"
        },
        {
          "row_index": 49,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 50,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 51,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 52,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 53,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 54,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 55,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 56,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 57,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 58,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 59,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 60,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 61,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 62,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 63,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 64,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 65,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 66,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 67,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 68,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 69,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 70,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 71,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 72,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 73,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 74,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 75,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 76,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 77,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 78,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 79,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 80,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 81,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 82,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 83,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 84,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 85,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 86,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 87,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 88,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 89,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 90,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 91,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 92,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 93,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 94,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 95,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 96,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 97,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 98,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 99,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 100,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 101,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 102,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 103,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 104,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 105,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 106,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 107,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 108,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 109,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 110,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 111,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 112,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 113,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 114,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 115,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 116,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 117,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 118,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 119,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 120,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 121,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 122,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 123,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 124,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 125,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 126,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 127,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 128,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 129,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 130,
          "witness_key": "claim:s-wave-delays-removed"
        },
        {
          "row_index": 131,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 132,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 133,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 134,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 135,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 136,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 137,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 138,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 139,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 140,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 141,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 142,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 143,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 144,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 145,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 146,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 147,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 148,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 149,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 150,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 151,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 152,
          "witness_key": "obs:events-identified-760"
        },
        {
          "row_index": 153,
          "witness_key": "obs:fm-new-3"
        },
        {
          "row_index": 154,
          "witness_key": "obs:fm-previous-3"
        },
        {
          "row_index": 155,
          "witness_key": "obs:fm-total-6"
        },
        {
          "row_index": 156,
          "witness_key": "obs:forced-depth-subset"
        },
        {
          "row_index": 157,
          "witness_key": "obs:located-514"
        },
        {
          "row_index": 158,
          "witness_key": "obs:magnitude-groups"
        },
        {
          "row_index": 159,
          "witness_key": "obs:obs-deployed-19"
        },
        {
          "row_index": 160,
          "witness_key": "obs:obs-useful-17"
        },
        {
          "row_index": 161,
          "witness_key": "obs:quality-categories"
        },
        {
          "row_index": 162,
          "witness_key": "obs:relocated-364"
        },
        {
          "row_index": 163,
          "witness_key": "obs:romanche-2016-subevents"
        },
        {
          "row_index": 164,
          "witness_key": "obs:subsection-count"
        },
        {
          "row_index": 165,
          "witness_key": "obs:velest-subdataset"
        },
        {
          "row_index": 166,
          "witness_key": "obs:velocity-models-five"
        },
        {
          "row_index": 167,
          "witness_key": "obs:well-relocated-276"
        },
        {
          "row_index": 168,
          "witness_key": "obs:abstract-co2-primary"
        },
        {
          "row_index": 169,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 170,
          "witness_key": "obs:eq-atlantic-co2-average"
        },
        {
          "row_index": 171,
          "witness_key": "obs:eq-atlantic-co2-max"
        },
        {
          "row_index": 172,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 173,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 174,
          "witness_key": "obs:axial-event-depth-stable"
        },
        {
          "row_index": 175,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 176,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 177,
          "witness_key": "obs:cluster-depth-west"
        },
        {
          "row_index": 178,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 179,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 180,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 181,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 182,
          "witness_key": "obs:criteria-met-fraction"
        },
        {
          "row_index": 183,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 184,
          "witness_key": "obs:criterion-gap"
        },
        {
          "row_index": 185,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 186,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 187,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 188,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 189,
          "witness_key": "obs:degassing-depth-range"
        },
        {
          "row_index": 190,
          "witness_key": "obs:depth-uncertainty-cap"
        },
        {
          "row_index": 191,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 192,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 193,
          "witness_key": "obs:expected-brittle-thickness"
        },
        {
          "row_index": 194,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 195,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 196,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 197,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 198,
          "witness_key": "obs:fig3e-elevation-scale"
        },
        {
          "row_index": 199,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 200,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 201,
          "witness_key": "obs:fm-gap"
        },
        {
          "row_index": 202,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 203,
          "witness_key": "obs:fm-polarities"
        },
        {
          "row_index": 204,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 205,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 206,
          "witness_key": "obs:forced-depth-range"
        },
        {
          "row_index": 207,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 208,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 209,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 210,
          "witness_key": "obs:horizontal-uncertainty-cap"
        },
        {
          "row_index": 211,
          "witness_key": "obs:lithospheric-age-interval"
        },
        {
          "row_index": 212,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 213,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 214,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 215,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 216,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 217,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 218,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 219,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 220,
          "witness_key": "obs:min-obs-per-event"
        },
        {
          "row_index": 221,
          "witness_key": "obs:model1-depth"
        },
        {
          "row_index": 222,
          "witness_key": "obs:model1-p-velocity"
        },
        {
          "row_index": 223,
          "witness_key": "obs:occ-transect-halfwidth"
        },
        {
          "row_index": 224,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 225,
          "witness_key": "obs:perturbed-deep-events"
        },
        {
          "row_index": 226,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 227,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 228,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 229,
          "witness_key": "obs:quality-a-uncertainty"
        },
        {
          "row_index": 230,
          "witness_key": "obs:quality-b-uncertainty"
        },
        {
          "row_index": 231,
          "witness_key": "obs:quality-c-uncertainty"
        },
        {
          "row_index": 232,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 233,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 234,
          "witness_key": "obs:refraction-constraint-depth"
        },
        {
          "row_index": 235,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 236,
          "witness_key": "obs:relocation-iterations"
        },
        {
          "row_index": 237,
          "witness_key": "obs:relocation-obs-count"
        },
        {
          "row_index": 238,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 239,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 240,
          "witness_key": "obs:rms-residual-cap"
        },
        {
          "row_index": 241,
          "witness_key": "obs:solubility-temperature"
        },
        {
          "row_index": 242,
          "witness_key": "obs:station-gap-cap"
        },
        {
          "row_index": 243,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 244,
          "witness_key": "obs:subdataset-arrivals"
        },
        {
          "row_index": 245,
          "witness_key": "obs:subdataset-gap"
        },
        {
          "row_index": 246,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 247,
          "witness_key": "obs:velest-iterations"
        },
        {
          "row_index": 248,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 249,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 250,
          "witness_key": "rel:askja-in-iceland"
        },
        {
          "row_index": 251,
          "witness_key": "rel:fagradalsfjall-in-iceland"
        },
        {
          "row_index": 252,
          "witness_key": "rel:logachev-of-knipovich"
        },
        {
          "row_index": 253,
          "witness_key": "rel:mar-in-eq-atlantic"
        },
        {
          "row_index": 254,
          "witness_key": "rel:marseg-bounded-chain"
        },
        {
          "row_index": 255,
          "witness_key": "rel:marseg-bounded-romanche"
        },
        {
          "row_index": 256,
          "witness_key": "rel:mayotte-in-indian-ocean"
        },
        {
          "row_index": 257,
          "witness_key": "rel:occ-on-mar"
        },
        {
          "row_index": 258,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 259,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 260,
          "witness_key": "rel:romanche-faults-in-tf"
        },
        {
          "row_index": 261,
          "witness_key": "rel:vent-field-on-ntd1"
        },
        {
          "row_index": 262,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 263,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 264,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 265,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 266,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 267,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 268,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 269,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 270,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 271,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 272,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 273,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 274,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 275,
          "witness_key": "obs:mar-events-317"
        },
        {
          "row_index": 276,
          "witness_key": "obs:romanche-events-197"
        },
        {
          "row_index": 277,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 278,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 279,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 280,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 281,
          "witness_key": "obs:co2-calc-rc2"
        },
        {
          "row_index": 282,
          "witness_key": "obs:co2-calc-rc3"
        },
        {
          "row_index": 283,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 284,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 285,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 286,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 287,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 288,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 289,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 290,
          "witness_key": "obs:rc2-ba"
        },
        {
          "row_index": 291,
          "witness_key": "obs:rc2-rb"
        },
        {
          "row_index": 292,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 293,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 294,
          "witness_key": "obs:bdb-at-ntd2"
        },
        {
          "row_index": 295,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 296,
          "witness_key": "obs:bdb-isotherm-fig6"
        },
        {
          "row_index": 297,
          "witness_key": "obs:bdb-isotherm-slow"
        },
        {
          "row_index": 298,
          "witness_key": "obs:bdb-isotherms-cold"
        },
        {
          "row_index": 299,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 300,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 301,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 302,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 303,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 304,
          "witness_key": "obs:deep-eq-rc2-1619"
        },
        {
          "row_index": 305,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 306,
          "witness_key": "obs:depth-range-ntd2"
        },
        {
          "row_index": 307,
          "witness_key": "obs:depth-range-occ"
        },
        {
          "row_index": 308,
          "witness_key": "obs:hot-mantle-temperature"
        },
        {
          "row_index": 309,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 310,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 311,
          "witness_key": "obs:mantle-temperature-rc2"
        },
        {
          "row_index": 312,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 313,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 314,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 315,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 316,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 317,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 318,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 319,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 320,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 321,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 322,
          "witness_key": "obs:subsolidus-temperature"
        },
        {
          "row_index": 323,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 324,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 325,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 326,
          "witness_key": "obs:obs-no-data"
        },
        {
          "row_index": 327,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 328,
          "witness_key": "obs:vp-vs-test-range"
        }
      ]
    },
    {
      "question_id": "CQ-T2-04",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The thickness, the flank it belongs to and the crustal age are all carried by returned observation rows. The earlier study is not: the source attributes the thickness by a superscript numeral, which the capture records as a gap and which no returned row or relation carries.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "source_study",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "the attribution is a superscript numeral inside the sentence the graph holds as a locator and a digest, and no returned relation ties the reference record to the thickness"
        },
        {
          "semantic": "crustal_thickness_claim",
          "row_index": 273,
          "absent_reason": null,
          "note": "the thickness with its uncertainty"
        },
        {
          "semantic": "location_relation",
          "row_index": 273,
          "absent_reason": null,
          "note": "the same row's quantity kind names the western ridge flank"
        },
        {
          "semantic": "crustal_age",
          "row_index": 272,
          "absent_reason": null,
          "note": "the age of that crust"
        }
      ],
      "source_locators": [
        "page:2:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:axial-melt-lens"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 4,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 5,
          "witness_key": "feature:eq-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fracture-zone"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:hummocky"
        },
        {
          "row_index": 11,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 12,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 20,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 21,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 22,
          "witness_key": "feature:neo-volcanic-ridge"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 24,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 25,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 26,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 28,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 29,
          "witness_key": "feature:occ-surface-faults"
        },
        {
          "row_index": 30,
          "witness_key": "feature:occ-termination"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 36,
          "witness_key": "feature:romanche-faults"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:romanche-transform-valley"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rti-detachment"
        },
        {
          "row_index": 41,
          "witness_key": "feature:suspended-valley"
        },
        {
          "row_index": 42,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 43,
          "witness_key": "feature:swir-oblique"
        },
        {
          "row_index": 44,
          "witness_key": "feature:swir-segment-8"
        },
        {
          "row_index": 45,
          "witness_key": "feature:tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:transverse-ridge"
        },
        {
          "row_index": 47,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 48,
          "witness_key": "feature:west-indian-ocean"
        },
        {
          "row_index": 49,
          "witness_key": "work:cruise-data"
        },
        {
          "row_index": 50,
          "witness_key": "work:earthquake-catalog"
        },
        {
          "row_index": 51,
          "witness_key": "work:petdb"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref-1"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref-10"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref-11"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref-12"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref-13"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref-14"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref-15"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref-16"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref-17"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref-18"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref-19"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref-2"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref-20"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref-21"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref-22"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref-23"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref-24"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref-25"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref-26"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref-27"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref-28"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref-29"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref-3"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref-30"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref-31"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref-32"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref-33"
        },
        {
          "row_index": 79,
          "witness_key": "work:ref-34"
        },
        {
          "row_index": 80,
          "witness_key": "work:ref-35"
        },
        {
          "row_index": 81,
          "witness_key": "work:ref-36"
        },
        {
          "row_index": 82,
          "witness_key": "work:ref-37"
        },
        {
          "row_index": 83,
          "witness_key": "work:ref-38"
        },
        {
          "row_index": 84,
          "witness_key": "work:ref-39"
        },
        {
          "row_index": 85,
          "witness_key": "work:ref-4"
        },
        {
          "row_index": 86,
          "witness_key": "work:ref-40"
        },
        {
          "row_index": 87,
          "witness_key": "work:ref-41"
        },
        {
          "row_index": 88,
          "witness_key": "work:ref-42"
        },
        {
          "row_index": 89,
          "witness_key": "work:ref-43"
        },
        {
          "row_index": 90,
          "witness_key": "work:ref-44"
        },
        {
          "row_index": 91,
          "witness_key": "work:ref-45"
        },
        {
          "row_index": 92,
          "witness_key": "work:ref-46"
        },
        {
          "row_index": 93,
          "witness_key": "work:ref-47"
        },
        {
          "row_index": 94,
          "witness_key": "work:ref-48"
        },
        {
          "row_index": 95,
          "witness_key": "work:ref-49"
        },
        {
          "row_index": 96,
          "witness_key": "work:ref-5"
        },
        {
          "row_index": 97,
          "witness_key": "work:ref-50"
        },
        {
          "row_index": 98,
          "witness_key": "work:ref-51"
        },
        {
          "row_index": 99,
          "witness_key": "work:ref-52"
        },
        {
          "row_index": 100,
          "witness_key": "work:ref-53"
        },
        {
          "row_index": 101,
          "witness_key": "work:ref-54"
        },
        {
          "row_index": 102,
          "witness_key": "work:ref-55"
        },
        {
          "row_index": 103,
          "witness_key": "work:ref-56"
        },
        {
          "row_index": 104,
          "witness_key": "work:ref-57"
        },
        {
          "row_index": 105,
          "witness_key": "work:ref-58"
        },
        {
          "row_index": 106,
          "witness_key": "work:ref-59"
        },
        {
          "row_index": 107,
          "witness_key": "work:ref-6"
        },
        {
          "row_index": 108,
          "witness_key": "work:ref-60"
        },
        {
          "row_index": 109,
          "witness_key": "work:ref-61"
        },
        {
          "row_index": 110,
          "witness_key": "work:ref-62"
        },
        {
          "row_index": 111,
          "witness_key": "work:ref-63"
        },
        {
          "row_index": 112,
          "witness_key": "work:ref-64"
        },
        {
          "row_index": 113,
          "witness_key": "work:ref-65"
        },
        {
          "row_index": 114,
          "witness_key": "work:ref-66"
        },
        {
          "row_index": 115,
          "witness_key": "work:ref-67"
        },
        {
          "row_index": 116,
          "witness_key": "work:ref-68"
        },
        {
          "row_index": 117,
          "witness_key": "work:ref-69"
        },
        {
          "row_index": 118,
          "witness_key": "work:ref-7"
        },
        {
          "row_index": 119,
          "witness_key": "work:ref-70"
        },
        {
          "row_index": 120,
          "witness_key": "work:ref-71"
        },
        {
          "row_index": 121,
          "witness_key": "work:ref-72"
        },
        {
          "row_index": 122,
          "witness_key": "work:ref-73"
        },
        {
          "row_index": 123,
          "witness_key": "work:ref-74"
        },
        {
          "row_index": 124,
          "witness_key": "work:ref-75"
        },
        {
          "row_index": 125,
          "witness_key": "work:ref-76"
        },
        {
          "row_index": 126,
          "witness_key": "work:ref-77"
        },
        {
          "row_index": 127,
          "witness_key": "work:ref-78"
        },
        {
          "row_index": 128,
          "witness_key": "work:ref-79"
        },
        {
          "row_index": 129,
          "witness_key": "work:ref-8"
        },
        {
          "row_index": 130,
          "witness_key": "work:ref-9"
        },
        {
          "row_index": 131,
          "witness_key": "work:reprints"
        },
        {
          "row_index": 132,
          "witness_key": "work:self"
        },
        {
          "row_index": 133,
          "witness_key": "work:supplementary"
        },
        {
          "row_index": 134,
          "witness_key": "work:zenodo"
        },
        {
          "row_index": 135,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 136,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 137,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 138,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 139,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 140,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 141,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 142,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 143,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 144,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 145,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 146,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 147,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 148,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 149,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 150,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 151,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 152,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 153,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 154,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 155,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 156,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 157,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 158,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 159,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 160,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 161,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 162,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 163,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 164,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 165,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 166,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 167,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 168,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 169,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 170,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 171,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 172,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 173,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 174,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 175,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 176,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 177,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 178,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 179,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 180,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 181,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 182,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 183,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 184,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 185,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 186,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 187,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 188,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 189,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 190,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 191,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 192,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 193,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 194,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 195,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 196,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 197,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 198,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 199,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 200,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 201,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 202,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 203,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 204,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 205,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 206,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 207,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 208,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 209,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 210,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 211,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 212,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 213,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 214,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 215,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 216,
          "witness_key": "claim:s-wave-delays-removed"
        },
        {
          "row_index": 217,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 218,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 219,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 220,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 221,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 222,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 223,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 224,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 225,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 226,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 227,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 228,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 229,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 230,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 231,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 232,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 233,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 234,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 235,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 236,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 237,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 238,
          "witness_key": "obs:events-identified-760"
        },
        {
          "row_index": 239,
          "witness_key": "obs:fm-new-3"
        },
        {
          "row_index": 240,
          "witness_key": "obs:fm-previous-3"
        },
        {
          "row_index": 241,
          "witness_key": "obs:fm-total-6"
        },
        {
          "row_index": 242,
          "witness_key": "obs:forced-depth-subset"
        },
        {
          "row_index": 243,
          "witness_key": "obs:located-514"
        },
        {
          "row_index": 244,
          "witness_key": "obs:magnitude-groups"
        },
        {
          "row_index": 245,
          "witness_key": "obs:obs-deployed-19"
        },
        {
          "row_index": 246,
          "witness_key": "obs:obs-useful-17"
        },
        {
          "row_index": 247,
          "witness_key": "obs:quality-categories"
        },
        {
          "row_index": 248,
          "witness_key": "obs:relocated-364"
        },
        {
          "row_index": 249,
          "witness_key": "obs:romanche-2016-subevents"
        },
        {
          "row_index": 250,
          "witness_key": "obs:subsection-count"
        },
        {
          "row_index": 251,
          "witness_key": "obs:velest-subdataset"
        },
        {
          "row_index": 252,
          "witness_key": "obs:velocity-models-five"
        },
        {
          "row_index": 253,
          "witness_key": "obs:well-relocated-276"
        },
        {
          "row_index": 254,
          "witness_key": "obs:abstract-co2-primary"
        },
        {
          "row_index": 255,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 256,
          "witness_key": "obs:eq-atlantic-co2-average"
        },
        {
          "row_index": 257,
          "witness_key": "obs:eq-atlantic-co2-max"
        },
        {
          "row_index": 258,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 259,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 260,
          "witness_key": "obs:axial-event-depth-stable"
        },
        {
          "row_index": 261,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 262,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 263,
          "witness_key": "obs:cluster-depth-west"
        },
        {
          "row_index": 264,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 265,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 266,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 267,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 268,
          "witness_key": "obs:criteria-met-fraction"
        },
        {
          "row_index": 269,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 270,
          "witness_key": "obs:criterion-gap"
        },
        {
          "row_index": 271,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 272,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 273,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 274,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 275,
          "witness_key": "obs:degassing-depth-range"
        },
        {
          "row_index": 276,
          "witness_key": "obs:depth-uncertainty-cap"
        },
        {
          "row_index": 277,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 278,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 279,
          "witness_key": "obs:expected-brittle-thickness"
        },
        {
          "row_index": 280,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 281,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 282,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 283,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 284,
          "witness_key": "obs:fig3e-elevation-scale"
        },
        {
          "row_index": 285,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 286,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 287,
          "witness_key": "obs:fm-gap"
        },
        {
          "row_index": 288,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 289,
          "witness_key": "obs:fm-polarities"
        },
        {
          "row_index": 290,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 291,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 292,
          "witness_key": "obs:forced-depth-range"
        },
        {
          "row_index": 293,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 294,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 295,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 296,
          "witness_key": "obs:horizontal-uncertainty-cap"
        },
        {
          "row_index": 297,
          "witness_key": "obs:lithospheric-age-interval"
        },
        {
          "row_index": 298,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 299,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 300,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 301,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 302,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 303,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 304,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 305,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 306,
          "witness_key": "obs:min-obs-per-event"
        },
        {
          "row_index": 307,
          "witness_key": "obs:model1-depth"
        },
        {
          "row_index": 308,
          "witness_key": "obs:model1-p-velocity"
        },
        {
          "row_index": 309,
          "witness_key": "obs:occ-transect-halfwidth"
        },
        {
          "row_index": 310,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 311,
          "witness_key": "obs:perturbed-deep-events"
        },
        {
          "row_index": 312,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 313,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 314,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 315,
          "witness_key": "obs:quality-a-uncertainty"
        },
        {
          "row_index": 316,
          "witness_key": "obs:quality-b-uncertainty"
        },
        {
          "row_index": 317,
          "witness_key": "obs:quality-c-uncertainty"
        },
        {
          "row_index": 318,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 319,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 320,
          "witness_key": "obs:refraction-constraint-depth"
        },
        {
          "row_index": 321,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 322,
          "witness_key": "obs:relocation-iterations"
        },
        {
          "row_index": 323,
          "witness_key": "obs:relocation-obs-count"
        },
        {
          "row_index": 324,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 325,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 326,
          "witness_key": "obs:rms-residual-cap"
        },
        {
          "row_index": 327,
          "witness_key": "obs:solubility-temperature"
        },
        {
          "row_index": 328,
          "witness_key": "obs:station-gap-cap"
        },
        {
          "row_index": 329,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 330,
          "witness_key": "obs:subdataset-arrivals"
        },
        {
          "row_index": 331,
          "witness_key": "obs:subdataset-gap"
        },
        {
          "row_index": 332,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 333,
          "witness_key": "obs:velest-iterations"
        },
        {
          "row_index": 334,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 335,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 336,
          "witness_key": "rel:askja-in-iceland"
        },
        {
          "row_index": 337,
          "witness_key": "rel:fagradalsfjall-in-iceland"
        },
        {
          "row_index": 338,
          "witness_key": "rel:logachev-of-knipovich"
        },
        {
          "row_index": 339,
          "witness_key": "rel:mar-in-eq-atlantic"
        },
        {
          "row_index": 340,
          "witness_key": "rel:marseg-bounded-chain"
        },
        {
          "row_index": 341,
          "witness_key": "rel:marseg-bounded-romanche"
        },
        {
          "row_index": 342,
          "witness_key": "rel:mayotte-in-indian-ocean"
        },
        {
          "row_index": 343,
          "witness_key": "rel:occ-on-mar"
        },
        {
          "row_index": 344,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 345,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 346,
          "witness_key": "rel:romanche-faults-in-tf"
        },
        {
          "row_index": 347,
          "witness_key": "rel:vent-field-on-ntd1"
        },
        {
          "row_index": 348,
          "witness_key": "rel:catalog-in-zenodo"
        },
        {
          "row_index": 349,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 350,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 351,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 352,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 353,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 354,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 355,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 356,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 357,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 358,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 359,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 360,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 361,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 362,
          "witness_key": "obs:mar-events-317"
        },
        {
          "row_index": 363,
          "witness_key": "obs:romanche-events-197"
        },
        {
          "row_index": 364,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 365,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 366,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 367,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 368,
          "witness_key": "obs:co2-calc-rc2"
        },
        {
          "row_index": 369,
          "witness_key": "obs:co2-calc-rc3"
        },
        {
          "row_index": 370,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 371,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 372,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 373,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 374,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 375,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 376,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 377,
          "witness_key": "obs:rc2-ba"
        },
        {
          "row_index": 378,
          "witness_key": "obs:rc2-rb"
        },
        {
          "row_index": 379,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 380,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 381,
          "witness_key": "obs:bdb-at-ntd2"
        },
        {
          "row_index": 382,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 383,
          "witness_key": "obs:bdb-isotherm-fig6"
        },
        {
          "row_index": 384,
          "witness_key": "obs:bdb-isotherm-slow"
        },
        {
          "row_index": 385,
          "witness_key": "obs:bdb-isotherms-cold"
        },
        {
          "row_index": 386,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 387,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 388,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 389,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 390,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 391,
          "witness_key": "obs:deep-eq-rc2-1619"
        },
        {
          "row_index": 392,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 393,
          "witness_key": "obs:depth-range-ntd2"
        },
        {
          "row_index": 394,
          "witness_key": "obs:depth-range-occ"
        },
        {
          "row_index": 395,
          "witness_key": "obs:hot-mantle-temperature"
        },
        {
          "row_index": 396,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 397,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 398,
          "witness_key": "obs:mantle-temperature-rc2"
        },
        {
          "row_index": 399,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 400,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 401,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 402,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 403,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 404,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 405,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 406,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 407,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 408,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 409,
          "witness_key": "obs:subsolidus-temperature"
        },
        {
          "row_index": 410,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 411,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 412,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 413,
          "witness_key": "obs:obs-no-data"
        },
        {
          "row_index": 414,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 415,
          "witness_key": "obs:vp-vs-test-range"
        }
      ]
    },
    {
      "question_id": "CQ-T2-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The award, its identifier, the author and the relation attributing the one to the other are all returned.",
      "assembly": "LINKED_ROWS",
      "coverage": [
        {
          "semantic": "funding_record",
          "row_index": 0,
          "absent_reason": null,
          "note": "the named grant award"
        },
        {
          "semantic": "grant_identifier",
          "row_index": 0,
          "absent_reason": null,
          "note": "the same row's agreement number"
        },
        {
          "semantic": "person",
          "row_index": 15,
          "absent_reason": null,
          "note": "the author the grant is attributed to"
        },
        {
          "semantic": "attribution_relation",
          "row_index": 31,
          "absent_reason": null,
          "note": "the returned funding relation between them"
        }
      ],
      "source_locators": [
        "page:10:block:044",
        "page:1:block:001",
        "page:1:block:006",
        "page:11:block:002"
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
          "witness_key": "agent:brunelli"
        },
        {
          "row_index": 9,
          "witness_key": "agent:cartigny"
        },
        {
          "row_index": 10,
          "witness_key": "agent:geli"
        },
        {
          "row_index": 11,
          "witness_key": "agent:grenet"
        },
        {
          "row_index": 12,
          "witness_key": "agent:hamelin"
        },
        {
          "row_index": 13,
          "witness_key": "agent:maia"
        },
        {
          "row_index": 14,
          "witness_key": "agent:petracchini"
        },
        {
          "row_index": 15,
          "witness_key": "agent:singh"
        },
        {
          "row_index": 16,
          "witness_key": "agent:wang"
        },
        {
          "row_index": 17,
          "witness_key": "agent:yang"
        },
        {
          "row_index": 18,
          "witness_key": "agent:yu"
        },
        {
          "row_index": 19,
          "witness_key": "org:brittany"
        },
        {
          "row_index": 20,
          "witness_key": "org:cnr-igag"
        },
        {
          "row_index": 21,
          "witness_key": "org:erc"
        },
        {
          "row_index": 22,
          "witness_key": "org:eu"
        },
        {
          "row_index": 23,
          "witness_key": "org:french-government"
        },
        {
          "row_index": 24,
          "witness_key": "org:geo-ocean"
        },
        {
          "row_index": 25,
          "witness_key": "org:ipgp"
        },
        {
          "row_index": 26,
          "witness_key": "org:nsfc"
        },
        {
          "row_index": 27,
          "witness_key": "org:sio"
        },
        {
          "row_index": 28,
          "witness_key": "org:tgir"
        },
        {
          "row_index": 29,
          "witness_key": "org:unimore"
        },
        {
          "row_index": 30,
          "witness_key": "org:zjnsf"
        },
        {
          "row_index": 31,
          "witness_key": "rel:singh-funded-erc"
        },
        {
          "row_index": 32,
          "witness_key": "rel:singh-funded-fp7"
        },
        {
          "row_index": 33,
          "witness_key": "rel:yu-funded-nsfc"
        },
        {
          "row_index": 34,
          "witness_key": "rel:yu-funded-zjnsf"
        },
        {
          "row_index": 35,
          "witness_key": "rel:yu-funded-nsfc-body"
        },
        {
          "row_index": 36,
          "witness_key": "rel:yu-funded-zjnsf-body"
        }
      ]
    },
    {
      "question_id": "CQ-T3-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The depth range, its unit, its subject and its measured status are carried by the segment observation, and the reference surface is carried by a second observation of the same deep earthquakes beneath the ridge axis; nothing joins the two rows.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 305,
          "absent_reason": null,
          "note": "the observed depth range beneath the segment axis"
        },
        {
          "semantic": "length_unit",
          "row_index": 305,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "quantity_subject",
          "row_index": 305,
          "absent_reason": null,
          "note": "the row's subject is the magmatic ridge segment"
        },
        {
          "semantic": "measurement_status",
          "row_index": 305,
          "absent_reason": null,
          "note": "the row's determination is measured, so the depths were located in this study"
        },
        {
          "semantic": "depth_reference_surface",
          "row_index": 304,
          "absent_reason": null,
          "note": "this row states the same deep earthquakes below the seafloor; its subject is the ridge rather than the segment"
        }
      ],
      "source_locators": [
        "page:2:block:006",
        "page:7:block:012"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:axial-melt-lens"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 4,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 5,
          "witness_key": "feature:eq-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fracture-zone"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:hummocky"
        },
        {
          "row_index": 11,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 12,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 20,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 21,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 22,
          "witness_key": "feature:neo-volcanic-ridge"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 24,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 25,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 26,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 28,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 29,
          "witness_key": "feature:occ-surface-faults"
        },
        {
          "row_index": 30,
          "witness_key": "feature:occ-termination"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 36,
          "witness_key": "feature:romanche-faults"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:romanche-transform-valley"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rti-detachment"
        },
        {
          "row_index": 41,
          "witness_key": "feature:suspended-valley"
        },
        {
          "row_index": 42,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 43,
          "witness_key": "feature:swir-oblique"
        },
        {
          "row_index": 44,
          "witness_key": "feature:swir-segment-8"
        },
        {
          "row_index": 45,
          "witness_key": "feature:tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:transverse-ridge"
        },
        {
          "row_index": 47,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 48,
          "witness_key": "feature:west-indian-ocean"
        },
        {
          "row_index": 49,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 50,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 51,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 52,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 53,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 54,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 55,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 56,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 57,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 58,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 59,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 60,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 61,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 62,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 63,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 64,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 65,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 66,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 67,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 68,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 69,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 70,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 71,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 72,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 73,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 74,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 75,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 76,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 77,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 78,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 79,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 80,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 81,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 82,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 83,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 84,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 85,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 86,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 87,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 88,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 89,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 90,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 91,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 92,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 93,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 94,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 95,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 96,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 97,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 98,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 99,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 100,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 101,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 102,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 103,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 104,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 105,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 106,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 107,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 108,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 109,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 110,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 111,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 112,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 113,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 114,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 115,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 116,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 117,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 118,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 119,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 120,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 121,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 122,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 123,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 124,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 125,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 126,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 127,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 128,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 129,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 130,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 131,
          "witness_key": "claim:s-wave-delays-removed"
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
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 135,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 136,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 137,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 138,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 139,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 140,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 141,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 142,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 143,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 144,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 145,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 146,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 147,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 148,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 149,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 150,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 151,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 152,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 153,
          "witness_key": "obs:events-identified-760"
        },
        {
          "row_index": 154,
          "witness_key": "obs:fm-new-3"
        },
        {
          "row_index": 155,
          "witness_key": "obs:fm-previous-3"
        },
        {
          "row_index": 156,
          "witness_key": "obs:fm-total-6"
        },
        {
          "row_index": 157,
          "witness_key": "obs:forced-depth-subset"
        },
        {
          "row_index": 158,
          "witness_key": "obs:located-514"
        },
        {
          "row_index": 159,
          "witness_key": "obs:magnitude-groups"
        },
        {
          "row_index": 160,
          "witness_key": "obs:obs-deployed-19"
        },
        {
          "row_index": 161,
          "witness_key": "obs:obs-useful-17"
        },
        {
          "row_index": 162,
          "witness_key": "obs:quality-categories"
        },
        {
          "row_index": 163,
          "witness_key": "obs:relocated-364"
        },
        {
          "row_index": 164,
          "witness_key": "obs:romanche-2016-subevents"
        },
        {
          "row_index": 165,
          "witness_key": "obs:subsection-count"
        },
        {
          "row_index": 166,
          "witness_key": "obs:velest-subdataset"
        },
        {
          "row_index": 167,
          "witness_key": "obs:velocity-models-five"
        },
        {
          "row_index": 168,
          "witness_key": "obs:well-relocated-276"
        },
        {
          "row_index": 169,
          "witness_key": "obs:abstract-co2-primary"
        },
        {
          "row_index": 170,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 171,
          "witness_key": "obs:eq-atlantic-co2-average"
        },
        {
          "row_index": 172,
          "witness_key": "obs:eq-atlantic-co2-max"
        },
        {
          "row_index": 173,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 174,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 175,
          "witness_key": "obs:axial-event-depth-stable"
        },
        {
          "row_index": 176,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 177,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 178,
          "witness_key": "obs:cluster-depth-west"
        },
        {
          "row_index": 179,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 180,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 181,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 182,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 183,
          "witness_key": "obs:criteria-met-fraction"
        },
        {
          "row_index": 184,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 185,
          "witness_key": "obs:criterion-gap"
        },
        {
          "row_index": 186,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 187,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 188,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 189,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 190,
          "witness_key": "obs:degassing-depth-range"
        },
        {
          "row_index": 191,
          "witness_key": "obs:depth-uncertainty-cap"
        },
        {
          "row_index": 192,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 193,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 194,
          "witness_key": "obs:expected-brittle-thickness"
        },
        {
          "row_index": 195,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 196,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 197,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 198,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 199,
          "witness_key": "obs:fig3e-elevation-scale"
        },
        {
          "row_index": 200,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 201,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 202,
          "witness_key": "obs:fm-gap"
        },
        {
          "row_index": 203,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 204,
          "witness_key": "obs:fm-polarities"
        },
        {
          "row_index": 205,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 206,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 207,
          "witness_key": "obs:forced-depth-range"
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
          "witness_key": "obs:horizontal-uncertainty-cap"
        },
        {
          "row_index": 212,
          "witness_key": "obs:lithospheric-age-interval"
        },
        {
          "row_index": 213,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 214,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 215,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 216,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 217,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 218,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 219,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 220,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 221,
          "witness_key": "obs:min-obs-per-event"
        },
        {
          "row_index": 222,
          "witness_key": "obs:model1-depth"
        },
        {
          "row_index": 223,
          "witness_key": "obs:model1-p-velocity"
        },
        {
          "row_index": 224,
          "witness_key": "obs:occ-transect-halfwidth"
        },
        {
          "row_index": 225,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 226,
          "witness_key": "obs:perturbed-deep-events"
        },
        {
          "row_index": 227,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 228,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 229,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 230,
          "witness_key": "obs:quality-a-uncertainty"
        },
        {
          "row_index": 231,
          "witness_key": "obs:quality-b-uncertainty"
        },
        {
          "row_index": 232,
          "witness_key": "obs:quality-c-uncertainty"
        },
        {
          "row_index": 233,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 234,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 235,
          "witness_key": "obs:refraction-constraint-depth"
        },
        {
          "row_index": 236,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 237,
          "witness_key": "obs:relocation-iterations"
        },
        {
          "row_index": 238,
          "witness_key": "obs:relocation-obs-count"
        },
        {
          "row_index": 239,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 240,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 241,
          "witness_key": "obs:rms-residual-cap"
        },
        {
          "row_index": 242,
          "witness_key": "obs:solubility-temperature"
        },
        {
          "row_index": 243,
          "witness_key": "obs:station-gap-cap"
        },
        {
          "row_index": 244,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 245,
          "witness_key": "obs:subdataset-arrivals"
        },
        {
          "row_index": 246,
          "witness_key": "obs:subdataset-gap"
        },
        {
          "row_index": 247,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 248,
          "witness_key": "obs:velest-iterations"
        },
        {
          "row_index": 249,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 250,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 251,
          "witness_key": "rel:askja-in-iceland"
        },
        {
          "row_index": 252,
          "witness_key": "rel:fagradalsfjall-in-iceland"
        },
        {
          "row_index": 253,
          "witness_key": "rel:logachev-of-knipovich"
        },
        {
          "row_index": 254,
          "witness_key": "rel:mar-in-eq-atlantic"
        },
        {
          "row_index": 255,
          "witness_key": "rel:marseg-bounded-chain"
        },
        {
          "row_index": 256,
          "witness_key": "rel:marseg-bounded-romanche"
        },
        {
          "row_index": 257,
          "witness_key": "rel:mayotte-in-indian-ocean"
        },
        {
          "row_index": 258,
          "witness_key": "rel:occ-on-mar"
        },
        {
          "row_index": 259,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 260,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 261,
          "witness_key": "rel:romanche-faults-in-tf"
        },
        {
          "row_index": 262,
          "witness_key": "rel:vent-field-on-ntd1"
        },
        {
          "row_index": 263,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 264,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 265,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 266,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 267,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 268,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 269,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 270,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 271,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 272,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 273,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 274,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 275,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 276,
          "witness_key": "obs:mar-events-317"
        },
        {
          "row_index": 277,
          "witness_key": "obs:romanche-events-197"
        },
        {
          "row_index": 278,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 279,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 280,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 281,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 282,
          "witness_key": "obs:co2-calc-rc2"
        },
        {
          "row_index": 283,
          "witness_key": "obs:co2-calc-rc3"
        },
        {
          "row_index": 284,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 285,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 286,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 287,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 288,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 289,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 290,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 291,
          "witness_key": "obs:rc2-ba"
        },
        {
          "row_index": 292,
          "witness_key": "obs:rc2-rb"
        },
        {
          "row_index": 293,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 294,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 295,
          "witness_key": "obs:bdb-at-ntd2"
        },
        {
          "row_index": 296,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 297,
          "witness_key": "obs:bdb-isotherm-fig6"
        },
        {
          "row_index": 298,
          "witness_key": "obs:bdb-isotherm-slow"
        },
        {
          "row_index": 299,
          "witness_key": "obs:bdb-isotherms-cold"
        },
        {
          "row_index": 300,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 301,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 302,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 303,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 304,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 305,
          "witness_key": "obs:deep-eq-rc2-1619"
        },
        {
          "row_index": 306,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 307,
          "witness_key": "obs:depth-range-ntd2"
        },
        {
          "row_index": 308,
          "witness_key": "obs:depth-range-occ"
        },
        {
          "row_index": 309,
          "witness_key": "obs:hot-mantle-temperature"
        },
        {
          "row_index": 310,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 311,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 312,
          "witness_key": "obs:mantle-temperature-rc2"
        },
        {
          "row_index": 313,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 314,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 315,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 316,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 317,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 318,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 319,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 320,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 321,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 322,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 323,
          "witness_key": "obs:subsolidus-temperature"
        },
        {
          "row_index": 324,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 325,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 326,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 327,
          "witness_key": "obs:obs-no-data"
        },
        {
          "row_index": 328,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 329,
          "witness_key": "obs:vp-vs-test-range"
        }
      ]
    },
    {
      "question_id": "CQ-T3-02",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One observation row carries the content, the unit, the primary-melt subject and the calculated status.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 285,
          "absent_reason": null,
          "note": "the primary-melt content estimated from the barium proxy"
        },
        {
          "semantic": "concentration_unit",
          "row_index": 285,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "quantity_subject",
          "row_index": 285,
          "absent_reason": null,
          "note": "the row's subject is the studied segment and its melt stage is the primary melt"
        },
        {
          "semantic": "calculated_or_measured_status",
          "row_index": 285,
          "absent_reason": null,
          "note": "the row's determination is estimated and its modality calculated"
        }
      ],
      "source_locators": [
        "page:8:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:axial-melt-lens"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 4,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 5,
          "witness_key": "feature:eq-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fracture-zone"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:hummocky"
        },
        {
          "row_index": 11,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 12,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 20,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 21,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 22,
          "witness_key": "feature:neo-volcanic-ridge"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 24,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 25,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 26,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 28,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 29,
          "witness_key": "feature:occ-surface-faults"
        },
        {
          "row_index": 30,
          "witness_key": "feature:occ-termination"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 36,
          "witness_key": "feature:romanche-faults"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:romanche-transform-valley"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rti-detachment"
        },
        {
          "row_index": 41,
          "witness_key": "feature:suspended-valley"
        },
        {
          "row_index": 42,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 43,
          "witness_key": "feature:swir-oblique"
        },
        {
          "row_index": 44,
          "witness_key": "feature:swir-segment-8"
        },
        {
          "row_index": 45,
          "witness_key": "feature:tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:transverse-ridge"
        },
        {
          "row_index": 47,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 48,
          "witness_key": "feature:west-indian-ocean"
        },
        {
          "row_index": 49,
          "witness_key": "sample:basalt"
        },
        {
          "row_index": 50,
          "witness_key": "sample:morb-obs-network"
        },
        {
          "row_index": 51,
          "witness_key": "sample:morb-rc2"
        },
        {
          "row_index": 52,
          "witness_key": "sample:peridotite"
        },
        {
          "row_index": 53,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 54,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 55,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 56,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 57,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 58,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 59,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 60,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 61,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 62,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 63,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 64,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 65,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 66,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 67,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 68,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 69,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 70,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 71,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 72,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 73,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 74,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 75,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 76,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 77,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 78,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 79,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 80,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 81,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 82,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 83,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 84,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 85,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 86,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 87,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 88,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 89,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 90,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 91,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 92,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 93,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 94,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 95,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 96,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 97,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 98,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 99,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 100,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 101,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 102,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 103,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 104,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 105,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 106,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 107,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 108,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 109,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 110,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 111,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 112,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 113,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 114,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 115,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 116,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 117,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 118,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 119,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 120,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 121,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 122,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 123,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 124,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 125,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 126,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 127,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 128,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 129,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 130,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 131,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 132,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 133,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 134,
          "witness_key": "claim:s-wave-delays-removed"
        },
        {
          "row_index": 135,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 136,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 137,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 138,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 139,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 140,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 141,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 142,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 143,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 144,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 145,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 146,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 147,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 148,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 149,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 150,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 151,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 152,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 153,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 154,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 155,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 156,
          "witness_key": "obs:events-identified-760"
        },
        {
          "row_index": 157,
          "witness_key": "obs:fm-new-3"
        },
        {
          "row_index": 158,
          "witness_key": "obs:fm-previous-3"
        },
        {
          "row_index": 159,
          "witness_key": "obs:fm-total-6"
        },
        {
          "row_index": 160,
          "witness_key": "obs:forced-depth-subset"
        },
        {
          "row_index": 161,
          "witness_key": "obs:located-514"
        },
        {
          "row_index": 162,
          "witness_key": "obs:magnitude-groups"
        },
        {
          "row_index": 163,
          "witness_key": "obs:obs-deployed-19"
        },
        {
          "row_index": 164,
          "witness_key": "obs:obs-useful-17"
        },
        {
          "row_index": 165,
          "witness_key": "obs:quality-categories"
        },
        {
          "row_index": 166,
          "witness_key": "obs:relocated-364"
        },
        {
          "row_index": 167,
          "witness_key": "obs:romanche-2016-subevents"
        },
        {
          "row_index": 168,
          "witness_key": "obs:subsection-count"
        },
        {
          "row_index": 169,
          "witness_key": "obs:velest-subdataset"
        },
        {
          "row_index": 170,
          "witness_key": "obs:velocity-models-five"
        },
        {
          "row_index": 171,
          "witness_key": "obs:well-relocated-276"
        },
        {
          "row_index": 172,
          "witness_key": "ratio:co2-ba"
        },
        {
          "row_index": 173,
          "witness_key": "ratio:co2-rb"
        },
        {
          "row_index": 174,
          "witness_key": "obs:abstract-co2-primary"
        },
        {
          "row_index": 175,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 176,
          "witness_key": "obs:eq-atlantic-co2-average"
        },
        {
          "row_index": 177,
          "witness_key": "obs:eq-atlantic-co2-max"
        },
        {
          "row_index": 178,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 179,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 180,
          "witness_key": "obs:axial-event-depth-stable"
        },
        {
          "row_index": 181,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 182,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 183,
          "witness_key": "obs:cluster-depth-west"
        },
        {
          "row_index": 184,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 185,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 186,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 187,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 188,
          "witness_key": "obs:criteria-met-fraction"
        },
        {
          "row_index": 189,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 190,
          "witness_key": "obs:criterion-gap"
        },
        {
          "row_index": 191,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 192,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 193,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 194,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 195,
          "witness_key": "obs:degassing-depth-range"
        },
        {
          "row_index": 196,
          "witness_key": "obs:depth-uncertainty-cap"
        },
        {
          "row_index": 197,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 198,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 199,
          "witness_key": "obs:expected-brittle-thickness"
        },
        {
          "row_index": 200,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 201,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 202,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 203,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 204,
          "witness_key": "obs:fig3e-elevation-scale"
        },
        {
          "row_index": 205,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 206,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 207,
          "witness_key": "obs:fm-gap"
        },
        {
          "row_index": 208,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 209,
          "witness_key": "obs:fm-polarities"
        },
        {
          "row_index": 210,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 211,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 212,
          "witness_key": "obs:forced-depth-range"
        },
        {
          "row_index": 213,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 214,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 215,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 216,
          "witness_key": "obs:horizontal-uncertainty-cap"
        },
        {
          "row_index": 217,
          "witness_key": "obs:lithospheric-age-interval"
        },
        {
          "row_index": 218,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 219,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 220,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 221,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 222,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 223,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 224,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 225,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 226,
          "witness_key": "obs:min-obs-per-event"
        },
        {
          "row_index": 227,
          "witness_key": "obs:model1-depth"
        },
        {
          "row_index": 228,
          "witness_key": "obs:model1-p-velocity"
        },
        {
          "row_index": 229,
          "witness_key": "obs:occ-transect-halfwidth"
        },
        {
          "row_index": 230,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 231,
          "witness_key": "obs:perturbed-deep-events"
        },
        {
          "row_index": 232,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 233,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 234,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 235,
          "witness_key": "obs:quality-a-uncertainty"
        },
        {
          "row_index": 236,
          "witness_key": "obs:quality-b-uncertainty"
        },
        {
          "row_index": 237,
          "witness_key": "obs:quality-c-uncertainty"
        },
        {
          "row_index": 238,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 239,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 240,
          "witness_key": "obs:refraction-constraint-depth"
        },
        {
          "row_index": 241,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 242,
          "witness_key": "obs:relocation-iterations"
        },
        {
          "row_index": 243,
          "witness_key": "obs:relocation-obs-count"
        },
        {
          "row_index": 244,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 245,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 246,
          "witness_key": "obs:rms-residual-cap"
        },
        {
          "row_index": 247,
          "witness_key": "obs:solubility-temperature"
        },
        {
          "row_index": 248,
          "witness_key": "obs:station-gap-cap"
        },
        {
          "row_index": 249,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 250,
          "witness_key": "obs:subdataset-arrivals"
        },
        {
          "row_index": 251,
          "witness_key": "obs:subdataset-gap"
        },
        {
          "row_index": 252,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 253,
          "witness_key": "obs:velest-iterations"
        },
        {
          "row_index": 254,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 255,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 256,
          "witness_key": "rel:askja-in-iceland"
        },
        {
          "row_index": 257,
          "witness_key": "rel:fagradalsfjall-in-iceland"
        },
        {
          "row_index": 258,
          "witness_key": "rel:logachev-of-knipovich"
        },
        {
          "row_index": 259,
          "witness_key": "rel:mar-in-eq-atlantic"
        },
        {
          "row_index": 260,
          "witness_key": "rel:marseg-bounded-chain"
        },
        {
          "row_index": 261,
          "witness_key": "rel:marseg-bounded-romanche"
        },
        {
          "row_index": 262,
          "witness_key": "rel:mayotte-in-indian-ocean"
        },
        {
          "row_index": 263,
          "witness_key": "rel:occ-on-mar"
        },
        {
          "row_index": 264,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 265,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 266,
          "witness_key": "rel:romanche-faults-in-tf"
        },
        {
          "row_index": 267,
          "witness_key": "rel:vent-field-on-ntd1"
        },
        {
          "row_index": 268,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 269,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 270,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 271,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 272,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 273,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 274,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 275,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 276,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 277,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 278,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 279,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 280,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 281,
          "witness_key": "obs:mar-events-317"
        },
        {
          "row_index": 282,
          "witness_key": "obs:romanche-events-197"
        },
        {
          "row_index": 283,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 284,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 285,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 286,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 287,
          "witness_key": "obs:co2-calc-rc2"
        },
        {
          "row_index": 288,
          "witness_key": "obs:co2-calc-rc3"
        },
        {
          "row_index": 289,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 290,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 291,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 292,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 293,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 294,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 295,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 296,
          "witness_key": "obs:rc2-ba"
        },
        {
          "row_index": 297,
          "witness_key": "obs:rc2-rb"
        },
        {
          "row_index": 298,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 299,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 300,
          "witness_key": "obs:bdb-at-ntd2"
        },
        {
          "row_index": 301,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 302,
          "witness_key": "obs:bdb-isotherm-fig6"
        },
        {
          "row_index": 303,
          "witness_key": "obs:bdb-isotherm-slow"
        },
        {
          "row_index": 304,
          "witness_key": "obs:bdb-isotherms-cold"
        },
        {
          "row_index": 305,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 306,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 307,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 308,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 309,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 310,
          "witness_key": "obs:deep-eq-rc2-1619"
        },
        {
          "row_index": 311,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 312,
          "witness_key": "obs:depth-range-ntd2"
        },
        {
          "row_index": 313,
          "witness_key": "obs:depth-range-occ"
        },
        {
          "row_index": 314,
          "witness_key": "obs:hot-mantle-temperature"
        },
        {
          "row_index": 315,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 316,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 317,
          "witness_key": "obs:mantle-temperature-rc2"
        },
        {
          "row_index": 318,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 319,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 320,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 321,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 322,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 323,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 324,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 325,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 326,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 327,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 328,
          "witness_key": "obs:subsolidus-temperature"
        },
        {
          "row_index": 329,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 330,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 331,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 332,
          "witness_key": "obs:obs-no-data"
        },
        {
          "row_index": 333,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 334,
          "witness_key": "obs:vp-vs-test-range"
        }
      ]
    },
    {
      "question_id": "CQ-T3-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One observation row carries the range, the unit, the pre-eruptive melt stage and the estimated status.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 289,
          "absent_reason": null,
          "note": "the pre-eruptive range for the studied segment"
        },
        {
          "semantic": "concentration_unit",
          "row_index": 289,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "melt_stage",
          "row_index": 289,
          "absent_reason": null,
          "note": "the row's melt stage is the pre-eruptive melt"
        },
        {
          "semantic": "estimation_status",
          "row_index": 289,
          "absent_reason": null,
          "note": "the row's determination is estimated"
        }
      ],
      "source_locators": [
        "page:5:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:axial-melt-lens"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 4,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 5,
          "witness_key": "feature:eq-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fracture-zone"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:hummocky"
        },
        {
          "row_index": 11,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 12,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 20,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 21,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 22,
          "witness_key": "feature:neo-volcanic-ridge"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 24,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 25,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 26,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 28,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 29,
          "witness_key": "feature:occ-surface-faults"
        },
        {
          "row_index": 30,
          "witness_key": "feature:occ-termination"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 36,
          "witness_key": "feature:romanche-faults"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:romanche-transform-valley"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rti-detachment"
        },
        {
          "row_index": 41,
          "witness_key": "feature:suspended-valley"
        },
        {
          "row_index": 42,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 43,
          "witness_key": "feature:swir-oblique"
        },
        {
          "row_index": 44,
          "witness_key": "feature:swir-segment-8"
        },
        {
          "row_index": 45,
          "witness_key": "feature:tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:transverse-ridge"
        },
        {
          "row_index": 47,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 48,
          "witness_key": "feature:west-indian-ocean"
        },
        {
          "row_index": 49,
          "witness_key": "sample:basalt"
        },
        {
          "row_index": 50,
          "witness_key": "sample:morb-obs-network"
        },
        {
          "row_index": 51,
          "witness_key": "sample:morb-rc2"
        },
        {
          "row_index": 52,
          "witness_key": "sample:peridotite"
        },
        {
          "row_index": 53,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 54,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 55,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 56,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 57,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 58,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 59,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 60,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 61,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 62,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 63,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 64,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 65,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 66,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 67,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 68,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 69,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 70,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 71,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 72,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 73,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 74,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 75,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 76,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 77,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 78,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 79,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 80,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 81,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 82,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 83,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 84,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 85,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 86,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 87,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 88,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 89,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 90,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 91,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 92,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 93,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 94,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 95,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 96,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 97,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 98,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 99,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 100,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 101,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 102,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 103,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 104,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 105,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 106,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 107,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 108,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 109,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 110,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 111,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 112,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 113,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 114,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 115,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 116,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 117,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 118,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 119,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 120,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 121,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 122,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 123,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 124,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 125,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 126,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 127,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 128,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 129,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 130,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 131,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 132,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 133,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 134,
          "witness_key": "claim:s-wave-delays-removed"
        },
        {
          "row_index": 135,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 136,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 137,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 138,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 139,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 140,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 141,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 142,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 143,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 144,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 145,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 146,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 147,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 148,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 149,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 150,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 151,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 152,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 153,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 154,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 155,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 156,
          "witness_key": "obs:events-identified-760"
        },
        {
          "row_index": 157,
          "witness_key": "obs:fm-new-3"
        },
        {
          "row_index": 158,
          "witness_key": "obs:fm-previous-3"
        },
        {
          "row_index": 159,
          "witness_key": "obs:fm-total-6"
        },
        {
          "row_index": 160,
          "witness_key": "obs:forced-depth-subset"
        },
        {
          "row_index": 161,
          "witness_key": "obs:located-514"
        },
        {
          "row_index": 162,
          "witness_key": "obs:magnitude-groups"
        },
        {
          "row_index": 163,
          "witness_key": "obs:obs-deployed-19"
        },
        {
          "row_index": 164,
          "witness_key": "obs:obs-useful-17"
        },
        {
          "row_index": 165,
          "witness_key": "obs:quality-categories"
        },
        {
          "row_index": 166,
          "witness_key": "obs:relocated-364"
        },
        {
          "row_index": 167,
          "witness_key": "obs:romanche-2016-subevents"
        },
        {
          "row_index": 168,
          "witness_key": "obs:subsection-count"
        },
        {
          "row_index": 169,
          "witness_key": "obs:velest-subdataset"
        },
        {
          "row_index": 170,
          "witness_key": "obs:velocity-models-five"
        },
        {
          "row_index": 171,
          "witness_key": "obs:well-relocated-276"
        },
        {
          "row_index": 172,
          "witness_key": "ratio:co2-ba"
        },
        {
          "row_index": 173,
          "witness_key": "ratio:co2-rb"
        },
        {
          "row_index": 174,
          "witness_key": "obs:abstract-co2-primary"
        },
        {
          "row_index": 175,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 176,
          "witness_key": "obs:eq-atlantic-co2-average"
        },
        {
          "row_index": 177,
          "witness_key": "obs:eq-atlantic-co2-max"
        },
        {
          "row_index": 178,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 179,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 180,
          "witness_key": "obs:axial-event-depth-stable"
        },
        {
          "row_index": 181,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 182,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 183,
          "witness_key": "obs:cluster-depth-west"
        },
        {
          "row_index": 184,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 185,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 186,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 187,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 188,
          "witness_key": "obs:criteria-met-fraction"
        },
        {
          "row_index": 189,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 190,
          "witness_key": "obs:criterion-gap"
        },
        {
          "row_index": 191,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 192,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 193,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 194,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 195,
          "witness_key": "obs:degassing-depth-range"
        },
        {
          "row_index": 196,
          "witness_key": "obs:depth-uncertainty-cap"
        },
        {
          "row_index": 197,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 198,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 199,
          "witness_key": "obs:expected-brittle-thickness"
        },
        {
          "row_index": 200,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 201,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 202,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 203,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 204,
          "witness_key": "obs:fig3e-elevation-scale"
        },
        {
          "row_index": 205,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 206,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 207,
          "witness_key": "obs:fm-gap"
        },
        {
          "row_index": 208,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 209,
          "witness_key": "obs:fm-polarities"
        },
        {
          "row_index": 210,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 211,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 212,
          "witness_key": "obs:forced-depth-range"
        },
        {
          "row_index": 213,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 214,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 215,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 216,
          "witness_key": "obs:horizontal-uncertainty-cap"
        },
        {
          "row_index": 217,
          "witness_key": "obs:lithospheric-age-interval"
        },
        {
          "row_index": 218,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 219,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 220,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 221,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 222,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 223,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 224,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 225,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 226,
          "witness_key": "obs:min-obs-per-event"
        },
        {
          "row_index": 227,
          "witness_key": "obs:model1-depth"
        },
        {
          "row_index": 228,
          "witness_key": "obs:model1-p-velocity"
        },
        {
          "row_index": 229,
          "witness_key": "obs:occ-transect-halfwidth"
        },
        {
          "row_index": 230,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 231,
          "witness_key": "obs:perturbed-deep-events"
        },
        {
          "row_index": 232,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 233,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 234,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 235,
          "witness_key": "obs:quality-a-uncertainty"
        },
        {
          "row_index": 236,
          "witness_key": "obs:quality-b-uncertainty"
        },
        {
          "row_index": 237,
          "witness_key": "obs:quality-c-uncertainty"
        },
        {
          "row_index": 238,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 239,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 240,
          "witness_key": "obs:refraction-constraint-depth"
        },
        {
          "row_index": 241,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 242,
          "witness_key": "obs:relocation-iterations"
        },
        {
          "row_index": 243,
          "witness_key": "obs:relocation-obs-count"
        },
        {
          "row_index": 244,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 245,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 246,
          "witness_key": "obs:rms-residual-cap"
        },
        {
          "row_index": 247,
          "witness_key": "obs:solubility-temperature"
        },
        {
          "row_index": 248,
          "witness_key": "obs:station-gap-cap"
        },
        {
          "row_index": 249,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 250,
          "witness_key": "obs:subdataset-arrivals"
        },
        {
          "row_index": 251,
          "witness_key": "obs:subdataset-gap"
        },
        {
          "row_index": 252,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 253,
          "witness_key": "obs:velest-iterations"
        },
        {
          "row_index": 254,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 255,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 256,
          "witness_key": "rel:askja-in-iceland"
        },
        {
          "row_index": 257,
          "witness_key": "rel:fagradalsfjall-in-iceland"
        },
        {
          "row_index": 258,
          "witness_key": "rel:logachev-of-knipovich"
        },
        {
          "row_index": 259,
          "witness_key": "rel:mar-in-eq-atlantic"
        },
        {
          "row_index": 260,
          "witness_key": "rel:marseg-bounded-chain"
        },
        {
          "row_index": 261,
          "witness_key": "rel:marseg-bounded-romanche"
        },
        {
          "row_index": 262,
          "witness_key": "rel:mayotte-in-indian-ocean"
        },
        {
          "row_index": 263,
          "witness_key": "rel:occ-on-mar"
        },
        {
          "row_index": 264,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 265,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 266,
          "witness_key": "rel:romanche-faults-in-tf"
        },
        {
          "row_index": 267,
          "witness_key": "rel:vent-field-on-ntd1"
        },
        {
          "row_index": 268,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 269,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 270,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 271,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 272,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 273,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 274,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 275,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 276,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 277,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 278,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 279,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 280,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 281,
          "witness_key": "obs:mar-events-317"
        },
        {
          "row_index": 282,
          "witness_key": "obs:romanche-events-197"
        },
        {
          "row_index": 283,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 284,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 285,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 286,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 287,
          "witness_key": "obs:co2-calc-rc2"
        },
        {
          "row_index": 288,
          "witness_key": "obs:co2-calc-rc3"
        },
        {
          "row_index": 289,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 290,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 291,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 292,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 293,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 294,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 295,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 296,
          "witness_key": "obs:rc2-ba"
        },
        {
          "row_index": 297,
          "witness_key": "obs:rc2-rb"
        },
        {
          "row_index": 298,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 299,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 300,
          "witness_key": "obs:bdb-at-ntd2"
        },
        {
          "row_index": 301,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 302,
          "witness_key": "obs:bdb-isotherm-fig6"
        },
        {
          "row_index": 303,
          "witness_key": "obs:bdb-isotherm-slow"
        },
        {
          "row_index": 304,
          "witness_key": "obs:bdb-isotherms-cold"
        },
        {
          "row_index": 305,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 306,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 307,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 308,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 309,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 310,
          "witness_key": "obs:deep-eq-rc2-1619"
        },
        {
          "row_index": 311,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 312,
          "witness_key": "obs:depth-range-ntd2"
        },
        {
          "row_index": 313,
          "witness_key": "obs:depth-range-occ"
        },
        {
          "row_index": 314,
          "witness_key": "obs:hot-mantle-temperature"
        },
        {
          "row_index": 315,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 316,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 317,
          "witness_key": "obs:mantle-temperature-rc2"
        },
        {
          "row_index": 318,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 319,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 320,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 321,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 322,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 323,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 324,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 325,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 326,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 327,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 328,
          "witness_key": "obs:subsolidus-temperature"
        },
        {
          "row_index": 329,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 330,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 331,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 332,
          "witness_key": "obs:obs-no-data"
        },
        {
          "row_index": 333,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 334,
          "witness_key": "obs:vp-vs-test-range"
        }
      ]
    },
    {
      "question_id": "CQ-T3-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The uncertainty row carries the value, the unit, the subject and the measured status, and a second count row names the relocated events of the final catalogue; nothing joins them.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 146,
          "absent_reason": null,
          "note": "the average horizontal uncertainty after relocation"
        },
        {
          "semantic": "length_unit",
          "row_index": 146,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "quantity_subject",
          "row_index": 146,
          "absent_reason": null,
          "note": "the quantity kind names the catalogue after earthquake relocation"
        },
        {
          "semantic": "derivation_status",
          "row_index": 146,
          "absent_reason": null,
          "note": "the row's modality is measured"
        },
        {
          "semantic": "event_set",
          "row_index": 140,
          "absent_reason": null,
          "note": "the count scope names the well relocated events that replaced the earlier locations in the final catalogue"
        }
      ],
      "source_locators": [
        "page:3:block:003",
        "page:3:block:004",
        "page:7:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "method:1d-inversion"
        },
        {
          "row_index": 1,
          "witness_key": "method:catalog-analysis"
        },
        {
          "row_index": 2,
          "witness_key": "method:dd-relocation"
        },
        {
          "row_index": 3,
          "witness_key": "method:double-difference"
        },
        {
          "row_index": 4,
          "witness_key": "method:earthquake-location"
        },
        {
          "row_index": 5,
          "witness_key": "method:focal-mechanism"
        },
        {
          "row_index": 6,
          "witness_key": "method:graphing"
        },
        {
          "row_index": 7,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 8,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 9,
          "witness_key": "method:oct-tree"
        },
        {
          "row_index": 10,
          "witness_key": "method:phase-picking"
        },
        {
          "row_index": 11,
          "witness_key": "method:sta-lta"
        },
        {
          "row_index": 12,
          "witness_key": "method:structural-analysis"
        },
        {
          "row_index": 13,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 14,
          "witness_key": "software:global-mapper"
        },
        {
          "row_index": 15,
          "witness_key": "software:gmt"
        },
        {
          "row_index": 16,
          "witness_key": "software:hash"
        },
        {
          "row_index": 17,
          "witness_key": "software:hypodd"
        },
        {
          "row_index": 18,
          "witness_key": "software:nonlinloc"
        },
        {
          "row_index": 19,
          "witness_key": "software:seisan"
        },
        {
          "row_index": 20,
          "witness_key": "software:velest"
        },
        {
          "row_index": 21,
          "witness_key": "software:zmap"
        },
        {
          "row_index": 22,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 23,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 24,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 25,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 26,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 27,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 28,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 29,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 30,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 31,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 32,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 33,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 34,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 35,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 36,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 37,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 38,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 39,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 40,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 41,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 42,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 43,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 44,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 45,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 46,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 47,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 48,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 49,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 50,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 51,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 52,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 53,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 54,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 55,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 56,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 57,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 58,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 59,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 60,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 61,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 62,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 63,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 64,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 65,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 66,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 67,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 68,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 69,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 70,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 71,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 72,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 73,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 74,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 75,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 76,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 77,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 78,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 79,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 80,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 81,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 82,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 83,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 84,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 85,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 86,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 87,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 88,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 89,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 90,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 91,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 92,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 93,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 94,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 95,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 96,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 97,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 98,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 99,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 100,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 101,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 102,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 103,
          "witness_key": "claim:s-wave-delays-removed"
        },
        {
          "row_index": 104,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 105,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 106,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 107,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 108,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 109,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 110,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 111,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 112,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 113,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 114,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 115,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 116,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 117,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 118,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 119,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 120,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 121,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 122,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 123,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 124,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 125,
          "witness_key": "obs:events-identified-760"
        },
        {
          "row_index": 126,
          "witness_key": "obs:fm-new-3"
        },
        {
          "row_index": 127,
          "witness_key": "obs:fm-previous-3"
        },
        {
          "row_index": 128,
          "witness_key": "obs:fm-total-6"
        },
        {
          "row_index": 129,
          "witness_key": "obs:forced-depth-subset"
        },
        {
          "row_index": 130,
          "witness_key": "obs:located-514"
        },
        {
          "row_index": 131,
          "witness_key": "obs:magnitude-groups"
        },
        {
          "row_index": 132,
          "witness_key": "obs:obs-deployed-19"
        },
        {
          "row_index": 133,
          "witness_key": "obs:obs-useful-17"
        },
        {
          "row_index": 134,
          "witness_key": "obs:quality-categories"
        },
        {
          "row_index": 135,
          "witness_key": "obs:relocated-364"
        },
        {
          "row_index": 136,
          "witness_key": "obs:romanche-2016-subevents"
        },
        {
          "row_index": 137,
          "witness_key": "obs:subsection-count"
        },
        {
          "row_index": 138,
          "witness_key": "obs:velest-subdataset"
        },
        {
          "row_index": 139,
          "witness_key": "obs:velocity-models-five"
        },
        {
          "row_index": 140,
          "witness_key": "obs:well-relocated-276"
        },
        {
          "row_index": 141,
          "witness_key": "obs:abstract-co2-primary"
        },
        {
          "row_index": 142,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 143,
          "witness_key": "obs:eq-atlantic-co2-average"
        },
        {
          "row_index": 144,
          "witness_key": "obs:eq-atlantic-co2-max"
        },
        {
          "row_index": 145,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 146,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 147,
          "witness_key": "obs:axial-event-depth-stable"
        },
        {
          "row_index": 148,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 149,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 150,
          "witness_key": "obs:cluster-depth-west"
        },
        {
          "row_index": 151,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 152,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 153,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 154,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 155,
          "witness_key": "obs:criteria-met-fraction"
        },
        {
          "row_index": 156,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 157,
          "witness_key": "obs:criterion-gap"
        },
        {
          "row_index": 158,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 159,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 160,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 161,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 162,
          "witness_key": "obs:degassing-depth-range"
        },
        {
          "row_index": 163,
          "witness_key": "obs:depth-uncertainty-cap"
        },
        {
          "row_index": 164,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 165,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 166,
          "witness_key": "obs:expected-brittle-thickness"
        },
        {
          "row_index": 167,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 168,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 169,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 170,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 171,
          "witness_key": "obs:fig3e-elevation-scale"
        },
        {
          "row_index": 172,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 173,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 174,
          "witness_key": "obs:fm-gap"
        },
        {
          "row_index": 175,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 176,
          "witness_key": "obs:fm-polarities"
        },
        {
          "row_index": 177,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 178,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 179,
          "witness_key": "obs:forced-depth-range"
        },
        {
          "row_index": 180,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 181,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 182,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 183,
          "witness_key": "obs:horizontal-uncertainty-cap"
        },
        {
          "row_index": 184,
          "witness_key": "obs:lithospheric-age-interval"
        },
        {
          "row_index": 185,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 186,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 187,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 188,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 189,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 190,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 191,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 192,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 193,
          "witness_key": "obs:min-obs-per-event"
        },
        {
          "row_index": 194,
          "witness_key": "obs:model1-depth"
        },
        {
          "row_index": 195,
          "witness_key": "obs:model1-p-velocity"
        },
        {
          "row_index": 196,
          "witness_key": "obs:occ-transect-halfwidth"
        },
        {
          "row_index": 197,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 198,
          "witness_key": "obs:perturbed-deep-events"
        },
        {
          "row_index": 199,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 200,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 201,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 202,
          "witness_key": "obs:quality-a-uncertainty"
        },
        {
          "row_index": 203,
          "witness_key": "obs:quality-b-uncertainty"
        },
        {
          "row_index": 204,
          "witness_key": "obs:quality-c-uncertainty"
        },
        {
          "row_index": 205,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 206,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 207,
          "witness_key": "obs:refraction-constraint-depth"
        },
        {
          "row_index": 208,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 209,
          "witness_key": "obs:relocation-iterations"
        },
        {
          "row_index": 210,
          "witness_key": "obs:relocation-obs-count"
        },
        {
          "row_index": 211,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 212,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 213,
          "witness_key": "obs:rms-residual-cap"
        },
        {
          "row_index": 214,
          "witness_key": "obs:solubility-temperature"
        },
        {
          "row_index": 215,
          "witness_key": "obs:station-gap-cap"
        },
        {
          "row_index": 216,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 217,
          "witness_key": "obs:subdataset-arrivals"
        },
        {
          "row_index": 218,
          "witness_key": "obs:subdataset-gap"
        },
        {
          "row_index": 219,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 220,
          "witness_key": "obs:velest-iterations"
        },
        {
          "row_index": 221,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 222,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 223,
          "witness_key": "rel:globalmapper-used-for-structural"
        },
        {
          "row_index": 224,
          "witness_key": "rel:gmt-used-for-graphing"
        },
        {
          "row_index": 225,
          "witness_key": "rel:hash-used-for-fm"
        },
        {
          "row_index": 226,
          "witness_key": "rel:hypodd-used-for-relocation"
        },
        {
          "row_index": 227,
          "witness_key": "rel:nonlinloc-used-for-octtree"
        },
        {
          "row_index": 228,
          "witness_key": "rel:seisan-used-for-picking"
        },
        {
          "row_index": 229,
          "witness_key": "rel:seisan-used-for-stalta"
        },
        {
          "row_index": 230,
          "witness_key": "rel:velest-used-for-inversion"
        },
        {
          "row_index": 231,
          "witness_key": "rel:zmap-used-for-catalog"
        },
        {
          "row_index": 232,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 233,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 234,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 235,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 236,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 237,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 238,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 239,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 240,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 241,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 242,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 243,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 244,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 245,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 246,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 247,
          "witness_key": "obs:mar-events-317"
        },
        {
          "row_index": 248,
          "witness_key": "obs:obs-no-data"
        },
        {
          "row_index": 249,
          "witness_key": "obs:romanche-events-197"
        },
        {
          "row_index": 250,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 251,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 252,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 253,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 254,
          "witness_key": "obs:co2-calc-rc2"
        },
        {
          "row_index": 255,
          "witness_key": "obs:co2-calc-rc3"
        },
        {
          "row_index": 256,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 257,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 258,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 259,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 260,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 261,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 262,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 263,
          "witness_key": "obs:rc2-ba"
        },
        {
          "row_index": 264,
          "witness_key": "obs:rc2-rb"
        },
        {
          "row_index": 265,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 266,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 267,
          "witness_key": "obs:bdb-at-ntd2"
        },
        {
          "row_index": 268,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 269,
          "witness_key": "obs:bdb-isotherm-fig6"
        },
        {
          "row_index": 270,
          "witness_key": "obs:bdb-isotherm-slow"
        },
        {
          "row_index": 271,
          "witness_key": "obs:bdb-isotherms-cold"
        },
        {
          "row_index": 272,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 273,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 274,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 275,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 276,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 277,
          "witness_key": "obs:deep-eq-rc2-1619"
        },
        {
          "row_index": 278,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 279,
          "witness_key": "obs:depth-range-ntd2"
        },
        {
          "row_index": 280,
          "witness_key": "obs:depth-range-occ"
        },
        {
          "row_index": 281,
          "witness_key": "obs:hot-mantle-temperature"
        },
        {
          "row_index": 282,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 283,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 284,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 285,
          "witness_key": "obs:mantle-temperature-rc2"
        },
        {
          "row_index": 286,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 287,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 288,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 289,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 290,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 291,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 292,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 293,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 294,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 295,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 296,
          "witness_key": "obs:subsolidus-temperature"
        },
        {
          "row_index": 297,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 298,
          "witness_key": "obs:vp-vs-test-range"
        }
      ]
    },
    {
      "question_id": "CQ-T3-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The pressure row carries the value, its unit, the melt it describes and the modelled status, and the temperature row carries the temperature unit; nothing joins the two rows.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 153,
          "absent_reason": null,
          "note": "the saturation pressure"
        },
        {
          "semantic": "pressure_unit",
          "row_index": 153,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "temperature_unit",
          "row_index": 154,
          "absent_reason": null,
          "note": "the saturation temperature row"
        },
        {
          "semantic": "quantity_subject",
          "row_index": 153,
          "absent_reason": null,
          "note": "the quantity kind names the melt above the stated CO2 content"
        },
        {
          "semantic": "model_derived_status",
          "row_index": 153,
          "absent_reason": null,
          "note": "the row's determination is modelled, from the solubility model"
        }
      ],
      "source_locators": [
        "page:5:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "method:1d-inversion"
        },
        {
          "row_index": 1,
          "witness_key": "method:catalog-analysis"
        },
        {
          "row_index": 2,
          "witness_key": "method:dd-relocation"
        },
        {
          "row_index": 3,
          "witness_key": "method:double-difference"
        },
        {
          "row_index": 4,
          "witness_key": "method:earthquake-location"
        },
        {
          "row_index": 5,
          "witness_key": "method:focal-mechanism"
        },
        {
          "row_index": 6,
          "witness_key": "method:graphing"
        },
        {
          "row_index": 7,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 8,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 9,
          "witness_key": "method:oct-tree"
        },
        {
          "row_index": 10,
          "witness_key": "method:phase-picking"
        },
        {
          "row_index": 11,
          "witness_key": "method:sta-lta"
        },
        {
          "row_index": 12,
          "witness_key": "method:structural-analysis"
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
          "witness_key": "model:low-velocity"
        },
        {
          "row_index": 16,
          "witness_key": "model:minimum-1d"
        },
        {
          "row_index": 17,
          "witness_key": "model:model-1"
        },
        {
          "row_index": 18,
          "witness_key": "model:north-flank"
        },
        {
          "row_index": 19,
          "witness_key": "model:selected-1d"
        },
        {
          "row_index": 20,
          "witness_key": "model:south-flank"
        },
        {
          "row_index": 21,
          "witness_key": "model:thermal-model"
        },
        {
          "row_index": 22,
          "witness_key": "model:transform-valley"
        },
        {
          "row_index": 23,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 24,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 25,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 26,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 27,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 28,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 29,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 30,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 31,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 32,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 33,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 34,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 35,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 36,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 37,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 38,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 39,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 40,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 41,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 42,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 43,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 44,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 45,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 46,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 47,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 48,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 49,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 50,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 51,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 52,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 53,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 54,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 55,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 56,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 57,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 58,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 59,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 60,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 61,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 62,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 63,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 64,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 65,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 66,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 67,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 68,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 69,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 70,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 71,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 72,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 73,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 74,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 75,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 76,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 77,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 78,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 79,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 80,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 81,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 83,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 84,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 85,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 86,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 87,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 88,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 89,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 90,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 91,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 92,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 93,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 94,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 95,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 96,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 97,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 98,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 99,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 100,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 101,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 102,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 103,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 104,
          "witness_key": "claim:s-wave-delays-removed"
        },
        {
          "row_index": 105,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 106,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 107,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 108,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 109,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 110,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 111,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 112,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 113,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 114,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 115,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 116,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 117,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 118,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 119,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 120,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 121,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 122,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 123,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 124,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 125,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 126,
          "witness_key": "obs:events-identified-760"
        },
        {
          "row_index": 127,
          "witness_key": "obs:fm-new-3"
        },
        {
          "row_index": 128,
          "witness_key": "obs:fm-previous-3"
        },
        {
          "row_index": 129,
          "witness_key": "obs:fm-total-6"
        },
        {
          "row_index": 130,
          "witness_key": "obs:forced-depth-subset"
        },
        {
          "row_index": 131,
          "witness_key": "obs:located-514"
        },
        {
          "row_index": 132,
          "witness_key": "obs:magnitude-groups"
        },
        {
          "row_index": 133,
          "witness_key": "obs:obs-deployed-19"
        },
        {
          "row_index": 134,
          "witness_key": "obs:obs-useful-17"
        },
        {
          "row_index": 135,
          "witness_key": "obs:quality-categories"
        },
        {
          "row_index": 136,
          "witness_key": "obs:relocated-364"
        },
        {
          "row_index": 137,
          "witness_key": "obs:romanche-2016-subevents"
        },
        {
          "row_index": 138,
          "witness_key": "obs:subsection-count"
        },
        {
          "row_index": 139,
          "witness_key": "obs:velest-subdataset"
        },
        {
          "row_index": 140,
          "witness_key": "obs:velocity-models-five"
        },
        {
          "row_index": 141,
          "witness_key": "obs:well-relocated-276"
        },
        {
          "row_index": 142,
          "witness_key": "obs:abstract-co2-primary"
        },
        {
          "row_index": 143,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 144,
          "witness_key": "obs:eq-atlantic-co2-average"
        },
        {
          "row_index": 145,
          "witness_key": "obs:eq-atlantic-co2-max"
        },
        {
          "row_index": 146,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 147,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 148,
          "witness_key": "obs:axial-event-depth-stable"
        },
        {
          "row_index": 149,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 150,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 151,
          "witness_key": "obs:cluster-depth-west"
        },
        {
          "row_index": 152,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 153,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 154,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 155,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 156,
          "witness_key": "obs:criteria-met-fraction"
        },
        {
          "row_index": 157,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 158,
          "witness_key": "obs:criterion-gap"
        },
        {
          "row_index": 159,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 160,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 161,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 162,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 163,
          "witness_key": "obs:degassing-depth-range"
        },
        {
          "row_index": 164,
          "witness_key": "obs:depth-uncertainty-cap"
        },
        {
          "row_index": 165,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 166,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 167,
          "witness_key": "obs:expected-brittle-thickness"
        },
        {
          "row_index": 168,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 169,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 170,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 171,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 172,
          "witness_key": "obs:fig3e-elevation-scale"
        },
        {
          "row_index": 173,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 174,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 175,
          "witness_key": "obs:fm-gap"
        },
        {
          "row_index": 176,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 177,
          "witness_key": "obs:fm-polarities"
        },
        {
          "row_index": 178,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 179,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 180,
          "witness_key": "obs:forced-depth-range"
        },
        {
          "row_index": 181,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 182,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 183,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 184,
          "witness_key": "obs:horizontal-uncertainty-cap"
        },
        {
          "row_index": 185,
          "witness_key": "obs:lithospheric-age-interval"
        },
        {
          "row_index": 186,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 187,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 188,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 189,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 190,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 191,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 192,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 193,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 194,
          "witness_key": "obs:min-obs-per-event"
        },
        {
          "row_index": 195,
          "witness_key": "obs:model1-depth"
        },
        {
          "row_index": 196,
          "witness_key": "obs:model1-p-velocity"
        },
        {
          "row_index": 197,
          "witness_key": "obs:occ-transect-halfwidth"
        },
        {
          "row_index": 198,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 199,
          "witness_key": "obs:perturbed-deep-events"
        },
        {
          "row_index": 200,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 201,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 202,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 203,
          "witness_key": "obs:quality-a-uncertainty"
        },
        {
          "row_index": 204,
          "witness_key": "obs:quality-b-uncertainty"
        },
        {
          "row_index": 205,
          "witness_key": "obs:quality-c-uncertainty"
        },
        {
          "row_index": 206,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 207,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 208,
          "witness_key": "obs:refraction-constraint-depth"
        },
        {
          "row_index": 209,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 210,
          "witness_key": "obs:relocation-iterations"
        },
        {
          "row_index": 211,
          "witness_key": "obs:relocation-obs-count"
        },
        {
          "row_index": 212,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 213,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 214,
          "witness_key": "obs:rms-residual-cap"
        },
        {
          "row_index": 215,
          "witness_key": "obs:solubility-temperature"
        },
        {
          "row_index": 216,
          "witness_key": "obs:station-gap-cap"
        },
        {
          "row_index": 217,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 218,
          "witness_key": "obs:subdataset-arrivals"
        },
        {
          "row_index": 219,
          "witness_key": "obs:subdataset-gap"
        },
        {
          "row_index": 220,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 221,
          "witness_key": "obs:velest-iterations"
        },
        {
          "row_index": 222,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 223,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 224,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 225,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 226,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 227,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 228,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 229,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 230,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 231,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 232,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 233,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 234,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 235,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 236,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 237,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 238,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 239,
          "witness_key": "obs:mar-events-317"
        },
        {
          "row_index": 240,
          "witness_key": "obs:obs-no-data"
        },
        {
          "row_index": 241,
          "witness_key": "obs:romanche-events-197"
        },
        {
          "row_index": 242,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 243,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 244,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 245,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 246,
          "witness_key": "obs:co2-calc-rc2"
        },
        {
          "row_index": 247,
          "witness_key": "obs:co2-calc-rc3"
        },
        {
          "row_index": 248,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 249,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 250,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 251,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 252,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 253,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 254,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 255,
          "witness_key": "obs:rc2-ba"
        },
        {
          "row_index": 256,
          "witness_key": "obs:rc2-rb"
        },
        {
          "row_index": 257,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 258,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 259,
          "witness_key": "obs:bdb-at-ntd2"
        },
        {
          "row_index": 260,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 261,
          "witness_key": "obs:bdb-isotherm-fig6"
        },
        {
          "row_index": 262,
          "witness_key": "obs:bdb-isotherm-slow"
        },
        {
          "row_index": 263,
          "witness_key": "obs:bdb-isotherms-cold"
        },
        {
          "row_index": 264,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 265,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 266,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 267,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 268,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 269,
          "witness_key": "obs:deep-eq-rc2-1619"
        },
        {
          "row_index": 270,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 271,
          "witness_key": "obs:depth-range-ntd2"
        },
        {
          "row_index": 272,
          "witness_key": "obs:depth-range-occ"
        },
        {
          "row_index": 273,
          "witness_key": "obs:hot-mantle-temperature"
        },
        {
          "row_index": 274,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 275,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 276,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 277,
          "witness_key": "obs:mantle-temperature-rc2"
        },
        {
          "row_index": 278,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 279,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 280,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 281,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 282,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 283,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 284,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 285,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 286,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 287,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 288,
          "witness_key": "obs:subsolidus-temperature"
        },
        {
          "row_index": 289,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 290,
          "witness_key": "obs:vp-vs-test-range"
        }
      ]
    },
    {
      "question_id": "CQ-T4-01",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One claim row carries the mechanism, its preferred disposition, its hedged modality and its subject.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "causal_claim",
          "row_index": 165,
          "absent_reason": null,
          "note": "the proposed degassing mechanism"
        },
        {
          "semantic": "preferred_disposition",
          "row_index": 165,
          "absent_reason": null,
          "note": "the row's disposition is preferred"
        },
        {
          "semantic": "epistemic_modality",
          "row_index": 165,
          "absent_reason": null,
          "note": "the row's modality is hypothesised"
        },
        {
          "semantic": "claim_subject",
          "row_index": 165,
          "absent_reason": null,
          "note": "the row's subject is the segment with the deep earthquakes"
        }
      ],
      "source_locators": [
        "page:1:block:001",
        "page:5:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:axial-melt-lens"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 4,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 5,
          "witness_key": "feature:eq-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fracture-zone"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:hummocky"
        },
        {
          "row_index": 11,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 12,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 20,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 21,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 22,
          "witness_key": "feature:neo-volcanic-ridge"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 24,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 25,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 26,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 28,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 29,
          "witness_key": "feature:occ-surface-faults"
        },
        {
          "row_index": 30,
          "witness_key": "feature:occ-termination"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 36,
          "witness_key": "feature:romanche-faults"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:romanche-transform-valley"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rti-detachment"
        },
        {
          "row_index": 41,
          "witness_key": "feature:suspended-valley"
        },
        {
          "row_index": 42,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 43,
          "witness_key": "feature:swir-oblique"
        },
        {
          "row_index": 44,
          "witness_key": "feature:swir-segment-8"
        },
        {
          "row_index": 45,
          "witness_key": "feature:tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:transverse-ridge"
        },
        {
          "row_index": 47,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 48,
          "witness_key": "feature:west-indian-ocean"
        },
        {
          "row_index": 49,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 50,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 51,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 52,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 53,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 54,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 55,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 56,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 57,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 58,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 59,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 60,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 61,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 62,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 63,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 64,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 65,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 66,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 67,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 68,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 69,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 70,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 71,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 72,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 73,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 74,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 75,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 76,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 77,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 78,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 79,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 80,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 81,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 82,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 83,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 84,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 85,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 86,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 87,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 88,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 89,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 90,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 91,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 92,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 93,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 94,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 95,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 96,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 97,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 98,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 99,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 100,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 101,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 102,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 103,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 104,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 105,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 106,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 107,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 108,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 109,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 110,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 111,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 112,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 113,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 114,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 115,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 116,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 117,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 118,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 119,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 120,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 121,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 122,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 123,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 124,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 125,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 126,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 127,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 128,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 129,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 130,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 131,
          "witness_key": "claim:s-wave-delays-removed"
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
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 135,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 136,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 137,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 138,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 139,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 140,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 141,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 142,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 143,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 144,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 145,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 146,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 147,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 148,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 149,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 150,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 151,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 152,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 153,
          "witness_key": "rel:askja-in-iceland"
        },
        {
          "row_index": 154,
          "witness_key": "rel:fagradalsfjall-in-iceland"
        },
        {
          "row_index": 155,
          "witness_key": "rel:logachev-of-knipovich"
        },
        {
          "row_index": 156,
          "witness_key": "rel:mar-in-eq-atlantic"
        },
        {
          "row_index": 157,
          "witness_key": "rel:marseg-bounded-chain"
        },
        {
          "row_index": 158,
          "witness_key": "rel:marseg-bounded-romanche"
        },
        {
          "row_index": 159,
          "witness_key": "rel:mayotte-in-indian-ocean"
        },
        {
          "row_index": 160,
          "witness_key": "rel:occ-on-mar"
        },
        {
          "row_index": 161,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 162,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 163,
          "witness_key": "rel:romanche-faults-in-tf"
        },
        {
          "row_index": 164,
          "witness_key": "rel:vent-field-on-ntd1"
        },
        {
          "row_index": 165,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 166,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 167,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 168,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 169,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 170,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 171,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 172,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 173,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 174,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 175,
          "witness_key": "claim:small-pressure-increase"
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
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 179,
          "witness_key": "claim:vp-vs-reasonable"
        }
      ]
    },
    {
      "question_id": "CQ-T4-02",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The candidate explanation and its declined disposition are carried by one claim row and a ground is carried by another, but that claim carries no subject reference: unlike the preferred explanation, this record has no subject field, so the subject of the declined claim is not modelled.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "candidate_mechanism",
          "row_index": 91,
          "absent_reason": null,
          "note": "the explanation associating the deep earthquakes with magmatic-tectonic activities, which the paper sets aside as melt movement"
        },
        {
          "semantic": "declined_disposition",
          "row_index": 91,
          "absent_reason": null,
          "note": "the row's disposition is not supported"
        },
        {
          "semantic": "stated_ground",
          "row_index": 174,
          "absent_reason": null,
          "note": "the absence of evidence for a current eruption in the axial valley"
        },
        {
          "semantic": "claim_subject",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "this explanation claim carries no subject reference, where the preferred explanation claim does"
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
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:axial-melt-lens"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 4,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 5,
          "witness_key": "feature:eq-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fracture-zone"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:hummocky"
        },
        {
          "row_index": 11,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 12,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 20,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 21,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 22,
          "witness_key": "feature:neo-volcanic-ridge"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 24,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 25,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 26,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 28,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 29,
          "witness_key": "feature:occ-surface-faults"
        },
        {
          "row_index": 30,
          "witness_key": "feature:occ-termination"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 36,
          "witness_key": "feature:romanche-faults"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:romanche-transform-valley"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rti-detachment"
        },
        {
          "row_index": 41,
          "witness_key": "feature:suspended-valley"
        },
        {
          "row_index": 42,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 43,
          "witness_key": "feature:swir-oblique"
        },
        {
          "row_index": 44,
          "witness_key": "feature:swir-segment-8"
        },
        {
          "row_index": 45,
          "witness_key": "feature:tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:transverse-ridge"
        },
        {
          "row_index": 47,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 48,
          "witness_key": "feature:west-indian-ocean"
        },
        {
          "row_index": 49,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 50,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 51,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 52,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 53,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 54,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 55,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 56,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 57,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 58,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 59,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 60,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 61,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 62,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 63,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 64,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 65,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 66,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 67,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 68,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 69,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 70,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 71,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 72,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 73,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 74,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 75,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 76,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 77,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 78,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 79,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 80,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 81,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 82,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 83,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 84,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 85,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 86,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 87,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 88,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 89,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 90,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 91,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 92,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 93,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 94,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 95,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 96,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 97,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 98,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 99,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 100,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 101,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 102,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 103,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 104,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 105,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 106,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 107,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 108,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 109,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 110,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 111,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 112,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 113,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 114,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 115,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 116,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 117,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 118,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 119,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 120,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 121,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 122,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 123,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 124,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 125,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 126,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 127,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 128,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 129,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 130,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 131,
          "witness_key": "claim:s-wave-delays-removed"
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
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 135,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 136,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 137,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 138,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 139,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 140,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 141,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 142,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 143,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 144,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 145,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 146,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 147,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 148,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 149,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 150,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 151,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 152,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 153,
          "witness_key": "rel:askja-in-iceland"
        },
        {
          "row_index": 154,
          "witness_key": "rel:fagradalsfjall-in-iceland"
        },
        {
          "row_index": 155,
          "witness_key": "rel:logachev-of-knipovich"
        },
        {
          "row_index": 156,
          "witness_key": "rel:mar-in-eq-atlantic"
        },
        {
          "row_index": 157,
          "witness_key": "rel:marseg-bounded-chain"
        },
        {
          "row_index": 158,
          "witness_key": "rel:marseg-bounded-romanche"
        },
        {
          "row_index": 159,
          "witness_key": "rel:mayotte-in-indian-ocean"
        },
        {
          "row_index": 160,
          "witness_key": "rel:occ-on-mar"
        },
        {
          "row_index": 161,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 162,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 163,
          "witness_key": "rel:romanche-faults-in-tf"
        },
        {
          "row_index": 164,
          "witness_key": "rel:vent-field-on-ntd1"
        },
        {
          "row_index": 165,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 166,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 167,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 168,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 169,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 170,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 171,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 172,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 173,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 174,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 175,
          "witness_key": "claim:small-pressure-increase"
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
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 179,
          "witness_key": "claim:vp-vs-reasonable"
        }
      ]
    },
    {
      "question_id": "CQ-T4-03",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The caveat and the claim it qualifies are both returned, but nothing carries a typed disposition marking a claim as a caveat: the ontology's disposition field appears only on the explanation claims, so the caveat's standing is only in the claim kind and in the words the graph withholds.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "qualified_claim",
          "row_index": 26,
          "absent_reason": null,
          "note": "the calculation of CO2 from the two proxies that the caveat qualifies, stated in the same block"
        },
        {
          "semantic": "stated_assumption",
          "row_index": 111,
          "absent_reason": null,
          "note": "the assumption that the trace elements reflect the mantle source"
        },
        {
          "semantic": "caveat_disposition",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "no returned row carries a typed disposition for a caveat; the only disposition field in the result is the hypothesis disposition of the explanation claims"
        },
        {
          "semantic": "claim_subject",
          "row_index": 26,
          "absent_reason": null,
          "note": "the row that is the estimation the caveat is attached to"
        }
      ],
      "source_locators": [
        "page:5:block:004"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "method:1d-inversion"
        },
        {
          "row_index": 1,
          "witness_key": "method:catalog-analysis"
        },
        {
          "row_index": 2,
          "witness_key": "method:dd-relocation"
        },
        {
          "row_index": 3,
          "witness_key": "method:double-difference"
        },
        {
          "row_index": 4,
          "witness_key": "method:earthquake-location"
        },
        {
          "row_index": 5,
          "witness_key": "method:focal-mechanism"
        },
        {
          "row_index": 6,
          "witness_key": "method:graphing"
        },
        {
          "row_index": 7,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 8,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 9,
          "witness_key": "method:oct-tree"
        },
        {
          "row_index": 10,
          "witness_key": "method:phase-picking"
        },
        {
          "row_index": 11,
          "witness_key": "method:sta-lta"
        },
        {
          "row_index": 12,
          "witness_key": "method:structural-analysis"
        },
        {
          "row_index": 13,
          "witness_key": "sample:basalt"
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
          "witness_key": "sample:peridotite"
        },
        {
          "row_index": 17,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 18,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 19,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 20,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 21,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 22,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 23,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 24,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 25,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 26,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 27,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 28,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 29,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 30,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 31,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 32,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 33,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 34,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 35,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 36,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 37,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 38,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 39,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 40,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 41,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 42,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 43,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 44,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 45,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 46,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 47,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 48,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 49,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 50,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 51,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 52,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 53,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 54,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 55,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 56,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 57,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 58,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 59,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 60,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 61,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 62,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 63,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 64,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 65,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 66,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 67,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 68,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 69,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 70,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 71,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 72,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 73,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 74,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 75,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 76,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 77,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 78,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 79,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 80,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 81,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 82,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 83,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 84,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 85,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 86,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 87,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 88,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 89,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 90,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 91,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 92,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 93,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 94,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 95,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 96,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 97,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 98,
          "witness_key": "claim:s-wave-delays-removed"
        },
        {
          "row_index": 99,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 100,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 101,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 102,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 103,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 104,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 105,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 106,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 107,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 108,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 109,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 110,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 111,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 112,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 113,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 114,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 115,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 116,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 117,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 118,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 119,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 120,
          "witness_key": "ratio:co2-ba"
        },
        {
          "row_index": 121,
          "witness_key": "ratio:co2-rb"
        },
        {
          "row_index": 122,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 123,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 124,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 125,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 126,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 127,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 128,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 129,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 130,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 131,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 132,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 133,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 134,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 135,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 136,
          "witness_key": "claim:vp-vs-reasonable"
        }
      ]
    },
    {
      "question_id": "CQ-T4-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "One claim row carries the existence statement, its negated modality, its subject and the spatial scope named in its claim kind.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "existence_claim",
          "row_index": 269,
          "absent_reason": null,
          "note": "the statement about active hydrothermal vents on the segment axis"
        },
        {
          "semantic": "negated_disposition",
          "row_index": 269,
          "absent_reason": null,
          "note": "the row's modality is negated, so the statement is one of absence"
        },
        {
          "semantic": "claim_subject",
          "row_index": 269,
          "absent_reason": null,
          "note": "the row's subject is the deep-earthquake segment"
        },
        {
          "semantic": "spatial_scope",
          "row_index": 269,
          "absent_reason": null,
          "note": "the claim kind names the segment axis"
        }
      ],
      "source_locators": [
        "page:3:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:axial-melt-lens"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 4,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 5,
          "witness_key": "feature:eq-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fracture-zone"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:hummocky"
        },
        {
          "row_index": 11,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 12,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 20,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 21,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 22,
          "witness_key": "feature:neo-volcanic-ridge"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 24,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 25,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 26,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 28,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 29,
          "witness_key": "feature:occ-surface-faults"
        },
        {
          "row_index": 30,
          "witness_key": "feature:occ-termination"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 36,
          "witness_key": "feature:romanche-faults"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:romanche-transform-valley"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rti-detachment"
        },
        {
          "row_index": 41,
          "witness_key": "feature:suspended-valley"
        },
        {
          "row_index": 42,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 43,
          "witness_key": "feature:swir-oblique"
        },
        {
          "row_index": 44,
          "witness_key": "feature:swir-segment-8"
        },
        {
          "row_index": 45,
          "witness_key": "feature:tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:transverse-ridge"
        },
        {
          "row_index": 47,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 48,
          "witness_key": "feature:west-indian-ocean"
        },
        {
          "row_index": 49,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 50,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 51,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 52,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 53,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 54,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 55,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 56,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 57,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 58,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 59,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 60,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 61,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 62,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 63,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 64,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 65,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 66,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 67,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 68,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 69,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 70,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 71,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 72,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 73,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 74,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 75,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 76,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 77,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 78,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 79,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 80,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 81,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 82,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 83,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 84,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 85,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 86,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 87,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 88,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 89,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 90,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 91,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 92,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 93,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 94,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 95,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 96,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 97,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 98,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 99,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 100,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 101,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 102,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 103,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 104,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 105,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 106,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 107,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 108,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 109,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 110,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 111,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 112,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 113,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 114,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 115,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 116,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 117,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 118,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 119,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 120,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 121,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 122,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 123,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 124,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 125,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 126,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 127,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 128,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 129,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 130,
          "witness_key": "claim:s-wave-delays-removed"
        },
        {
          "row_index": 131,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 132,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 133,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 134,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 135,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 136,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 137,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 138,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 139,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 140,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 141,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 142,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 143,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 144,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 145,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 146,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 147,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 148,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 149,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 150,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 151,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 152,
          "witness_key": "obs:events-identified-760"
        },
        {
          "row_index": 153,
          "witness_key": "obs:fm-new-3"
        },
        {
          "row_index": 154,
          "witness_key": "obs:fm-previous-3"
        },
        {
          "row_index": 155,
          "witness_key": "obs:fm-total-6"
        },
        {
          "row_index": 156,
          "witness_key": "obs:forced-depth-subset"
        },
        {
          "row_index": 157,
          "witness_key": "obs:located-514"
        },
        {
          "row_index": 158,
          "witness_key": "obs:magnitude-groups"
        },
        {
          "row_index": 159,
          "witness_key": "obs:obs-deployed-19"
        },
        {
          "row_index": 160,
          "witness_key": "obs:obs-useful-17"
        },
        {
          "row_index": 161,
          "witness_key": "obs:quality-categories"
        },
        {
          "row_index": 162,
          "witness_key": "obs:relocated-364"
        },
        {
          "row_index": 163,
          "witness_key": "obs:romanche-2016-subevents"
        },
        {
          "row_index": 164,
          "witness_key": "obs:subsection-count"
        },
        {
          "row_index": 165,
          "witness_key": "obs:velest-subdataset"
        },
        {
          "row_index": 166,
          "witness_key": "obs:velocity-models-five"
        },
        {
          "row_index": 167,
          "witness_key": "obs:well-relocated-276"
        },
        {
          "row_index": 168,
          "witness_key": "obs:abstract-co2-primary"
        },
        {
          "row_index": 169,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 170,
          "witness_key": "obs:eq-atlantic-co2-average"
        },
        {
          "row_index": 171,
          "witness_key": "obs:eq-atlantic-co2-max"
        },
        {
          "row_index": 172,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 173,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 174,
          "witness_key": "obs:axial-event-depth-stable"
        },
        {
          "row_index": 175,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 176,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 177,
          "witness_key": "obs:cluster-depth-west"
        },
        {
          "row_index": 178,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 179,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 180,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 181,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 182,
          "witness_key": "obs:criteria-met-fraction"
        },
        {
          "row_index": 183,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 184,
          "witness_key": "obs:criterion-gap"
        },
        {
          "row_index": 185,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 186,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 187,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 188,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 189,
          "witness_key": "obs:degassing-depth-range"
        },
        {
          "row_index": 190,
          "witness_key": "obs:depth-uncertainty-cap"
        },
        {
          "row_index": 191,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 192,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 193,
          "witness_key": "obs:expected-brittle-thickness"
        },
        {
          "row_index": 194,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 195,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 196,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 197,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 198,
          "witness_key": "obs:fig3e-elevation-scale"
        },
        {
          "row_index": 199,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 200,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 201,
          "witness_key": "obs:fm-gap"
        },
        {
          "row_index": 202,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 203,
          "witness_key": "obs:fm-polarities"
        },
        {
          "row_index": 204,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 205,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 206,
          "witness_key": "obs:forced-depth-range"
        },
        {
          "row_index": 207,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 208,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 209,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 210,
          "witness_key": "obs:horizontal-uncertainty-cap"
        },
        {
          "row_index": 211,
          "witness_key": "obs:lithospheric-age-interval"
        },
        {
          "row_index": 212,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 213,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 214,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 215,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 216,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 217,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 218,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 219,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 220,
          "witness_key": "obs:min-obs-per-event"
        },
        {
          "row_index": 221,
          "witness_key": "obs:model1-depth"
        },
        {
          "row_index": 222,
          "witness_key": "obs:model1-p-velocity"
        },
        {
          "row_index": 223,
          "witness_key": "obs:occ-transect-halfwidth"
        },
        {
          "row_index": 224,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 225,
          "witness_key": "obs:perturbed-deep-events"
        },
        {
          "row_index": 226,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 227,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 228,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 229,
          "witness_key": "obs:quality-a-uncertainty"
        },
        {
          "row_index": 230,
          "witness_key": "obs:quality-b-uncertainty"
        },
        {
          "row_index": 231,
          "witness_key": "obs:quality-c-uncertainty"
        },
        {
          "row_index": 232,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 233,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 234,
          "witness_key": "obs:refraction-constraint-depth"
        },
        {
          "row_index": 235,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 236,
          "witness_key": "obs:relocation-iterations"
        },
        {
          "row_index": 237,
          "witness_key": "obs:relocation-obs-count"
        },
        {
          "row_index": 238,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 239,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 240,
          "witness_key": "obs:rms-residual-cap"
        },
        {
          "row_index": 241,
          "witness_key": "obs:solubility-temperature"
        },
        {
          "row_index": 242,
          "witness_key": "obs:station-gap-cap"
        },
        {
          "row_index": 243,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 244,
          "witness_key": "obs:subdataset-arrivals"
        },
        {
          "row_index": 245,
          "witness_key": "obs:subdataset-gap"
        },
        {
          "row_index": 246,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 247,
          "witness_key": "obs:velest-iterations"
        },
        {
          "row_index": 248,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 249,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 250,
          "witness_key": "rel:askja-in-iceland"
        },
        {
          "row_index": 251,
          "witness_key": "rel:fagradalsfjall-in-iceland"
        },
        {
          "row_index": 252,
          "witness_key": "rel:logachev-of-knipovich"
        },
        {
          "row_index": 253,
          "witness_key": "rel:mar-in-eq-atlantic"
        },
        {
          "row_index": 254,
          "witness_key": "rel:marseg-bounded-chain"
        },
        {
          "row_index": 255,
          "witness_key": "rel:marseg-bounded-romanche"
        },
        {
          "row_index": 256,
          "witness_key": "rel:mayotte-in-indian-ocean"
        },
        {
          "row_index": 257,
          "witness_key": "rel:occ-on-mar"
        },
        {
          "row_index": 258,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 259,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 260,
          "witness_key": "rel:romanche-faults-in-tf"
        },
        {
          "row_index": 261,
          "witness_key": "rel:vent-field-on-ntd1"
        },
        {
          "row_index": 262,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 263,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 264,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 265,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 266,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 267,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 268,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 269,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 270,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 271,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 272,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 273,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 274,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 275,
          "witness_key": "obs:mar-events-317"
        },
        {
          "row_index": 276,
          "witness_key": "obs:romanche-events-197"
        },
        {
          "row_index": 277,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 278,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 279,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 280,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 281,
          "witness_key": "obs:co2-calc-rc2"
        },
        {
          "row_index": 282,
          "witness_key": "obs:co2-calc-rc3"
        },
        {
          "row_index": 283,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 284,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 285,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 286,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 287,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 288,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 289,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 290,
          "witness_key": "obs:rc2-ba"
        },
        {
          "row_index": 291,
          "witness_key": "obs:rc2-rb"
        },
        {
          "row_index": 292,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 293,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 294,
          "witness_key": "obs:bdb-at-ntd2"
        },
        {
          "row_index": 295,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 296,
          "witness_key": "obs:bdb-isotherm-fig6"
        },
        {
          "row_index": 297,
          "witness_key": "obs:bdb-isotherm-slow"
        },
        {
          "row_index": 298,
          "witness_key": "obs:bdb-isotherms-cold"
        },
        {
          "row_index": 299,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 300,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 301,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 302,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 303,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 304,
          "witness_key": "obs:deep-eq-rc2-1619"
        },
        {
          "row_index": 305,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 306,
          "witness_key": "obs:depth-range-ntd2"
        },
        {
          "row_index": 307,
          "witness_key": "obs:depth-range-occ"
        },
        {
          "row_index": 308,
          "witness_key": "obs:hot-mantle-temperature"
        },
        {
          "row_index": 309,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 310,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 311,
          "witness_key": "obs:mantle-temperature-rc2"
        },
        {
          "row_index": 312,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 313,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 314,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 315,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 316,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 317,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 318,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 319,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 320,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 321,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 322,
          "witness_key": "obs:subsolidus-temperature"
        },
        {
          "row_index": 323,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 324,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 325,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 326,
          "witness_key": "obs:obs-no-data"
        },
        {
          "row_index": 327,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 328,
          "witness_key": "obs:vp-vs-test-range"
        }
      ]
    },
    {
      "question_id": "CQ-T4-05",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The hedged claim about deep long-period earthquakes and its hypothesised modality are carried by one claim row and the stated limitation by another, but no returned row carries a typed disposition for that hedge: the hypothesis disposition field appears only on the explanation claims, whose subject is different.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "hedged_claim",
          "row_index": 20,
          "absent_reason": null,
          "note": "the claim that the mechanism may result in deep long-period earthquakes"
        },
        {
          "semantic": "hypothesised_disposition",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "this claim carries no disposition field; the dispositions in the result belong to the four explanation claims"
        },
        {
          "semantic": "epistemic_modality",
          "row_index": 20,
          "absent_reason": null,
          "note": "the row's modality is hypothesised, which is the qualification asked for"
        },
        {
          "semantic": "stated_limitation",
          "row_index": 59,
          "absent_reason": null,
          "note": "the claim that not all events are low-frequency and that more earthquakes would be required"
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
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 3,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 4,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 5,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 6,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 7,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 8,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 9,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 10,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 11,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 12,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 13,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 14,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 15,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 16,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 17,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 18,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 19,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 20,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 21,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 22,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 23,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 24,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 25,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 26,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 27,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 28,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 29,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 30,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 31,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 32,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 33,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 34,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 35,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 36,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 37,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 38,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 39,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 40,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 41,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 42,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 43,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 44,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 45,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 46,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 47,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 48,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 49,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 50,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 51,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 52,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 53,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 54,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 55,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 56,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 57,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 58,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 59,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 60,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 61,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 62,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 63,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 64,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 65,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 66,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 67,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 68,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 69,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 70,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 71,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 72,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 73,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 74,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 75,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 76,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 77,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 78,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 79,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 80,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 81,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 82,
          "witness_key": "claim:s-wave-delays-removed"
        },
        {
          "row_index": 83,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 84,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 85,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 86,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 87,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 88,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 89,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 90,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 91,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 92,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 93,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 94,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 95,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 96,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 97,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 98,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 99,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 100,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 101,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 102,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 103,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 104,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 105,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 106,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 107,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 108,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 109,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 110,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 111,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 112,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 113,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 114,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 115,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 116,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 117,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 118,
          "witness_key": "claim:vp-vs-reasonable"
        }
      ]
    },
    {
      "question_id": "CQ-T5-01",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The mechanism, a geochemical observation of the melts and the seismic depth observation are all returned, but nothing joins an observation to the claim it supports: the relation types in the result are locational, part-whole, bounding, use, funding and deposit, and no evidential relation is returned.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "causal_mechanism",
          "row_index": 202,
          "absent_reason": null,
          "note": "the proposed degassing mechanism"
        },
        {
          "semantic": "supporting_observation",
          "row_index": 223,
          "absent_reason": null,
          "note": "the calculated volatile content of the melts of that segment"
        },
        {
          "semantic": "geochemical_evidence",
          "row_index": 221,
          "absent_reason": null,
          "note": "the primary-melt content estimated from the barium proxy for the same segment"
        },
        {
          "semantic": "seismic_evidence",
          "row_index": 246,
          "absent_reason": null,
          "note": "the observed depth of the deep earthquakes beneath that segment axis"
        },
        {
          "semantic": "evidence_relation",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "no returned relation ties an observation to the claim it supports, and no such relation type appears in the result"
        }
      ],
      "source_locators": [
        "page:1:block:001",
        "page:5:block:002",
        "page:5:block:005",
        "page:8:block:007",
        "page:2:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 1,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 2,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 3,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 4,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 5,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 6,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 7,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 8,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 9,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 10,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 11,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 12,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 13,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 14,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 15,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 16,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 17,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 18,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 19,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 20,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 21,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 22,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 23,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 24,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 25,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 26,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 27,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 28,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 29,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 30,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 31,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 32,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 33,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 34,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 35,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 36,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 37,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 38,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 39,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 40,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 41,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 42,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 43,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 44,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 45,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 46,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 47,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 48,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 49,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 50,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 51,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 52,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 53,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 54,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 55,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 56,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 57,
          "witness_key": "claim:model1-inappropriate"
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
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 61,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 62,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 63,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 64,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 65,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 66,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 67,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 68,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 69,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 70,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 71,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 72,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 73,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 74,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 75,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 76,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 77,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 78,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 79,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 80,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 81,
          "witness_key": "claim:s-wave-delays-removed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 83,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 84,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 85,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 86,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 87,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 88,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 89,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 90,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 91,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 92,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 93,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 94,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 95,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 96,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 97,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 98,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 99,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 100,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 101,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 102,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 103,
          "witness_key": "obs:events-identified-760"
        },
        {
          "row_index": 104,
          "witness_key": "obs:fm-new-3"
        },
        {
          "row_index": 105,
          "witness_key": "obs:fm-previous-3"
        },
        {
          "row_index": 106,
          "witness_key": "obs:fm-total-6"
        },
        {
          "row_index": 107,
          "witness_key": "obs:forced-depth-subset"
        },
        {
          "row_index": 108,
          "witness_key": "obs:located-514"
        },
        {
          "row_index": 109,
          "witness_key": "obs:magnitude-groups"
        },
        {
          "row_index": 110,
          "witness_key": "obs:obs-deployed-19"
        },
        {
          "row_index": 111,
          "witness_key": "obs:obs-useful-17"
        },
        {
          "row_index": 112,
          "witness_key": "obs:quality-categories"
        },
        {
          "row_index": 113,
          "witness_key": "obs:relocated-364"
        },
        {
          "row_index": 114,
          "witness_key": "obs:romanche-2016-subevents"
        },
        {
          "row_index": 115,
          "witness_key": "obs:subsection-count"
        },
        {
          "row_index": 116,
          "witness_key": "obs:velest-subdataset"
        },
        {
          "row_index": 117,
          "witness_key": "obs:velocity-models-five"
        },
        {
          "row_index": 118,
          "witness_key": "obs:well-relocated-276"
        },
        {
          "row_index": 119,
          "witness_key": "obs:abstract-co2-primary"
        },
        {
          "row_index": 120,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 121,
          "witness_key": "obs:eq-atlantic-co2-average"
        },
        {
          "row_index": 122,
          "witness_key": "obs:eq-atlantic-co2-max"
        },
        {
          "row_index": 123,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 124,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 125,
          "witness_key": "obs:axial-event-depth-stable"
        },
        {
          "row_index": 126,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 127,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 128,
          "witness_key": "obs:cluster-depth-west"
        },
        {
          "row_index": 129,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 130,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 131,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 132,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 133,
          "witness_key": "obs:criteria-met-fraction"
        },
        {
          "row_index": 134,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 135,
          "witness_key": "obs:criterion-gap"
        },
        {
          "row_index": 136,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 137,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 138,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 139,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 140,
          "witness_key": "obs:degassing-depth-range"
        },
        {
          "row_index": 141,
          "witness_key": "obs:depth-uncertainty-cap"
        },
        {
          "row_index": 142,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 143,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 144,
          "witness_key": "obs:expected-brittle-thickness"
        },
        {
          "row_index": 145,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 146,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 147,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 148,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 149,
          "witness_key": "obs:fig3e-elevation-scale"
        },
        {
          "row_index": 150,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 151,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 152,
          "witness_key": "obs:fm-gap"
        },
        {
          "row_index": 153,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 154,
          "witness_key": "obs:fm-polarities"
        },
        {
          "row_index": 155,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 156,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 157,
          "witness_key": "obs:forced-depth-range"
        },
        {
          "row_index": 158,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 159,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 160,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 161,
          "witness_key": "obs:horizontal-uncertainty-cap"
        },
        {
          "row_index": 162,
          "witness_key": "obs:lithospheric-age-interval"
        },
        {
          "row_index": 163,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 164,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 165,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 166,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 167,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 168,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 169,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 170,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 171,
          "witness_key": "obs:min-obs-per-event"
        },
        {
          "row_index": 172,
          "witness_key": "obs:model1-depth"
        },
        {
          "row_index": 173,
          "witness_key": "obs:model1-p-velocity"
        },
        {
          "row_index": 174,
          "witness_key": "obs:occ-transect-halfwidth"
        },
        {
          "row_index": 175,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 176,
          "witness_key": "obs:perturbed-deep-events"
        },
        {
          "row_index": 177,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 178,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 179,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 180,
          "witness_key": "obs:quality-a-uncertainty"
        },
        {
          "row_index": 181,
          "witness_key": "obs:quality-b-uncertainty"
        },
        {
          "row_index": 182,
          "witness_key": "obs:quality-c-uncertainty"
        },
        {
          "row_index": 183,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 184,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 185,
          "witness_key": "obs:refraction-constraint-depth"
        },
        {
          "row_index": 186,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 187,
          "witness_key": "obs:relocation-iterations"
        },
        {
          "row_index": 188,
          "witness_key": "obs:relocation-obs-count"
        },
        {
          "row_index": 189,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 190,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 191,
          "witness_key": "obs:rms-residual-cap"
        },
        {
          "row_index": 192,
          "witness_key": "obs:solubility-temperature"
        },
        {
          "row_index": 193,
          "witness_key": "obs:station-gap-cap"
        },
        {
          "row_index": 194,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 195,
          "witness_key": "obs:subdataset-arrivals"
        },
        {
          "row_index": 196,
          "witness_key": "obs:subdataset-gap"
        },
        {
          "row_index": 197,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 198,
          "witness_key": "obs:velest-iterations"
        },
        {
          "row_index": 199,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 200,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 201,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 202,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 203,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 204,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 205,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 206,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 207,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 208,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 209,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 210,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 211,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 212,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 213,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 214,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 215,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 216,
          "witness_key": "obs:mar-events-317"
        },
        {
          "row_index": 217,
          "witness_key": "obs:obs-no-data"
        },
        {
          "row_index": 218,
          "witness_key": "obs:romanche-events-197"
        },
        {
          "row_index": 219,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 220,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 221,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 222,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 223,
          "witness_key": "obs:co2-calc-rc2"
        },
        {
          "row_index": 224,
          "witness_key": "obs:co2-calc-rc3"
        },
        {
          "row_index": 225,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 226,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 227,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 228,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 229,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 230,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 231,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 232,
          "witness_key": "obs:rc2-ba"
        },
        {
          "row_index": 233,
          "witness_key": "obs:rc2-rb"
        },
        {
          "row_index": 234,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 235,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 236,
          "witness_key": "obs:bdb-at-ntd2"
        },
        {
          "row_index": 237,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 238,
          "witness_key": "obs:bdb-isotherm-fig6"
        },
        {
          "row_index": 239,
          "witness_key": "obs:bdb-isotherm-slow"
        },
        {
          "row_index": 240,
          "witness_key": "obs:bdb-isotherms-cold"
        },
        {
          "row_index": 241,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 242,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 243,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 244,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 245,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 246,
          "witness_key": "obs:deep-eq-rc2-1619"
        },
        {
          "row_index": 247,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 248,
          "witness_key": "obs:depth-range-ntd2"
        },
        {
          "row_index": 249,
          "witness_key": "obs:depth-range-occ"
        },
        {
          "row_index": 250,
          "witness_key": "obs:hot-mantle-temperature"
        },
        {
          "row_index": 251,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 252,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 253,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 254,
          "witness_key": "obs:mantle-temperature-rc2"
        },
        {
          "row_index": 255,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 256,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 257,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 258,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 259,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 260,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 261,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 262,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 263,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 264,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 265,
          "witness_key": "obs:subsolidus-temperature"
        },
        {
          "row_index": 266,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 267,
          "witness_key": "obs:vp-vs-test-range"
        }
      ]
    },
    {
      "question_id": "CQ-T5-02",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "Both segments' calculated contents are returned with their unit and their subjects, but the comparison between them is not a field of any row: the source makes it in the sentence the two rows share, which the graph holds as a locator and a digest.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "comparison_relation",
          "row_index": null,
          "absent_reason": "WITHHELD_STATEMENT",
          "note": "the enrichment of one segment compared with the other is stated only inside the sentence both rows cite, held as a locator and a digest"
        },
        {
          "semantic": "first_quantity_subject",
          "row_index": 287,
          "absent_reason": null,
          "note": "the row whose subject is the segment with the deep earthquakes"
        },
        {
          "semantic": "second_quantity_subject",
          "row_index": 288,
          "absent_reason": null,
          "note": "the row whose subject is the adjacent segment to the south"
        },
        {
          "semantic": "bounded_quantity",
          "row_index": 287,
          "absent_reason": null,
          "note": "the calculated content of the first segment"
        },
        {
          "semantic": "concentration_unit",
          "row_index": 287,
          "absent_reason": null,
          "note": ""
        }
      ],
      "source_locators": [
        "page:5:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:axial-melt-lens"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 4,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 5,
          "witness_key": "feature:eq-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fracture-zone"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:hummocky"
        },
        {
          "row_index": 11,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 12,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 20,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 21,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 22,
          "witness_key": "feature:neo-volcanic-ridge"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 24,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 25,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 26,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 28,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 29,
          "witness_key": "feature:occ-surface-faults"
        },
        {
          "row_index": 30,
          "witness_key": "feature:occ-termination"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 36,
          "witness_key": "feature:romanche-faults"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:romanche-transform-valley"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rti-detachment"
        },
        {
          "row_index": 41,
          "witness_key": "feature:suspended-valley"
        },
        {
          "row_index": 42,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 43,
          "witness_key": "feature:swir-oblique"
        },
        {
          "row_index": 44,
          "witness_key": "feature:swir-segment-8"
        },
        {
          "row_index": 45,
          "witness_key": "feature:tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:transverse-ridge"
        },
        {
          "row_index": 47,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 48,
          "witness_key": "feature:west-indian-ocean"
        },
        {
          "row_index": 49,
          "witness_key": "sample:basalt"
        },
        {
          "row_index": 50,
          "witness_key": "sample:morb-obs-network"
        },
        {
          "row_index": 51,
          "witness_key": "sample:morb-rc2"
        },
        {
          "row_index": 52,
          "witness_key": "sample:peridotite"
        },
        {
          "row_index": 53,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 54,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 55,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 56,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 57,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 58,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 59,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 60,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 61,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 62,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 63,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 64,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 65,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 66,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 67,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 68,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 69,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 70,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 71,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 72,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 73,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 74,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 75,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 76,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 77,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 78,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 79,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 80,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 81,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 82,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 83,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 84,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 85,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 86,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 87,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 88,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 89,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 90,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 91,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 92,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 93,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 94,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 95,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 96,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 97,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 98,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 99,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 100,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 101,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 102,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 103,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 104,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 105,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 106,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 107,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 108,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 109,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 110,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 111,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 112,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 113,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 114,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 115,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 116,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 117,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 118,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 119,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 120,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 121,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 122,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 123,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 124,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 125,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 126,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 127,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 128,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 129,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 130,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 131,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 132,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 133,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 134,
          "witness_key": "claim:s-wave-delays-removed"
        },
        {
          "row_index": 135,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 136,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 137,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 138,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 139,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 140,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 141,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 142,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 143,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 144,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 145,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 146,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 147,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 148,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 149,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 150,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 151,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 152,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 153,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 154,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 155,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 156,
          "witness_key": "obs:events-identified-760"
        },
        {
          "row_index": 157,
          "witness_key": "obs:fm-new-3"
        },
        {
          "row_index": 158,
          "witness_key": "obs:fm-previous-3"
        },
        {
          "row_index": 159,
          "witness_key": "obs:fm-total-6"
        },
        {
          "row_index": 160,
          "witness_key": "obs:forced-depth-subset"
        },
        {
          "row_index": 161,
          "witness_key": "obs:located-514"
        },
        {
          "row_index": 162,
          "witness_key": "obs:magnitude-groups"
        },
        {
          "row_index": 163,
          "witness_key": "obs:obs-deployed-19"
        },
        {
          "row_index": 164,
          "witness_key": "obs:obs-useful-17"
        },
        {
          "row_index": 165,
          "witness_key": "obs:quality-categories"
        },
        {
          "row_index": 166,
          "witness_key": "obs:relocated-364"
        },
        {
          "row_index": 167,
          "witness_key": "obs:romanche-2016-subevents"
        },
        {
          "row_index": 168,
          "witness_key": "obs:subsection-count"
        },
        {
          "row_index": 169,
          "witness_key": "obs:velest-subdataset"
        },
        {
          "row_index": 170,
          "witness_key": "obs:velocity-models-five"
        },
        {
          "row_index": 171,
          "witness_key": "obs:well-relocated-276"
        },
        {
          "row_index": 172,
          "witness_key": "ratio:co2-ba"
        },
        {
          "row_index": 173,
          "witness_key": "ratio:co2-rb"
        },
        {
          "row_index": 174,
          "witness_key": "obs:abstract-co2-primary"
        },
        {
          "row_index": 175,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 176,
          "witness_key": "obs:eq-atlantic-co2-average"
        },
        {
          "row_index": 177,
          "witness_key": "obs:eq-atlantic-co2-max"
        },
        {
          "row_index": 178,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 179,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 180,
          "witness_key": "obs:axial-event-depth-stable"
        },
        {
          "row_index": 181,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 182,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 183,
          "witness_key": "obs:cluster-depth-west"
        },
        {
          "row_index": 184,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 185,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 186,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 187,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 188,
          "witness_key": "obs:criteria-met-fraction"
        },
        {
          "row_index": 189,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 190,
          "witness_key": "obs:criterion-gap"
        },
        {
          "row_index": 191,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 192,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 193,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 194,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 195,
          "witness_key": "obs:degassing-depth-range"
        },
        {
          "row_index": 196,
          "witness_key": "obs:depth-uncertainty-cap"
        },
        {
          "row_index": 197,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 198,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 199,
          "witness_key": "obs:expected-brittle-thickness"
        },
        {
          "row_index": 200,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 201,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 202,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 203,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 204,
          "witness_key": "obs:fig3e-elevation-scale"
        },
        {
          "row_index": 205,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 206,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 207,
          "witness_key": "obs:fm-gap"
        },
        {
          "row_index": 208,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 209,
          "witness_key": "obs:fm-polarities"
        },
        {
          "row_index": 210,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 211,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 212,
          "witness_key": "obs:forced-depth-range"
        },
        {
          "row_index": 213,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 214,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 215,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 216,
          "witness_key": "obs:horizontal-uncertainty-cap"
        },
        {
          "row_index": 217,
          "witness_key": "obs:lithospheric-age-interval"
        },
        {
          "row_index": 218,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 219,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 220,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 221,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 222,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 223,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 224,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 225,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 226,
          "witness_key": "obs:min-obs-per-event"
        },
        {
          "row_index": 227,
          "witness_key": "obs:model1-depth"
        },
        {
          "row_index": 228,
          "witness_key": "obs:model1-p-velocity"
        },
        {
          "row_index": 229,
          "witness_key": "obs:occ-transect-halfwidth"
        },
        {
          "row_index": 230,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 231,
          "witness_key": "obs:perturbed-deep-events"
        },
        {
          "row_index": 232,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 233,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 234,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 235,
          "witness_key": "obs:quality-a-uncertainty"
        },
        {
          "row_index": 236,
          "witness_key": "obs:quality-b-uncertainty"
        },
        {
          "row_index": 237,
          "witness_key": "obs:quality-c-uncertainty"
        },
        {
          "row_index": 238,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 239,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 240,
          "witness_key": "obs:refraction-constraint-depth"
        },
        {
          "row_index": 241,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 242,
          "witness_key": "obs:relocation-iterations"
        },
        {
          "row_index": 243,
          "witness_key": "obs:relocation-obs-count"
        },
        {
          "row_index": 244,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 245,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 246,
          "witness_key": "obs:rms-residual-cap"
        },
        {
          "row_index": 247,
          "witness_key": "obs:solubility-temperature"
        },
        {
          "row_index": 248,
          "witness_key": "obs:station-gap-cap"
        },
        {
          "row_index": 249,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 250,
          "witness_key": "obs:subdataset-arrivals"
        },
        {
          "row_index": 251,
          "witness_key": "obs:subdataset-gap"
        },
        {
          "row_index": 252,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 253,
          "witness_key": "obs:velest-iterations"
        },
        {
          "row_index": 254,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 255,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 256,
          "witness_key": "rel:askja-in-iceland"
        },
        {
          "row_index": 257,
          "witness_key": "rel:fagradalsfjall-in-iceland"
        },
        {
          "row_index": 258,
          "witness_key": "rel:logachev-of-knipovich"
        },
        {
          "row_index": 259,
          "witness_key": "rel:mar-in-eq-atlantic"
        },
        {
          "row_index": 260,
          "witness_key": "rel:marseg-bounded-chain"
        },
        {
          "row_index": 261,
          "witness_key": "rel:marseg-bounded-romanche"
        },
        {
          "row_index": 262,
          "witness_key": "rel:mayotte-in-indian-ocean"
        },
        {
          "row_index": 263,
          "witness_key": "rel:occ-on-mar"
        },
        {
          "row_index": 264,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 265,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 266,
          "witness_key": "rel:romanche-faults-in-tf"
        },
        {
          "row_index": 267,
          "witness_key": "rel:vent-field-on-ntd1"
        },
        {
          "row_index": 268,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 269,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 270,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 271,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 272,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 273,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 274,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 275,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 276,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 277,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 278,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 279,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 280,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 281,
          "witness_key": "obs:mar-events-317"
        },
        {
          "row_index": 282,
          "witness_key": "obs:romanche-events-197"
        },
        {
          "row_index": 283,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 284,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 285,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 286,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 287,
          "witness_key": "obs:co2-calc-rc2"
        },
        {
          "row_index": 288,
          "witness_key": "obs:co2-calc-rc3"
        },
        {
          "row_index": 289,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 290,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 291,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 292,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 293,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 294,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 295,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 296,
          "witness_key": "obs:rc2-ba"
        },
        {
          "row_index": 297,
          "witness_key": "obs:rc2-rb"
        },
        {
          "row_index": 298,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 299,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 300,
          "witness_key": "obs:bdb-at-ntd2"
        },
        {
          "row_index": 301,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 302,
          "witness_key": "obs:bdb-isotherm-fig6"
        },
        {
          "row_index": 303,
          "witness_key": "obs:bdb-isotherm-slow"
        },
        {
          "row_index": 304,
          "witness_key": "obs:bdb-isotherms-cold"
        },
        {
          "row_index": 305,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 306,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 307,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 308,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 309,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 310,
          "witness_key": "obs:deep-eq-rc2-1619"
        },
        {
          "row_index": 311,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 312,
          "witness_key": "obs:depth-range-ntd2"
        },
        {
          "row_index": 313,
          "witness_key": "obs:depth-range-occ"
        },
        {
          "row_index": 314,
          "witness_key": "obs:hot-mantle-temperature"
        },
        {
          "row_index": 315,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 316,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 317,
          "witness_key": "obs:mantle-temperature-rc2"
        },
        {
          "row_index": 318,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 319,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 320,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 321,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 322,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 323,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 324,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 325,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 326,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 327,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 328,
          "witness_key": "obs:subsolidus-temperature"
        },
        {
          "row_index": 329,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 330,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 331,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 332,
          "witness_key": "obs:obs-no-data"
        },
        {
          "row_index": 333,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 334,
          "witness_key": "obs:vp-vs-test-range"
        }
      ]
    },
    {
      "question_id": "CQ-T5-03",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The set of subsections, a maximum depth for one of them, the depth expected for the spreading rate and a claim stating the departure from that expectation are all returned; nothing joins them.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "subsection_set",
          "row_index": 165,
          "absent_reason": null,
          "note": "the count scope names the four subsections the studied portion is divided into"
        },
        {
          "semantic": "maximum_depth_claim",
          "row_index": 305,
          "absent_reason": null,
          "note": "the observed depth range beneath the segment that exceeds the expectation"
        },
        {
          "semantic": "expected_depth_claim",
          "row_index": 197,
          "absent_reason": null,
          "note": "the maximum depth expected for the full spreading rate"
        },
        {
          "semantic": "comparison_relation",
          "row_index": 95,
          "absent_reason": null,
          "note": "the claim kind states the departure of the observed maximum depth from the depth and spreading-rate relationship"
        }
      ],
      "source_locators": [
        "page:1:block:005",
        "page:2:block:006",
        "page:2:block:005",
        "page:2:block:007",
        "page:3:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:axial-melt-lens"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 4,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 5,
          "witness_key": "feature:eq-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fracture-zone"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:hummocky"
        },
        {
          "row_index": 11,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 12,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 20,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 21,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 22,
          "witness_key": "feature:neo-volcanic-ridge"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 24,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 25,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 26,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 28,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 29,
          "witness_key": "feature:occ-surface-faults"
        },
        {
          "row_index": 30,
          "witness_key": "feature:occ-termination"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 36,
          "witness_key": "feature:romanche-faults"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:romanche-transform-valley"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rti-detachment"
        },
        {
          "row_index": 41,
          "witness_key": "feature:suspended-valley"
        },
        {
          "row_index": 42,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 43,
          "witness_key": "feature:swir-oblique"
        },
        {
          "row_index": 44,
          "witness_key": "feature:swir-segment-8"
        },
        {
          "row_index": 45,
          "witness_key": "feature:tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:transverse-ridge"
        },
        {
          "row_index": 47,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 48,
          "witness_key": "feature:west-indian-ocean"
        },
        {
          "row_index": 49,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 50,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 51,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 52,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 53,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 54,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 55,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 56,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 57,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 58,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 59,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 60,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 61,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 62,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 63,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 64,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 65,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 66,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 67,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 68,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 69,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 70,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 71,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 72,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 73,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 74,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 75,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 76,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 77,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 78,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 79,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 80,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 81,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 82,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 83,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 84,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 85,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 86,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 87,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 88,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 89,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 90,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 91,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 92,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 93,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 94,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 95,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 96,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 97,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 98,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 99,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 100,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 101,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 102,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 103,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 104,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 105,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 106,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 107,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 108,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 109,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 110,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 111,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 112,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 113,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 114,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 115,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 116,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 117,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 118,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 119,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 120,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 121,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 122,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 123,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 124,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 125,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 126,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 127,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 128,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 129,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 130,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 131,
          "witness_key": "claim:s-wave-delays-removed"
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
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 135,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 136,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 137,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 138,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 139,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 140,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 141,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 142,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 143,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 144,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 145,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 146,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 147,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 148,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 149,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 150,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 151,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 152,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 153,
          "witness_key": "obs:events-identified-760"
        },
        {
          "row_index": 154,
          "witness_key": "obs:fm-new-3"
        },
        {
          "row_index": 155,
          "witness_key": "obs:fm-previous-3"
        },
        {
          "row_index": 156,
          "witness_key": "obs:fm-total-6"
        },
        {
          "row_index": 157,
          "witness_key": "obs:forced-depth-subset"
        },
        {
          "row_index": 158,
          "witness_key": "obs:located-514"
        },
        {
          "row_index": 159,
          "witness_key": "obs:magnitude-groups"
        },
        {
          "row_index": 160,
          "witness_key": "obs:obs-deployed-19"
        },
        {
          "row_index": 161,
          "witness_key": "obs:obs-useful-17"
        },
        {
          "row_index": 162,
          "witness_key": "obs:quality-categories"
        },
        {
          "row_index": 163,
          "witness_key": "obs:relocated-364"
        },
        {
          "row_index": 164,
          "witness_key": "obs:romanche-2016-subevents"
        },
        {
          "row_index": 165,
          "witness_key": "obs:subsection-count"
        },
        {
          "row_index": 166,
          "witness_key": "obs:velest-subdataset"
        },
        {
          "row_index": 167,
          "witness_key": "obs:velocity-models-five"
        },
        {
          "row_index": 168,
          "witness_key": "obs:well-relocated-276"
        },
        {
          "row_index": 169,
          "witness_key": "obs:abstract-co2-primary"
        },
        {
          "row_index": 170,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 171,
          "witness_key": "obs:eq-atlantic-co2-average"
        },
        {
          "row_index": 172,
          "witness_key": "obs:eq-atlantic-co2-max"
        },
        {
          "row_index": 173,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 174,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 175,
          "witness_key": "obs:axial-event-depth-stable"
        },
        {
          "row_index": 176,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 177,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 178,
          "witness_key": "obs:cluster-depth-west"
        },
        {
          "row_index": 179,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 180,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 181,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 182,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 183,
          "witness_key": "obs:criteria-met-fraction"
        },
        {
          "row_index": 184,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 185,
          "witness_key": "obs:criterion-gap"
        },
        {
          "row_index": 186,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 187,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 188,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 189,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 190,
          "witness_key": "obs:degassing-depth-range"
        },
        {
          "row_index": 191,
          "witness_key": "obs:depth-uncertainty-cap"
        },
        {
          "row_index": 192,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 193,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 194,
          "witness_key": "obs:expected-brittle-thickness"
        },
        {
          "row_index": 195,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 196,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 197,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 198,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 199,
          "witness_key": "obs:fig3e-elevation-scale"
        },
        {
          "row_index": 200,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 201,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 202,
          "witness_key": "obs:fm-gap"
        },
        {
          "row_index": 203,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 204,
          "witness_key": "obs:fm-polarities"
        },
        {
          "row_index": 205,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 206,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 207,
          "witness_key": "obs:forced-depth-range"
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
          "witness_key": "obs:horizontal-uncertainty-cap"
        },
        {
          "row_index": 212,
          "witness_key": "obs:lithospheric-age-interval"
        },
        {
          "row_index": 213,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 214,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 215,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 216,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 217,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 218,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 219,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 220,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 221,
          "witness_key": "obs:min-obs-per-event"
        },
        {
          "row_index": 222,
          "witness_key": "obs:model1-depth"
        },
        {
          "row_index": 223,
          "witness_key": "obs:model1-p-velocity"
        },
        {
          "row_index": 224,
          "witness_key": "obs:occ-transect-halfwidth"
        },
        {
          "row_index": 225,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 226,
          "witness_key": "obs:perturbed-deep-events"
        },
        {
          "row_index": 227,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 228,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 229,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 230,
          "witness_key": "obs:quality-a-uncertainty"
        },
        {
          "row_index": 231,
          "witness_key": "obs:quality-b-uncertainty"
        },
        {
          "row_index": 232,
          "witness_key": "obs:quality-c-uncertainty"
        },
        {
          "row_index": 233,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 234,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 235,
          "witness_key": "obs:refraction-constraint-depth"
        },
        {
          "row_index": 236,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 237,
          "witness_key": "obs:relocation-iterations"
        },
        {
          "row_index": 238,
          "witness_key": "obs:relocation-obs-count"
        },
        {
          "row_index": 239,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 240,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 241,
          "witness_key": "obs:rms-residual-cap"
        },
        {
          "row_index": 242,
          "witness_key": "obs:solubility-temperature"
        },
        {
          "row_index": 243,
          "witness_key": "obs:station-gap-cap"
        },
        {
          "row_index": 244,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 245,
          "witness_key": "obs:subdataset-arrivals"
        },
        {
          "row_index": 246,
          "witness_key": "obs:subdataset-gap"
        },
        {
          "row_index": 247,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 248,
          "witness_key": "obs:velest-iterations"
        },
        {
          "row_index": 249,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 250,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 251,
          "witness_key": "rel:askja-in-iceland"
        },
        {
          "row_index": 252,
          "witness_key": "rel:fagradalsfjall-in-iceland"
        },
        {
          "row_index": 253,
          "witness_key": "rel:logachev-of-knipovich"
        },
        {
          "row_index": 254,
          "witness_key": "rel:mar-in-eq-atlantic"
        },
        {
          "row_index": 255,
          "witness_key": "rel:marseg-bounded-chain"
        },
        {
          "row_index": 256,
          "witness_key": "rel:marseg-bounded-romanche"
        },
        {
          "row_index": 257,
          "witness_key": "rel:mayotte-in-indian-ocean"
        },
        {
          "row_index": 258,
          "witness_key": "rel:occ-on-mar"
        },
        {
          "row_index": 259,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 260,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 261,
          "witness_key": "rel:romanche-faults-in-tf"
        },
        {
          "row_index": 262,
          "witness_key": "rel:vent-field-on-ntd1"
        },
        {
          "row_index": 263,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 264,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 265,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 266,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 267,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 268,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 269,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 270,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 271,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 272,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 273,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 274,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 275,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 276,
          "witness_key": "obs:mar-events-317"
        },
        {
          "row_index": 277,
          "witness_key": "obs:romanche-events-197"
        },
        {
          "row_index": 278,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 279,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 280,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 281,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 282,
          "witness_key": "obs:co2-calc-rc2"
        },
        {
          "row_index": 283,
          "witness_key": "obs:co2-calc-rc3"
        },
        {
          "row_index": 284,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 285,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 286,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 287,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 288,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 289,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 290,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 291,
          "witness_key": "obs:rc2-ba"
        },
        {
          "row_index": 292,
          "witness_key": "obs:rc2-rb"
        },
        {
          "row_index": 293,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 294,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 295,
          "witness_key": "obs:bdb-at-ntd2"
        },
        {
          "row_index": 296,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 297,
          "witness_key": "obs:bdb-isotherm-fig6"
        },
        {
          "row_index": 298,
          "witness_key": "obs:bdb-isotherm-slow"
        },
        {
          "row_index": 299,
          "witness_key": "obs:bdb-isotherms-cold"
        },
        {
          "row_index": 300,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 301,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 302,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 303,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 304,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 305,
          "witness_key": "obs:deep-eq-rc2-1619"
        },
        {
          "row_index": 306,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 307,
          "witness_key": "obs:depth-range-ntd2"
        },
        {
          "row_index": 308,
          "witness_key": "obs:depth-range-occ"
        },
        {
          "row_index": 309,
          "witness_key": "obs:hot-mantle-temperature"
        },
        {
          "row_index": 310,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 311,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 312,
          "witness_key": "obs:mantle-temperature-rc2"
        },
        {
          "row_index": 313,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 314,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 315,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 316,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 317,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 318,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 319,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 320,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 321,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 322,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 323,
          "witness_key": "obs:subsolidus-temperature"
        },
        {
          "row_index": 324,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 325,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 326,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 327,
          "witness_key": "obs:obs-no-data"
        },
        {
          "row_index": 328,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 329,
          "witness_key": "obs:vp-vs-test-range"
        }
      ]
    },
    {
      "question_id": "CQ-T5-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The category set and its count are carried by one observation row, the selection for interpretation by a claim row and the located catalogue by another count row; nothing joins them.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "category_set",
          "row_index": 125,
          "absent_reason": null,
          "note": "the count scope names the categories the locations were classified into"
        },
        {
          "semantic": "category_count",
          "row_index": 125,
          "absent_reason": null,
          "note": "the count itself"
        },
        {
          "semantic": "selection_for_interpretation",
          "row_index": 13,
          "absent_reason": null,
          "note": "the claim that categories A and B are used for interpretation"
        },
        {
          "semantic": "earthquake_catalog",
          "row_index": 121,
          "absent_reason": null,
          "note": "the count of located earthquakes that were classified"
        }
      ],
      "source_locators": [
        "page:2:block:003",
        "page:7:block:008",
        "page:6:block:005"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "method:1d-inversion"
        },
        {
          "row_index": 1,
          "witness_key": "method:catalog-analysis"
        },
        {
          "row_index": 2,
          "witness_key": "method:dd-relocation"
        },
        {
          "row_index": 3,
          "witness_key": "method:double-difference"
        },
        {
          "row_index": 4,
          "witness_key": "method:earthquake-location"
        },
        {
          "row_index": 5,
          "witness_key": "method:focal-mechanism"
        },
        {
          "row_index": 6,
          "witness_key": "method:graphing"
        },
        {
          "row_index": 7,
          "witness_key": "method:local-magnitude"
        },
        {
          "row_index": 8,
          "witness_key": "method:nonlinear-location"
        },
        {
          "row_index": 9,
          "witness_key": "method:oct-tree"
        },
        {
          "row_index": 10,
          "witness_key": "method:phase-picking"
        },
        {
          "row_index": 11,
          "witness_key": "method:sta-lta"
        },
        {
          "row_index": 12,
          "witness_key": "method:structural-analysis"
        },
        {
          "row_index": 13,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 14,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 15,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 16,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 17,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 18,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 19,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 20,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 21,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 22,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 23,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 24,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 25,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 26,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 27,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 28,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 29,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 30,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 31,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 32,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 33,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 34,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 35,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 36,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 37,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 38,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 39,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 40,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 41,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 42,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 43,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 44,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 45,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 46,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 47,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 48,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 49,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 50,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 51,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 52,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 53,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 54,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 55,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 56,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 57,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 58,
          "witness_key": "claim:max-depth-not-following"
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
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 62,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 63,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 64,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 65,
          "witness_key": "claim:melt-freeze-lithosphere"
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
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 69,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 70,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 71,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 72,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 73,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 74,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 75,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 76,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 77,
          "witness_key": "claim:occ-dome-ruptures"
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
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 81,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 82,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 83,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 84,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 85,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 86,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 87,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 88,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 89,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 90,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 91,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 92,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 93,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 94,
          "witness_key": "claim:s-wave-delays-removed"
        },
        {
          "row_index": 95,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 96,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 97,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 98,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 99,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 100,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 101,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 102,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 103,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 104,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 105,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 106,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 107,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 108,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 109,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 110,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 111,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 112,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 113,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 114,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 115,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 116,
          "witness_key": "obs:events-identified-760"
        },
        {
          "row_index": 117,
          "witness_key": "obs:fm-new-3"
        },
        {
          "row_index": 118,
          "witness_key": "obs:fm-previous-3"
        },
        {
          "row_index": 119,
          "witness_key": "obs:fm-total-6"
        },
        {
          "row_index": 120,
          "witness_key": "obs:forced-depth-subset"
        },
        {
          "row_index": 121,
          "witness_key": "obs:located-514"
        },
        {
          "row_index": 122,
          "witness_key": "obs:magnitude-groups"
        },
        {
          "row_index": 123,
          "witness_key": "obs:obs-deployed-19"
        },
        {
          "row_index": 124,
          "witness_key": "obs:obs-useful-17"
        },
        {
          "row_index": 125,
          "witness_key": "obs:quality-categories"
        },
        {
          "row_index": 126,
          "witness_key": "obs:relocated-364"
        },
        {
          "row_index": 127,
          "witness_key": "obs:romanche-2016-subevents"
        },
        {
          "row_index": 128,
          "witness_key": "obs:subsection-count"
        },
        {
          "row_index": 129,
          "witness_key": "obs:velest-subdataset"
        },
        {
          "row_index": 130,
          "witness_key": "obs:velocity-models-five"
        },
        {
          "row_index": 131,
          "witness_key": "obs:well-relocated-276"
        },
        {
          "row_index": 132,
          "witness_key": "obs:abstract-co2-primary"
        },
        {
          "row_index": 133,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 134,
          "witness_key": "obs:eq-atlantic-co2-average"
        },
        {
          "row_index": 135,
          "witness_key": "obs:eq-atlantic-co2-max"
        },
        {
          "row_index": 136,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 137,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 138,
          "witness_key": "obs:axial-event-depth-stable"
        },
        {
          "row_index": 139,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 140,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 141,
          "witness_key": "obs:cluster-depth-west"
        },
        {
          "row_index": 142,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 143,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 144,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 145,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 146,
          "witness_key": "obs:criteria-met-fraction"
        },
        {
          "row_index": 147,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 148,
          "witness_key": "obs:criterion-gap"
        },
        {
          "row_index": 149,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 150,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 151,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 152,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 153,
          "witness_key": "obs:degassing-depth-range"
        },
        {
          "row_index": 154,
          "witness_key": "obs:depth-uncertainty-cap"
        },
        {
          "row_index": 155,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 156,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 157,
          "witness_key": "obs:expected-brittle-thickness"
        },
        {
          "row_index": 158,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 159,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 160,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 161,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 162,
          "witness_key": "obs:fig3e-elevation-scale"
        },
        {
          "row_index": 163,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 164,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 165,
          "witness_key": "obs:fm-gap"
        },
        {
          "row_index": 166,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 167,
          "witness_key": "obs:fm-polarities"
        },
        {
          "row_index": 168,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 169,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 170,
          "witness_key": "obs:forced-depth-range"
        },
        {
          "row_index": 171,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 172,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 173,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 174,
          "witness_key": "obs:horizontal-uncertainty-cap"
        },
        {
          "row_index": 175,
          "witness_key": "obs:lithospheric-age-interval"
        },
        {
          "row_index": 176,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 177,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 178,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 179,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 180,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 181,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 182,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 183,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 184,
          "witness_key": "obs:min-obs-per-event"
        },
        {
          "row_index": 185,
          "witness_key": "obs:model1-depth"
        },
        {
          "row_index": 186,
          "witness_key": "obs:model1-p-velocity"
        },
        {
          "row_index": 187,
          "witness_key": "obs:occ-transect-halfwidth"
        },
        {
          "row_index": 188,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 189,
          "witness_key": "obs:perturbed-deep-events"
        },
        {
          "row_index": 190,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 191,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 192,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 193,
          "witness_key": "obs:quality-a-uncertainty"
        },
        {
          "row_index": 194,
          "witness_key": "obs:quality-b-uncertainty"
        },
        {
          "row_index": 195,
          "witness_key": "obs:quality-c-uncertainty"
        },
        {
          "row_index": 196,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 197,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 198,
          "witness_key": "obs:refraction-constraint-depth"
        },
        {
          "row_index": 199,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 200,
          "witness_key": "obs:relocation-iterations"
        },
        {
          "row_index": 201,
          "witness_key": "obs:relocation-obs-count"
        },
        {
          "row_index": 202,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 203,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 204,
          "witness_key": "obs:rms-residual-cap"
        },
        {
          "row_index": 205,
          "witness_key": "obs:solubility-temperature"
        },
        {
          "row_index": 206,
          "witness_key": "obs:station-gap-cap"
        },
        {
          "row_index": 207,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 208,
          "witness_key": "obs:subdataset-arrivals"
        },
        {
          "row_index": 209,
          "witness_key": "obs:subdataset-gap"
        },
        {
          "row_index": 210,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 211,
          "witness_key": "obs:velest-iterations"
        },
        {
          "row_index": 212,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 213,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 214,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 215,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 216,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 217,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 218,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 219,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 220,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 221,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 222,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 223,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 224,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 225,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 226,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 227,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 228,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 229,
          "witness_key": "obs:mar-events-317"
        },
        {
          "row_index": 230,
          "witness_key": "obs:obs-no-data"
        },
        {
          "row_index": 231,
          "witness_key": "obs:romanche-events-197"
        },
        {
          "row_index": 232,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 233,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 234,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 235,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 236,
          "witness_key": "obs:co2-calc-rc2"
        },
        {
          "row_index": 237,
          "witness_key": "obs:co2-calc-rc3"
        },
        {
          "row_index": 238,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 239,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 240,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 241,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 242,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 243,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 244,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 245,
          "witness_key": "obs:rc2-ba"
        },
        {
          "row_index": 246,
          "witness_key": "obs:rc2-rb"
        },
        {
          "row_index": 247,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 248,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 249,
          "witness_key": "obs:bdb-at-ntd2"
        },
        {
          "row_index": 250,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 251,
          "witness_key": "obs:bdb-isotherm-fig6"
        },
        {
          "row_index": 252,
          "witness_key": "obs:bdb-isotherm-slow"
        },
        {
          "row_index": 253,
          "witness_key": "obs:bdb-isotherms-cold"
        },
        {
          "row_index": 254,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 255,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 256,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 257,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 258,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 259,
          "witness_key": "obs:deep-eq-rc2-1619"
        },
        {
          "row_index": 260,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 261,
          "witness_key": "obs:depth-range-ntd2"
        },
        {
          "row_index": 262,
          "witness_key": "obs:depth-range-occ"
        },
        {
          "row_index": 263,
          "witness_key": "obs:hot-mantle-temperature"
        },
        {
          "row_index": 264,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 265,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 266,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 267,
          "witness_key": "obs:mantle-temperature-rc2"
        },
        {
          "row_index": 268,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 269,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 270,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 271,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 272,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 273,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 274,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 275,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 276,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 277,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 278,
          "witness_key": "obs:subsolidus-temperature"
        },
        {
          "row_index": 279,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 280,
          "witness_key": "obs:vp-vs-test-range"
        }
      ]
    },
    {
      "question_id": "CQ-T5-05",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The candidate explanation with its declined disposition, the morphological inference and the off-axis seismicity observation are all returned, but nothing joins an observation to the explanation it argues against: no evidential relation type appears in the result.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "candidate_explanation",
          "row_index": 62,
          "absent_reason": null,
          "note": "the cold and thick lithosphere explanation"
        },
        {
          "semantic": "morphological_observation",
          "row_index": 125,
          "absent_reason": null,
          "note": "the inference from the axial morphology to a magmatic origin of that segment"
        },
        {
          "semantic": "seismic_observation",
          "row_index": 319,
          "absent_reason": null,
          "note": "the depth of the off-axis shallow microseismicity west of that segment axis"
        },
        {
          "semantic": "evidence_relation",
          "row_index": null,
          "absent_reason": "NOT_MODELLED",
          "note": "no returned relation ties an observation to the explanation it argues against"
        },
        {
          "semantic": "declined_disposition",
          "row_index": 62,
          "absent_reason": null,
          "note": "the explanation row's disposition is not supported"
        }
      ],
      "source_locators": [
        "page:3:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:axial-melt-lens"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 4,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 5,
          "witness_key": "feature:eq-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fracture-zone"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:hummocky"
        },
        {
          "row_index": 11,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 12,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 20,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 21,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 22,
          "witness_key": "feature:neo-volcanic-ridge"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 24,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 25,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 26,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 28,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 29,
          "witness_key": "feature:occ-surface-faults"
        },
        {
          "row_index": 30,
          "witness_key": "feature:occ-termination"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 36,
          "witness_key": "feature:romanche-faults"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:romanche-transform-valley"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rti-detachment"
        },
        {
          "row_index": 41,
          "witness_key": "feature:suspended-valley"
        },
        {
          "row_index": 42,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 43,
          "witness_key": "feature:swir-oblique"
        },
        {
          "row_index": 44,
          "witness_key": "feature:swir-segment-8"
        },
        {
          "row_index": 45,
          "witness_key": "feature:tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:transverse-ridge"
        },
        {
          "row_index": 47,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 48,
          "witness_key": "feature:west-indian-ocean"
        },
        {
          "row_index": 49,
          "witness_key": "event:romanche-2016"
        },
        {
          "row_index": 50,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 51,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 52,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 53,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 54,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 55,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 56,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 57,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 58,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 59,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 60,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 61,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 62,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 63,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 64,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 65,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 66,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 67,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 68,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 69,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 70,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 71,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 72,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 73,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 74,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 75,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 76,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 77,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 78,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 79,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 80,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 81,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 82,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 83,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 84,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 85,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 86,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 87,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 88,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 89,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 90,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 91,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 92,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 93,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 94,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 95,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 96,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 97,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 98,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 99,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 100,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 101,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 102,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 103,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 104,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 105,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 106,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 107,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 108,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 109,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 110,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 111,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 112,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 113,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 114,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 115,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 116,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 117,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 118,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 119,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 120,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 121,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 122,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 123,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 124,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 125,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 126,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 127,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 128,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 129,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 130,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 131,
          "witness_key": "claim:s-wave-delays-removed"
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
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 135,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 136,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 137,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 138,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 139,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 140,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 141,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 142,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 143,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 144,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 145,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 146,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 147,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 148,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 149,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 150,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 151,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 152,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 153,
          "witness_key": "obs:events-identified-760"
        },
        {
          "row_index": 154,
          "witness_key": "obs:fm-new-3"
        },
        {
          "row_index": 155,
          "witness_key": "obs:fm-previous-3"
        },
        {
          "row_index": 156,
          "witness_key": "obs:fm-total-6"
        },
        {
          "row_index": 157,
          "witness_key": "obs:forced-depth-subset"
        },
        {
          "row_index": 158,
          "witness_key": "obs:located-514"
        },
        {
          "row_index": 159,
          "witness_key": "obs:magnitude-groups"
        },
        {
          "row_index": 160,
          "witness_key": "obs:obs-deployed-19"
        },
        {
          "row_index": 161,
          "witness_key": "obs:obs-useful-17"
        },
        {
          "row_index": 162,
          "witness_key": "obs:quality-categories"
        },
        {
          "row_index": 163,
          "witness_key": "obs:relocated-364"
        },
        {
          "row_index": 164,
          "witness_key": "obs:romanche-2016-subevents"
        },
        {
          "row_index": 165,
          "witness_key": "obs:subsection-count"
        },
        {
          "row_index": 166,
          "witness_key": "obs:velest-subdataset"
        },
        {
          "row_index": 167,
          "witness_key": "obs:velocity-models-five"
        },
        {
          "row_index": 168,
          "witness_key": "obs:well-relocated-276"
        },
        {
          "row_index": 169,
          "witness_key": "obs:abstract-co2-primary"
        },
        {
          "row_index": 170,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 171,
          "witness_key": "obs:eq-atlantic-co2-average"
        },
        {
          "row_index": 172,
          "witness_key": "obs:eq-atlantic-co2-max"
        },
        {
          "row_index": 173,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 174,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 175,
          "witness_key": "obs:axial-event-depth-stable"
        },
        {
          "row_index": 176,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 177,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 178,
          "witness_key": "obs:cluster-depth-west"
        },
        {
          "row_index": 179,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 180,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 181,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 182,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 183,
          "witness_key": "obs:criteria-met-fraction"
        },
        {
          "row_index": 184,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 185,
          "witness_key": "obs:criterion-gap"
        },
        {
          "row_index": 186,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 187,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 188,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 189,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 190,
          "witness_key": "obs:degassing-depth-range"
        },
        {
          "row_index": 191,
          "witness_key": "obs:depth-uncertainty-cap"
        },
        {
          "row_index": 192,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 193,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 194,
          "witness_key": "obs:expected-brittle-thickness"
        },
        {
          "row_index": 195,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 196,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 197,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 198,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 199,
          "witness_key": "obs:fig3e-elevation-scale"
        },
        {
          "row_index": 200,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 201,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 202,
          "witness_key": "obs:fm-gap"
        },
        {
          "row_index": 203,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 204,
          "witness_key": "obs:fm-polarities"
        },
        {
          "row_index": 205,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 206,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 207,
          "witness_key": "obs:forced-depth-range"
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
          "witness_key": "obs:horizontal-uncertainty-cap"
        },
        {
          "row_index": 212,
          "witness_key": "obs:lithospheric-age-interval"
        },
        {
          "row_index": 213,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 214,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 215,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 216,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 217,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 218,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 219,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 220,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 221,
          "witness_key": "obs:min-obs-per-event"
        },
        {
          "row_index": 222,
          "witness_key": "obs:model1-depth"
        },
        {
          "row_index": 223,
          "witness_key": "obs:model1-p-velocity"
        },
        {
          "row_index": 224,
          "witness_key": "obs:occ-transect-halfwidth"
        },
        {
          "row_index": 225,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 226,
          "witness_key": "obs:perturbed-deep-events"
        },
        {
          "row_index": 227,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 228,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 229,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 230,
          "witness_key": "obs:quality-a-uncertainty"
        },
        {
          "row_index": 231,
          "witness_key": "obs:quality-b-uncertainty"
        },
        {
          "row_index": 232,
          "witness_key": "obs:quality-c-uncertainty"
        },
        {
          "row_index": 233,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 234,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 235,
          "witness_key": "obs:refraction-constraint-depth"
        },
        {
          "row_index": 236,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 237,
          "witness_key": "obs:relocation-iterations"
        },
        {
          "row_index": 238,
          "witness_key": "obs:relocation-obs-count"
        },
        {
          "row_index": 239,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 240,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 241,
          "witness_key": "obs:rms-residual-cap"
        },
        {
          "row_index": 242,
          "witness_key": "obs:solubility-temperature"
        },
        {
          "row_index": 243,
          "witness_key": "obs:station-gap-cap"
        },
        {
          "row_index": 244,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 245,
          "witness_key": "obs:subdataset-arrivals"
        },
        {
          "row_index": 246,
          "witness_key": "obs:subdataset-gap"
        },
        {
          "row_index": 247,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 248,
          "witness_key": "obs:velest-iterations"
        },
        {
          "row_index": 249,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 250,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 251,
          "witness_key": "rel:askja-in-iceland"
        },
        {
          "row_index": 252,
          "witness_key": "rel:fagradalsfjall-in-iceland"
        },
        {
          "row_index": 253,
          "witness_key": "rel:logachev-of-knipovich"
        },
        {
          "row_index": 254,
          "witness_key": "rel:mar-in-eq-atlantic"
        },
        {
          "row_index": 255,
          "witness_key": "rel:marseg-bounded-chain"
        },
        {
          "row_index": 256,
          "witness_key": "rel:marseg-bounded-romanche"
        },
        {
          "row_index": 257,
          "witness_key": "rel:mayotte-in-indian-ocean"
        },
        {
          "row_index": 258,
          "witness_key": "rel:occ-on-mar"
        },
        {
          "row_index": 259,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 260,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 261,
          "witness_key": "rel:romanche-faults-in-tf"
        },
        {
          "row_index": 262,
          "witness_key": "rel:vent-field-on-ntd1"
        },
        {
          "row_index": 263,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 264,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 265,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 266,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 267,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 268,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 269,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 270,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 271,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 272,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 273,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 274,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 275,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 276,
          "witness_key": "obs:mar-events-317"
        },
        {
          "row_index": 277,
          "witness_key": "obs:romanche-events-197"
        },
        {
          "row_index": 278,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 279,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 280,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 281,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 282,
          "witness_key": "obs:co2-calc-rc2"
        },
        {
          "row_index": 283,
          "witness_key": "obs:co2-calc-rc3"
        },
        {
          "row_index": 284,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 285,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 286,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 287,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 288,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 289,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 290,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 291,
          "witness_key": "obs:rc2-ba"
        },
        {
          "row_index": 292,
          "witness_key": "obs:rc2-rb"
        },
        {
          "row_index": 293,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 294,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 295,
          "witness_key": "obs:bdb-at-ntd2"
        },
        {
          "row_index": 296,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 297,
          "witness_key": "obs:bdb-isotherm-fig6"
        },
        {
          "row_index": 298,
          "witness_key": "obs:bdb-isotherm-slow"
        },
        {
          "row_index": 299,
          "witness_key": "obs:bdb-isotherms-cold"
        },
        {
          "row_index": 300,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 301,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 302,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 303,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 304,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 305,
          "witness_key": "obs:deep-eq-rc2-1619"
        },
        {
          "row_index": 306,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 307,
          "witness_key": "obs:depth-range-ntd2"
        },
        {
          "row_index": 308,
          "witness_key": "obs:depth-range-occ"
        },
        {
          "row_index": 309,
          "witness_key": "obs:hot-mantle-temperature"
        },
        {
          "row_index": 310,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 311,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 312,
          "witness_key": "obs:mantle-temperature-rc2"
        },
        {
          "row_index": 313,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 314,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 315,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 316,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 317,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 318,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 319,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 320,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 321,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 322,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 323,
          "witness_key": "obs:subsolidus-temperature"
        },
        {
          "row_index": 324,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 325,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 326,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 327,
          "witness_key": "obs:obs-no-data"
        },
        {
          "row_index": 328,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 329,
          "witness_key": "obs:vp-vs-test-range"
        }
      ]
    },
    {
      "question_id": "CQ-C-01",
      "question_responsiveness": "NONE",
      "responsiveness_rationale": "No returned row carries a sulfur or chlorine concentration, a unit for one, a sample set measured for those elements, or a measurement status for them. The reading reports rubidium, barium and carbon dioxide for these samples and never sulfur or chlorine, and the sample records returned belong to the carbon dioxide estimation, so under the subject-tie rule they do not name the sample set of this question.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "the reading states no sulfur or chlorine concentration"
        },
        {
          "semantic": "concentration_unit",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "with no such concentration stated, no row carries its unit"
        },
        {
          "semantic": "sample_set",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "the returned sample records are the sets used for the carbon dioxide estimation, not a set analysed for sulfur and chlorine"
        },
        {
          "semantic": "measurement_status",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "no row carries the status of a measurement the reading does not report"
        }
      ],
      "source_locators": [
        "page:5:block:004",
        "page:8:block:006",
        "page:8:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "sample:basalt"
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
          "witness_key": "sample:peridotite"
        },
        {
          "row_index": 4,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 5,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 6,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 7,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 8,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 9,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 10,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 11,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 12,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 13,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 14,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 15,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 16,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 17,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 18,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 19,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 20,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 21,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 22,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 23,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 24,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 25,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 26,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 27,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 28,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 29,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 30,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 31,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 32,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 33,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 34,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 35,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 36,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 37,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 38,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 39,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 40,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 41,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 42,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 43,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 44,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 45,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 46,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 47,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 48,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 49,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 50,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 51,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 52,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 53,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 54,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 55,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 56,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 57,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 58,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 59,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 60,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 61,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 62,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 63,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 64,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 65,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 66,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 67,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 68,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 69,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 70,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 71,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 72,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 73,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 74,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 75,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 76,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 77,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 78,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 79,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 80,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 81,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 82,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 83,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 84,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 85,
          "witness_key": "claim:s-wave-delays-removed"
        },
        {
          "row_index": 86,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 87,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 88,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 89,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 90,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 91,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 92,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 93,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 94,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 95,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 96,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 97,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 98,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 99,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 100,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 101,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 102,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 103,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 104,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 105,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 106,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 107,
          "witness_key": "obs:events-identified-760"
        },
        {
          "row_index": 108,
          "witness_key": "obs:fm-new-3"
        },
        {
          "row_index": 109,
          "witness_key": "obs:fm-previous-3"
        },
        {
          "row_index": 110,
          "witness_key": "obs:fm-total-6"
        },
        {
          "row_index": 111,
          "witness_key": "obs:forced-depth-subset"
        },
        {
          "row_index": 112,
          "witness_key": "obs:located-514"
        },
        {
          "row_index": 113,
          "witness_key": "obs:magnitude-groups"
        },
        {
          "row_index": 114,
          "witness_key": "obs:obs-deployed-19"
        },
        {
          "row_index": 115,
          "witness_key": "obs:obs-useful-17"
        },
        {
          "row_index": 116,
          "witness_key": "obs:quality-categories"
        },
        {
          "row_index": 117,
          "witness_key": "obs:relocated-364"
        },
        {
          "row_index": 118,
          "witness_key": "obs:romanche-2016-subevents"
        },
        {
          "row_index": 119,
          "witness_key": "obs:subsection-count"
        },
        {
          "row_index": 120,
          "witness_key": "obs:velest-subdataset"
        },
        {
          "row_index": 121,
          "witness_key": "obs:velocity-models-five"
        },
        {
          "row_index": 122,
          "witness_key": "obs:well-relocated-276"
        },
        {
          "row_index": 123,
          "witness_key": "ratio:co2-ba"
        },
        {
          "row_index": 124,
          "witness_key": "ratio:co2-rb"
        },
        {
          "row_index": 125,
          "witness_key": "obs:abstract-co2-primary"
        },
        {
          "row_index": 126,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 127,
          "witness_key": "obs:eq-atlantic-co2-average"
        },
        {
          "row_index": 128,
          "witness_key": "obs:eq-atlantic-co2-max"
        },
        {
          "row_index": 129,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 130,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 131,
          "witness_key": "obs:axial-event-depth-stable"
        },
        {
          "row_index": 132,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 133,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 134,
          "witness_key": "obs:cluster-depth-west"
        },
        {
          "row_index": 135,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 136,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 137,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 138,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 139,
          "witness_key": "obs:criteria-met-fraction"
        },
        {
          "row_index": 140,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 141,
          "witness_key": "obs:criterion-gap"
        },
        {
          "row_index": 142,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 143,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 144,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 145,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 146,
          "witness_key": "obs:degassing-depth-range"
        },
        {
          "row_index": 147,
          "witness_key": "obs:depth-uncertainty-cap"
        },
        {
          "row_index": 148,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 149,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 150,
          "witness_key": "obs:expected-brittle-thickness"
        },
        {
          "row_index": 151,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 152,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 153,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 154,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 155,
          "witness_key": "obs:fig3e-elevation-scale"
        },
        {
          "row_index": 156,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 157,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 158,
          "witness_key": "obs:fm-gap"
        },
        {
          "row_index": 159,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 160,
          "witness_key": "obs:fm-polarities"
        },
        {
          "row_index": 161,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 162,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 163,
          "witness_key": "obs:forced-depth-range"
        },
        {
          "row_index": 164,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 165,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 166,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 167,
          "witness_key": "obs:horizontal-uncertainty-cap"
        },
        {
          "row_index": 168,
          "witness_key": "obs:lithospheric-age-interval"
        },
        {
          "row_index": 169,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 170,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 171,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 172,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 173,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 174,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 175,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 176,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 177,
          "witness_key": "obs:min-obs-per-event"
        },
        {
          "row_index": 178,
          "witness_key": "obs:model1-depth"
        },
        {
          "row_index": 179,
          "witness_key": "obs:model1-p-velocity"
        },
        {
          "row_index": 180,
          "witness_key": "obs:occ-transect-halfwidth"
        },
        {
          "row_index": 181,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 182,
          "witness_key": "obs:perturbed-deep-events"
        },
        {
          "row_index": 183,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 184,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 185,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 186,
          "witness_key": "obs:quality-a-uncertainty"
        },
        {
          "row_index": 187,
          "witness_key": "obs:quality-b-uncertainty"
        },
        {
          "row_index": 188,
          "witness_key": "obs:quality-c-uncertainty"
        },
        {
          "row_index": 189,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 190,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 191,
          "witness_key": "obs:refraction-constraint-depth"
        },
        {
          "row_index": 192,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 193,
          "witness_key": "obs:relocation-iterations"
        },
        {
          "row_index": 194,
          "witness_key": "obs:relocation-obs-count"
        },
        {
          "row_index": 195,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 196,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 197,
          "witness_key": "obs:rms-residual-cap"
        },
        {
          "row_index": 198,
          "witness_key": "obs:solubility-temperature"
        },
        {
          "row_index": 199,
          "witness_key": "obs:station-gap-cap"
        },
        {
          "row_index": 200,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 201,
          "witness_key": "obs:subdataset-arrivals"
        },
        {
          "row_index": 202,
          "witness_key": "obs:subdataset-gap"
        },
        {
          "row_index": 203,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 204,
          "witness_key": "obs:velest-iterations"
        },
        {
          "row_index": 205,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 206,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 207,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 208,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 209,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 210,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 211,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 212,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 213,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 214,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 215,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 216,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 217,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 218,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 219,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 220,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 221,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 222,
          "witness_key": "obs:mar-events-317"
        },
        {
          "row_index": 223,
          "witness_key": "obs:obs-no-data"
        },
        {
          "row_index": 224,
          "witness_key": "obs:romanche-events-197"
        },
        {
          "row_index": 225,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 226,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 227,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 228,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 229,
          "witness_key": "obs:co2-calc-rc2"
        },
        {
          "row_index": 230,
          "witness_key": "obs:co2-calc-rc3"
        },
        {
          "row_index": 231,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 232,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 233,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 234,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 235,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 236,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 237,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 238,
          "witness_key": "obs:rc2-ba"
        },
        {
          "row_index": 239,
          "witness_key": "obs:rc2-rb"
        },
        {
          "row_index": 240,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 241,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 242,
          "witness_key": "obs:bdb-at-ntd2"
        },
        {
          "row_index": 243,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 244,
          "witness_key": "obs:bdb-isotherm-fig6"
        },
        {
          "row_index": 245,
          "witness_key": "obs:bdb-isotherm-slow"
        },
        {
          "row_index": 246,
          "witness_key": "obs:bdb-isotherms-cold"
        },
        {
          "row_index": 247,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 248,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 249,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 250,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 251,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 252,
          "witness_key": "obs:deep-eq-rc2-1619"
        },
        {
          "row_index": 253,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 254,
          "witness_key": "obs:depth-range-ntd2"
        },
        {
          "row_index": 255,
          "witness_key": "obs:depth-range-occ"
        },
        {
          "row_index": 256,
          "witness_key": "obs:hot-mantle-temperature"
        },
        {
          "row_index": 257,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 258,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 259,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 260,
          "witness_key": "obs:mantle-temperature-rc2"
        },
        {
          "row_index": 261,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 262,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 263,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 264,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 265,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 266,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 267,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 268,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 269,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 270,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 271,
          "witness_key": "obs:subsolidus-temperature"
        },
        {
          "row_index": 272,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 273,
          "witness_key": "obs:vp-vs-test-range"
        }
      ]
    },
    {
      "question_id": "CQ-C-02",
      "question_responsiveness": "NONE",
      "responsiveness_rationale": "No returned row carries a recurrence interval, a time unit for one, an event population described by one, or its measurement status. The reading gives depths, counts and a recording duration for the deep earthquakes and never a recurrence interval, and the depth observations returned describe a different quantity, so under the subject-tie rule they do not name the event population of this question.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "temporal_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "the reading states no recurrence interval for these earthquakes"
        },
        {
          "semantic": "time_unit",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "with no such interval stated, no row carries its unit"
        },
        {
          "semantic": "event_population",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "the returned rows name the deep earthquakes as the subject of depth observations, not as the population of a recurrence interval"
        },
        {
          "semantic": "measurement_status",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "no row carries the status of a quantity the reading does not report"
        }
      ],
      "source_locators": [
        "page:2:block:006",
        "page:5:block:009",
        "page:7:block:012"
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
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 3,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 4,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 5,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 6,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 7,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 8,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 9,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 10,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 11,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 12,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 13,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 14,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 15,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 16,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 17,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 18,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 19,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 20,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 21,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 22,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 23,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 24,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 25,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 26,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 27,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 28,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 29,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 30,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 31,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 32,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 33,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 34,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 35,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 36,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 37,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 38,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 39,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 40,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 41,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 42,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 43,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 44,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 45,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 46,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 47,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 48,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 49,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 50,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 51,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 52,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 53,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 54,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 55,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 56,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 57,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 58,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 59,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 60,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 61,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 62,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 63,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 64,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 65,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 66,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 67,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 68,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 69,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 70,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 71,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 72,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 73,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 74,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 75,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 76,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 77,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 78,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 79,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 80,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 81,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 82,
          "witness_key": "claim:s-wave-delays-removed"
        },
        {
          "row_index": 83,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 84,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 85,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 86,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 87,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 88,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 89,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 90,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 91,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 92,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 93,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 94,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 95,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 96,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 97,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 98,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 99,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 100,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 101,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 102,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 103,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 104,
          "witness_key": "obs:events-identified-760"
        },
        {
          "row_index": 105,
          "witness_key": "obs:fm-new-3"
        },
        {
          "row_index": 106,
          "witness_key": "obs:fm-previous-3"
        },
        {
          "row_index": 107,
          "witness_key": "obs:fm-total-6"
        },
        {
          "row_index": 108,
          "witness_key": "obs:forced-depth-subset"
        },
        {
          "row_index": 109,
          "witness_key": "obs:located-514"
        },
        {
          "row_index": 110,
          "witness_key": "obs:magnitude-groups"
        },
        {
          "row_index": 111,
          "witness_key": "obs:obs-deployed-19"
        },
        {
          "row_index": 112,
          "witness_key": "obs:obs-useful-17"
        },
        {
          "row_index": 113,
          "witness_key": "obs:quality-categories"
        },
        {
          "row_index": 114,
          "witness_key": "obs:relocated-364"
        },
        {
          "row_index": 115,
          "witness_key": "obs:romanche-2016-subevents"
        },
        {
          "row_index": 116,
          "witness_key": "obs:subsection-count"
        },
        {
          "row_index": 117,
          "witness_key": "obs:velest-subdataset"
        },
        {
          "row_index": 118,
          "witness_key": "obs:velocity-models-five"
        },
        {
          "row_index": 119,
          "witness_key": "obs:well-relocated-276"
        },
        {
          "row_index": 120,
          "witness_key": "obs:abstract-co2-primary"
        },
        {
          "row_index": 121,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 122,
          "witness_key": "obs:eq-atlantic-co2-average"
        },
        {
          "row_index": 123,
          "witness_key": "obs:eq-atlantic-co2-max"
        },
        {
          "row_index": 124,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 125,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 126,
          "witness_key": "obs:axial-event-depth-stable"
        },
        {
          "row_index": 127,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 128,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 129,
          "witness_key": "obs:cluster-depth-west"
        },
        {
          "row_index": 130,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 131,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 132,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 133,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 134,
          "witness_key": "obs:criteria-met-fraction"
        },
        {
          "row_index": 135,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 136,
          "witness_key": "obs:criterion-gap"
        },
        {
          "row_index": 137,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 138,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 139,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 140,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 141,
          "witness_key": "obs:degassing-depth-range"
        },
        {
          "row_index": 142,
          "witness_key": "obs:depth-uncertainty-cap"
        },
        {
          "row_index": 143,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 144,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 145,
          "witness_key": "obs:expected-brittle-thickness"
        },
        {
          "row_index": 146,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 147,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 148,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 149,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 150,
          "witness_key": "obs:fig3e-elevation-scale"
        },
        {
          "row_index": 151,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 152,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 153,
          "witness_key": "obs:fm-gap"
        },
        {
          "row_index": 154,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 155,
          "witness_key": "obs:fm-polarities"
        },
        {
          "row_index": 156,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 157,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 158,
          "witness_key": "obs:forced-depth-range"
        },
        {
          "row_index": 159,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 160,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 161,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 162,
          "witness_key": "obs:horizontal-uncertainty-cap"
        },
        {
          "row_index": 163,
          "witness_key": "obs:lithospheric-age-interval"
        },
        {
          "row_index": 164,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 165,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 166,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 167,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 168,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 169,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 170,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 171,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 172,
          "witness_key": "obs:min-obs-per-event"
        },
        {
          "row_index": 173,
          "witness_key": "obs:model1-depth"
        },
        {
          "row_index": 174,
          "witness_key": "obs:model1-p-velocity"
        },
        {
          "row_index": 175,
          "witness_key": "obs:occ-transect-halfwidth"
        },
        {
          "row_index": 176,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 177,
          "witness_key": "obs:perturbed-deep-events"
        },
        {
          "row_index": 178,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 179,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 180,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 181,
          "witness_key": "obs:quality-a-uncertainty"
        },
        {
          "row_index": 182,
          "witness_key": "obs:quality-b-uncertainty"
        },
        {
          "row_index": 183,
          "witness_key": "obs:quality-c-uncertainty"
        },
        {
          "row_index": 184,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 185,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 186,
          "witness_key": "obs:refraction-constraint-depth"
        },
        {
          "row_index": 187,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 188,
          "witness_key": "obs:relocation-iterations"
        },
        {
          "row_index": 189,
          "witness_key": "obs:relocation-obs-count"
        },
        {
          "row_index": 190,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 191,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 192,
          "witness_key": "obs:rms-residual-cap"
        },
        {
          "row_index": 193,
          "witness_key": "obs:solubility-temperature"
        },
        {
          "row_index": 194,
          "witness_key": "obs:station-gap-cap"
        },
        {
          "row_index": 195,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 196,
          "witness_key": "obs:subdataset-arrivals"
        },
        {
          "row_index": 197,
          "witness_key": "obs:subdataset-gap"
        },
        {
          "row_index": 198,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 199,
          "witness_key": "obs:velest-iterations"
        },
        {
          "row_index": 200,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 201,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 202,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 203,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 204,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 205,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 206,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 207,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 208,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 209,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 210,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 211,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 212,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 213,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 214,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 215,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 216,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 217,
          "witness_key": "obs:mar-events-317"
        },
        {
          "row_index": 218,
          "witness_key": "obs:obs-no-data"
        },
        {
          "row_index": 219,
          "witness_key": "obs:romanche-events-197"
        },
        {
          "row_index": 220,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 221,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 222,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 223,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 224,
          "witness_key": "obs:co2-calc-rc2"
        },
        {
          "row_index": 225,
          "witness_key": "obs:co2-calc-rc3"
        },
        {
          "row_index": 226,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 227,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 228,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 229,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 230,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 231,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 232,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 233,
          "witness_key": "obs:rc2-ba"
        },
        {
          "row_index": 234,
          "witness_key": "obs:rc2-rb"
        },
        {
          "row_index": 235,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 236,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 237,
          "witness_key": "obs:bdb-at-ntd2"
        },
        {
          "row_index": 238,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 239,
          "witness_key": "obs:bdb-isotherm-fig6"
        },
        {
          "row_index": 240,
          "witness_key": "obs:bdb-isotherm-slow"
        },
        {
          "row_index": 241,
          "witness_key": "obs:bdb-isotherms-cold"
        },
        {
          "row_index": 242,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 243,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 244,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 245,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 246,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 247,
          "witness_key": "obs:deep-eq-rc2-1619"
        },
        {
          "row_index": 248,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 249,
          "witness_key": "obs:depth-range-ntd2"
        },
        {
          "row_index": 250,
          "witness_key": "obs:depth-range-occ"
        },
        {
          "row_index": 251,
          "witness_key": "obs:hot-mantle-temperature"
        },
        {
          "row_index": 252,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 253,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 254,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 255,
          "witness_key": "obs:mantle-temperature-rc2"
        },
        {
          "row_index": 256,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 257,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 258,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 259,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 260,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 261,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 262,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 263,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 264,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 265,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 266,
          "witness_key": "obs:subsolidus-temperature"
        },
        {
          "row_index": 267,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 268,
          "witness_key": "obs:vp-vs-test-range"
        }
      ]
    },
    {
      "question_id": "CQ-C-03",
      "question_responsiveness": "NONE",
      "responsiveness_rationale": "No returned row carries the compiled sites as a set, or a maximum depth or spreading rate for any site other than this study's. The per-site values are plotted in the figure and listed in a supplementary table, neither of which is in the reading; the spreading rate and expected depth rows returned are this ridge's own, a same-named element for a different subject, and the individual site records returned are named in the reading only as data updates and as one reference point.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "site_set",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "the reading names the compilation and four sites whose data were updated, but the set of compiled sites is in the figure and the supplementary table, which are not in the reading"
        },
        {
          "semantic": "maximum_depth_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "no maximum depth for any other site is stated in the reading"
        },
        {
          "semantic": "spreading_rate_quantity",
          "row_index": null,
          "absent_reason": "NOT_IN_SOURCE",
          "note": "the only full spreading rate in the reading is this ridge's own"
        }
      ],
      "source_locators": [
        "page:5:block:010",
        "page:8:block:004"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:axial-melt-lens"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 4,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 5,
          "witness_key": "feature:eq-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fracture-zone"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:hummocky"
        },
        {
          "row_index": 11,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 12,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 20,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 21,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 22,
          "witness_key": "feature:neo-volcanic-ridge"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 24,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 25,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 26,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 28,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 29,
          "witness_key": "feature:occ-surface-faults"
        },
        {
          "row_index": 30,
          "witness_key": "feature:occ-termination"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 36,
          "witness_key": "feature:romanche-faults"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:romanche-transform-valley"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rti-detachment"
        },
        {
          "row_index": 41,
          "witness_key": "feature:suspended-valley"
        },
        {
          "row_index": 42,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 43,
          "witness_key": "feature:swir-oblique"
        },
        {
          "row_index": 44,
          "witness_key": "feature:swir-segment-8"
        },
        {
          "row_index": 45,
          "witness_key": "feature:tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:transverse-ridge"
        },
        {
          "row_index": 47,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 48,
          "witness_key": "feature:west-indian-ocean"
        },
        {
          "row_index": 49,
          "witness_key": "work:cruise-data"
        },
        {
          "row_index": 50,
          "witness_key": "work:earthquake-catalog"
        },
        {
          "row_index": 51,
          "witness_key": "work:petdb"
        },
        {
          "row_index": 52,
          "witness_key": "work:ref-1"
        },
        {
          "row_index": 53,
          "witness_key": "work:ref-10"
        },
        {
          "row_index": 54,
          "witness_key": "work:ref-11"
        },
        {
          "row_index": 55,
          "witness_key": "work:ref-12"
        },
        {
          "row_index": 56,
          "witness_key": "work:ref-13"
        },
        {
          "row_index": 57,
          "witness_key": "work:ref-14"
        },
        {
          "row_index": 58,
          "witness_key": "work:ref-15"
        },
        {
          "row_index": 59,
          "witness_key": "work:ref-16"
        },
        {
          "row_index": 60,
          "witness_key": "work:ref-17"
        },
        {
          "row_index": 61,
          "witness_key": "work:ref-18"
        },
        {
          "row_index": 62,
          "witness_key": "work:ref-19"
        },
        {
          "row_index": 63,
          "witness_key": "work:ref-2"
        },
        {
          "row_index": 64,
          "witness_key": "work:ref-20"
        },
        {
          "row_index": 65,
          "witness_key": "work:ref-21"
        },
        {
          "row_index": 66,
          "witness_key": "work:ref-22"
        },
        {
          "row_index": 67,
          "witness_key": "work:ref-23"
        },
        {
          "row_index": 68,
          "witness_key": "work:ref-24"
        },
        {
          "row_index": 69,
          "witness_key": "work:ref-25"
        },
        {
          "row_index": 70,
          "witness_key": "work:ref-26"
        },
        {
          "row_index": 71,
          "witness_key": "work:ref-27"
        },
        {
          "row_index": 72,
          "witness_key": "work:ref-28"
        },
        {
          "row_index": 73,
          "witness_key": "work:ref-29"
        },
        {
          "row_index": 74,
          "witness_key": "work:ref-3"
        },
        {
          "row_index": 75,
          "witness_key": "work:ref-30"
        },
        {
          "row_index": 76,
          "witness_key": "work:ref-31"
        },
        {
          "row_index": 77,
          "witness_key": "work:ref-32"
        },
        {
          "row_index": 78,
          "witness_key": "work:ref-33"
        },
        {
          "row_index": 79,
          "witness_key": "work:ref-34"
        },
        {
          "row_index": 80,
          "witness_key": "work:ref-35"
        },
        {
          "row_index": 81,
          "witness_key": "work:ref-36"
        },
        {
          "row_index": 82,
          "witness_key": "work:ref-37"
        },
        {
          "row_index": 83,
          "witness_key": "work:ref-38"
        },
        {
          "row_index": 84,
          "witness_key": "work:ref-39"
        },
        {
          "row_index": 85,
          "witness_key": "work:ref-4"
        },
        {
          "row_index": 86,
          "witness_key": "work:ref-40"
        },
        {
          "row_index": 87,
          "witness_key": "work:ref-41"
        },
        {
          "row_index": 88,
          "witness_key": "work:ref-42"
        },
        {
          "row_index": 89,
          "witness_key": "work:ref-43"
        },
        {
          "row_index": 90,
          "witness_key": "work:ref-44"
        },
        {
          "row_index": 91,
          "witness_key": "work:ref-45"
        },
        {
          "row_index": 92,
          "witness_key": "work:ref-46"
        },
        {
          "row_index": 93,
          "witness_key": "work:ref-47"
        },
        {
          "row_index": 94,
          "witness_key": "work:ref-48"
        },
        {
          "row_index": 95,
          "witness_key": "work:ref-49"
        },
        {
          "row_index": 96,
          "witness_key": "work:ref-5"
        },
        {
          "row_index": 97,
          "witness_key": "work:ref-50"
        },
        {
          "row_index": 98,
          "witness_key": "work:ref-51"
        },
        {
          "row_index": 99,
          "witness_key": "work:ref-52"
        },
        {
          "row_index": 100,
          "witness_key": "work:ref-53"
        },
        {
          "row_index": 101,
          "witness_key": "work:ref-54"
        },
        {
          "row_index": 102,
          "witness_key": "work:ref-55"
        },
        {
          "row_index": 103,
          "witness_key": "work:ref-56"
        },
        {
          "row_index": 104,
          "witness_key": "work:ref-57"
        },
        {
          "row_index": 105,
          "witness_key": "work:ref-58"
        },
        {
          "row_index": 106,
          "witness_key": "work:ref-59"
        },
        {
          "row_index": 107,
          "witness_key": "work:ref-6"
        },
        {
          "row_index": 108,
          "witness_key": "work:ref-60"
        },
        {
          "row_index": 109,
          "witness_key": "work:ref-61"
        },
        {
          "row_index": 110,
          "witness_key": "work:ref-62"
        },
        {
          "row_index": 111,
          "witness_key": "work:ref-63"
        },
        {
          "row_index": 112,
          "witness_key": "work:ref-64"
        },
        {
          "row_index": 113,
          "witness_key": "work:ref-65"
        },
        {
          "row_index": 114,
          "witness_key": "work:ref-66"
        },
        {
          "row_index": 115,
          "witness_key": "work:ref-67"
        },
        {
          "row_index": 116,
          "witness_key": "work:ref-68"
        },
        {
          "row_index": 117,
          "witness_key": "work:ref-69"
        },
        {
          "row_index": 118,
          "witness_key": "work:ref-7"
        },
        {
          "row_index": 119,
          "witness_key": "work:ref-70"
        },
        {
          "row_index": 120,
          "witness_key": "work:ref-71"
        },
        {
          "row_index": 121,
          "witness_key": "work:ref-72"
        },
        {
          "row_index": 122,
          "witness_key": "work:ref-73"
        },
        {
          "row_index": 123,
          "witness_key": "work:ref-74"
        },
        {
          "row_index": 124,
          "witness_key": "work:ref-75"
        },
        {
          "row_index": 125,
          "witness_key": "work:ref-76"
        },
        {
          "row_index": 126,
          "witness_key": "work:ref-77"
        },
        {
          "row_index": 127,
          "witness_key": "work:ref-78"
        },
        {
          "row_index": 128,
          "witness_key": "work:ref-79"
        },
        {
          "row_index": 129,
          "witness_key": "work:ref-8"
        },
        {
          "row_index": 130,
          "witness_key": "work:ref-9"
        },
        {
          "row_index": 131,
          "witness_key": "work:reprints"
        },
        {
          "row_index": 132,
          "witness_key": "work:self"
        },
        {
          "row_index": 133,
          "witness_key": "work:supplementary"
        },
        {
          "row_index": 134,
          "witness_key": "work:zenodo"
        },
        {
          "row_index": 135,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 136,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 137,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 138,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 139,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 140,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 141,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 142,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 143,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 144,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 145,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 146,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 147,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 148,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 149,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 150,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 151,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 152,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 153,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 154,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 155,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 156,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 157,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 158,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 159,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 160,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 161,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 162,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 163,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 164,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 165,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 166,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 167,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 168,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 169,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 170,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 171,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 172,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 173,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 174,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 175,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 176,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 177,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 178,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 179,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 180,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 181,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 182,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 183,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 184,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 185,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 186,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 187,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 188,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 189,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 190,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 191,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 192,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 193,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 194,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 195,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 196,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 197,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 198,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 199,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 200,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 201,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 202,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 203,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 204,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 205,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 206,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 207,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 208,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 209,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 210,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 211,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 212,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 213,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 214,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 215,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 216,
          "witness_key": "claim:s-wave-delays-removed"
        },
        {
          "row_index": 217,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 218,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 219,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 220,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 221,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 222,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 223,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 224,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 225,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 226,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 227,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 228,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 229,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 230,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 231,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 232,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 233,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 234,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 235,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 236,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 237,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 238,
          "witness_key": "obs:events-identified-760"
        },
        {
          "row_index": 239,
          "witness_key": "obs:fm-new-3"
        },
        {
          "row_index": 240,
          "witness_key": "obs:fm-previous-3"
        },
        {
          "row_index": 241,
          "witness_key": "obs:fm-total-6"
        },
        {
          "row_index": 242,
          "witness_key": "obs:forced-depth-subset"
        },
        {
          "row_index": 243,
          "witness_key": "obs:located-514"
        },
        {
          "row_index": 244,
          "witness_key": "obs:magnitude-groups"
        },
        {
          "row_index": 245,
          "witness_key": "obs:obs-deployed-19"
        },
        {
          "row_index": 246,
          "witness_key": "obs:obs-useful-17"
        },
        {
          "row_index": 247,
          "witness_key": "obs:quality-categories"
        },
        {
          "row_index": 248,
          "witness_key": "obs:relocated-364"
        },
        {
          "row_index": 249,
          "witness_key": "obs:romanche-2016-subevents"
        },
        {
          "row_index": 250,
          "witness_key": "obs:subsection-count"
        },
        {
          "row_index": 251,
          "witness_key": "obs:velest-subdataset"
        },
        {
          "row_index": 252,
          "witness_key": "obs:velocity-models-five"
        },
        {
          "row_index": 253,
          "witness_key": "obs:well-relocated-276"
        },
        {
          "row_index": 254,
          "witness_key": "obs:abstract-co2-primary"
        },
        {
          "row_index": 255,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 256,
          "witness_key": "obs:eq-atlantic-co2-average"
        },
        {
          "row_index": 257,
          "witness_key": "obs:eq-atlantic-co2-max"
        },
        {
          "row_index": 258,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 259,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 260,
          "witness_key": "obs:axial-event-depth-stable"
        },
        {
          "row_index": 261,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 262,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 263,
          "witness_key": "obs:cluster-depth-west"
        },
        {
          "row_index": 264,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 265,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 266,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 267,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 268,
          "witness_key": "obs:criteria-met-fraction"
        },
        {
          "row_index": 269,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 270,
          "witness_key": "obs:criterion-gap"
        },
        {
          "row_index": 271,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 272,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 273,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 274,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 275,
          "witness_key": "obs:degassing-depth-range"
        },
        {
          "row_index": 276,
          "witness_key": "obs:depth-uncertainty-cap"
        },
        {
          "row_index": 277,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 278,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 279,
          "witness_key": "obs:expected-brittle-thickness"
        },
        {
          "row_index": 280,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 281,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 282,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 283,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 284,
          "witness_key": "obs:fig3e-elevation-scale"
        },
        {
          "row_index": 285,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 286,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 287,
          "witness_key": "obs:fm-gap"
        },
        {
          "row_index": 288,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 289,
          "witness_key": "obs:fm-polarities"
        },
        {
          "row_index": 290,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 291,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 292,
          "witness_key": "obs:forced-depth-range"
        },
        {
          "row_index": 293,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 294,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 295,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 296,
          "witness_key": "obs:horizontal-uncertainty-cap"
        },
        {
          "row_index": 297,
          "witness_key": "obs:lithospheric-age-interval"
        },
        {
          "row_index": 298,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 299,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 300,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 301,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 302,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 303,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 304,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 305,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 306,
          "witness_key": "obs:min-obs-per-event"
        },
        {
          "row_index": 307,
          "witness_key": "obs:model1-depth"
        },
        {
          "row_index": 308,
          "witness_key": "obs:model1-p-velocity"
        },
        {
          "row_index": 309,
          "witness_key": "obs:occ-transect-halfwidth"
        },
        {
          "row_index": 310,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 311,
          "witness_key": "obs:perturbed-deep-events"
        },
        {
          "row_index": 312,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 313,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 314,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 315,
          "witness_key": "obs:quality-a-uncertainty"
        },
        {
          "row_index": 316,
          "witness_key": "obs:quality-b-uncertainty"
        },
        {
          "row_index": 317,
          "witness_key": "obs:quality-c-uncertainty"
        },
        {
          "row_index": 318,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 319,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 320,
          "witness_key": "obs:refraction-constraint-depth"
        },
        {
          "row_index": 321,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 322,
          "witness_key": "obs:relocation-iterations"
        },
        {
          "row_index": 323,
          "witness_key": "obs:relocation-obs-count"
        },
        {
          "row_index": 324,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 325,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 326,
          "witness_key": "obs:rms-residual-cap"
        },
        {
          "row_index": 327,
          "witness_key": "obs:solubility-temperature"
        },
        {
          "row_index": 328,
          "witness_key": "obs:station-gap-cap"
        },
        {
          "row_index": 329,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 330,
          "witness_key": "obs:subdataset-arrivals"
        },
        {
          "row_index": 331,
          "witness_key": "obs:subdataset-gap"
        },
        {
          "row_index": 332,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 333,
          "witness_key": "obs:velest-iterations"
        },
        {
          "row_index": 334,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 335,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 336,
          "witness_key": "rel:askja-in-iceland"
        },
        {
          "row_index": 337,
          "witness_key": "rel:fagradalsfjall-in-iceland"
        },
        {
          "row_index": 338,
          "witness_key": "rel:logachev-of-knipovich"
        },
        {
          "row_index": 339,
          "witness_key": "rel:mar-in-eq-atlantic"
        },
        {
          "row_index": 340,
          "witness_key": "rel:marseg-bounded-chain"
        },
        {
          "row_index": 341,
          "witness_key": "rel:marseg-bounded-romanche"
        },
        {
          "row_index": 342,
          "witness_key": "rel:mayotte-in-indian-ocean"
        },
        {
          "row_index": 343,
          "witness_key": "rel:occ-on-mar"
        },
        {
          "row_index": 344,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 345,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 346,
          "witness_key": "rel:romanche-faults-in-tf"
        },
        {
          "row_index": 347,
          "witness_key": "rel:vent-field-on-ntd1"
        },
        {
          "row_index": 348,
          "witness_key": "rel:catalog-in-zenodo"
        },
        {
          "row_index": 349,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 350,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 351,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 352,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 353,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 354,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 355,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 356,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 357,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 358,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 359,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 360,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 361,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 362,
          "witness_key": "obs:mar-events-317"
        },
        {
          "row_index": 363,
          "witness_key": "obs:romanche-events-197"
        },
        {
          "row_index": 364,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 365,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 366,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 367,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 368,
          "witness_key": "obs:co2-calc-rc2"
        },
        {
          "row_index": 369,
          "witness_key": "obs:co2-calc-rc3"
        },
        {
          "row_index": 370,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 371,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 372,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 373,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 374,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 375,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 376,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 377,
          "witness_key": "obs:rc2-ba"
        },
        {
          "row_index": 378,
          "witness_key": "obs:rc2-rb"
        },
        {
          "row_index": 379,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 380,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 381,
          "witness_key": "obs:bdb-at-ntd2"
        },
        {
          "row_index": 382,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 383,
          "witness_key": "obs:bdb-isotherm-fig6"
        },
        {
          "row_index": 384,
          "witness_key": "obs:bdb-isotherm-slow"
        },
        {
          "row_index": 385,
          "witness_key": "obs:bdb-isotherms-cold"
        },
        {
          "row_index": 386,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 387,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 388,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 389,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 390,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 391,
          "witness_key": "obs:deep-eq-rc2-1619"
        },
        {
          "row_index": 392,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 393,
          "witness_key": "obs:depth-range-ntd2"
        },
        {
          "row_index": 394,
          "witness_key": "obs:depth-range-occ"
        },
        {
          "row_index": 395,
          "witness_key": "obs:hot-mantle-temperature"
        },
        {
          "row_index": 396,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 397,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 398,
          "witness_key": "obs:mantle-temperature-rc2"
        },
        {
          "row_index": 399,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 400,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 401,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 402,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 403,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 404,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 405,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 406,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 407,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 408,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 409,
          "witness_key": "obs:subsolidus-temperature"
        },
        {
          "row_index": 410,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 411,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 412,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 413,
          "witness_key": "obs:obs-no-data"
        },
        {
          "row_index": 414,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 415,
          "witness_key": "obs:vp-vs-test-range"
        }
      ]
    },
    {
      "question_id": "CQ-C-04",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "The same three elements are carried as for the question this one paraphrases: the count row gives the number and names the network, and the cruise row carries the deployment; nothing joins them.",
      "assembly": "UNLINKED_ROWS",
      "coverage": [
        {
          "semantic": "instrument_count",
          "row_index": 10,
          "absent_reason": null,
          "note": "the count of ocean-bottom seismometers"
        },
        {
          "semantic": "observing_system",
          "row_index": 10,
          "absent_reason": null,
          "note": "the count scope names the network that acquired the microseismicity data"
        },
        {
          "semantic": "deployment_event",
          "row_index": 0,
          "absent_reason": null,
          "note": "the cruise record's description states the OBS passive seismic experiment conducted during the 2019 cruise"
        }
      ],
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002",
        "page:2:block:007",
        "page:9:block:023",
        "page:9:block:024",
        "page:10:block:043",
        "page:10:block:044",
        "page:10:block:046"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "cruise:smarties"
        },
        {
          "row_index": 1,
          "witness_key": "instrument:nautile"
        },
        {
          "row_index": 2,
          "witness_key": "instrument:obs"
        },
        {
          "row_index": 3,
          "witness_key": "obs:events-identified-760"
        },
        {
          "row_index": 4,
          "witness_key": "obs:fm-new-3"
        },
        {
          "row_index": 5,
          "witness_key": "obs:fm-previous-3"
        },
        {
          "row_index": 6,
          "witness_key": "obs:fm-total-6"
        },
        {
          "row_index": 7,
          "witness_key": "obs:forced-depth-subset"
        },
        {
          "row_index": 8,
          "witness_key": "obs:located-514"
        },
        {
          "row_index": 9,
          "witness_key": "obs:magnitude-groups"
        },
        {
          "row_index": 10,
          "witness_key": "obs:obs-deployed-19"
        },
        {
          "row_index": 11,
          "witness_key": "obs:obs-useful-17"
        },
        {
          "row_index": 12,
          "witness_key": "obs:quality-categories"
        },
        {
          "row_index": 13,
          "witness_key": "obs:relocated-364"
        },
        {
          "row_index": 14,
          "witness_key": "obs:romanche-2016-subevents"
        },
        {
          "row_index": 15,
          "witness_key": "obs:subsection-count"
        },
        {
          "row_index": 16,
          "witness_key": "obs:velest-subdataset"
        },
        {
          "row_index": 17,
          "witness_key": "obs:velocity-models-five"
        },
        {
          "row_index": 18,
          "witness_key": "obs:well-relocated-276"
        },
        {
          "row_index": 19,
          "witness_key": "obs:abstract-co2-primary"
        },
        {
          "row_index": 20,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 21,
          "witness_key": "obs:eq-atlantic-co2-average"
        },
        {
          "row_index": 22,
          "witness_key": "obs:eq-atlantic-co2-max"
        },
        {
          "row_index": 23,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 24,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 25,
          "witness_key": "obs:axial-event-depth-stable"
        },
        {
          "row_index": 26,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 27,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 28,
          "witness_key": "obs:cluster-depth-west"
        },
        {
          "row_index": 29,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 30,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 31,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 32,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 33,
          "witness_key": "obs:criteria-met-fraction"
        },
        {
          "row_index": 34,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 35,
          "witness_key": "obs:criterion-gap"
        },
        {
          "row_index": 36,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 37,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 38,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 39,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 40,
          "witness_key": "obs:degassing-depth-range"
        },
        {
          "row_index": 41,
          "witness_key": "obs:depth-uncertainty-cap"
        },
        {
          "row_index": 42,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 43,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 44,
          "witness_key": "obs:expected-brittle-thickness"
        },
        {
          "row_index": 45,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 46,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 47,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 48,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 49,
          "witness_key": "obs:fig3e-elevation-scale"
        },
        {
          "row_index": 50,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 51,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 52,
          "witness_key": "obs:fm-gap"
        },
        {
          "row_index": 53,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 54,
          "witness_key": "obs:fm-polarities"
        },
        {
          "row_index": 55,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 56,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 57,
          "witness_key": "obs:forced-depth-range"
        },
        {
          "row_index": 58,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 59,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 60,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 61,
          "witness_key": "obs:horizontal-uncertainty-cap"
        },
        {
          "row_index": 62,
          "witness_key": "obs:lithospheric-age-interval"
        },
        {
          "row_index": 63,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 64,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 65,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 66,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 67,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 68,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 69,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 70,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 71,
          "witness_key": "obs:min-obs-per-event"
        },
        {
          "row_index": 72,
          "witness_key": "obs:model1-depth"
        },
        {
          "row_index": 73,
          "witness_key": "obs:model1-p-velocity"
        },
        {
          "row_index": 74,
          "witness_key": "obs:occ-transect-halfwidth"
        },
        {
          "row_index": 75,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 76,
          "witness_key": "obs:perturbed-deep-events"
        },
        {
          "row_index": 77,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 78,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 79,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 80,
          "witness_key": "obs:quality-a-uncertainty"
        },
        {
          "row_index": 81,
          "witness_key": "obs:quality-b-uncertainty"
        },
        {
          "row_index": 82,
          "witness_key": "obs:quality-c-uncertainty"
        },
        {
          "row_index": 83,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 84,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 85,
          "witness_key": "obs:refraction-constraint-depth"
        },
        {
          "row_index": 86,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 87,
          "witness_key": "obs:relocation-iterations"
        },
        {
          "row_index": 88,
          "witness_key": "obs:relocation-obs-count"
        },
        {
          "row_index": 89,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 90,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 91,
          "witness_key": "obs:rms-residual-cap"
        },
        {
          "row_index": 92,
          "witness_key": "obs:solubility-temperature"
        },
        {
          "row_index": 93,
          "witness_key": "obs:station-gap-cap"
        },
        {
          "row_index": 94,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 95,
          "witness_key": "obs:subdataset-arrivals"
        },
        {
          "row_index": 96,
          "witness_key": "obs:subdataset-gap"
        },
        {
          "row_index": 97,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 98,
          "witness_key": "obs:velest-iterations"
        },
        {
          "row_index": 99,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 100,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 101,
          "witness_key": "obs:obs-no-data"
        },
        {
          "row_index": 102,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 103,
          "witness_key": "obs:mar-events-317"
        },
        {
          "row_index": 104,
          "witness_key": "obs:romanche-events-197"
        },
        {
          "row_index": 105,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 106,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 107,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 108,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 109,
          "witness_key": "obs:co2-calc-rc2"
        },
        {
          "row_index": 110,
          "witness_key": "obs:co2-calc-rc3"
        },
        {
          "row_index": 111,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 112,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 113,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 114,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 115,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 116,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 117,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 118,
          "witness_key": "obs:rc2-ba"
        },
        {
          "row_index": 119,
          "witness_key": "obs:rc2-rb"
        },
        {
          "row_index": 120,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 121,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 122,
          "witness_key": "obs:bdb-at-ntd2"
        },
        {
          "row_index": 123,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 124,
          "witness_key": "obs:bdb-isotherm-fig6"
        },
        {
          "row_index": 125,
          "witness_key": "obs:bdb-isotherm-slow"
        },
        {
          "row_index": 126,
          "witness_key": "obs:bdb-isotherms-cold"
        },
        {
          "row_index": 127,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 128,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 129,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 130,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 131,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 132,
          "witness_key": "obs:deep-eq-rc2-1619"
        },
        {
          "row_index": 133,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 134,
          "witness_key": "obs:depth-range-ntd2"
        },
        {
          "row_index": 135,
          "witness_key": "obs:depth-range-occ"
        },
        {
          "row_index": 136,
          "witness_key": "obs:hot-mantle-temperature"
        },
        {
          "row_index": 137,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 138,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 139,
          "witness_key": "obs:mantle-temperature-rc2"
        },
        {
          "row_index": 140,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 141,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 142,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 143,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 144,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 145,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 146,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 147,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 148,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 149,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 150,
          "witness_key": "obs:subsolidus-temperature"
        },
        {
          "row_index": 151,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 152,
          "witness_key": "obs:vp-vs-test-range"
        }
      ]
    },
    {
      "question_id": "CQ-C-05",
      "question_responsiveness": "COVERED",
      "responsiveness_rationale": "As for the question this one paraphrases, one observation row carries the content, the unit, the primary-melt subject and the calculated status.",
      "assembly": "ONE_ROW",
      "coverage": [
        {
          "semantic": "bounded_quantity",
          "row_index": 285,
          "absent_reason": null,
          "note": "the primary-melt content estimated from the barium proxy"
        },
        {
          "semantic": "concentration_unit",
          "row_index": 285,
          "absent_reason": null,
          "note": ""
        },
        {
          "semantic": "quantity_subject",
          "row_index": 285,
          "absent_reason": null,
          "note": "the row's subject is the studied segment and its melt stage is the primary melt"
        },
        {
          "semantic": "calculated_or_measured_status",
          "row_index": 285,
          "absent_reason": null,
          "note": "the row's determination is estimated and its modality calculated"
        }
      ],
      "source_locators": [
        "page:8:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "witness_key": "feature:askja"
        },
        {
          "row_index": 1,
          "witness_key": "feature:axial-melt-lens"
        },
        {
          "row_index": 2,
          "witness_key": "feature:axial-valley"
        },
        {
          "row_index": 3,
          "witness_key": "feature:bdb"
        },
        {
          "row_index": 4,
          "witness_key": "feature:chain-tf"
        },
        {
          "row_index": 5,
          "witness_key": "feature:eq-atlantic"
        },
        {
          "row_index": 6,
          "witness_key": "feature:extinct-vent-field"
        },
        {
          "row_index": 7,
          "witness_key": "feature:fagradalsfjall"
        },
        {
          "row_index": 8,
          "witness_key": "feature:fracture-zone"
        },
        {
          "row_index": 9,
          "witness_key": "feature:gakkel"
        },
        {
          "row_index": 10,
          "witness_key": "feature:hummocky"
        },
        {
          "row_index": 11,
          "witness_key": "feature:iceland"
        },
        {
          "row_index": 12,
          "witness_key": "feature:inactive-mound"
        },
        {
          "row_index": 13,
          "witness_key": "feature:juan-de-fuca"
        },
        {
          "row_index": 14,
          "witness_key": "feature:knipovich"
        },
        {
          "row_index": 15,
          "witness_key": "feature:lab"
        },
        {
          "row_index": 16,
          "witness_key": "feature:logachev"
        },
        {
          "row_index": 17,
          "witness_key": "feature:mar"
        },
        {
          "row_index": 18,
          "witness_key": "feature:mar-segment"
        },
        {
          "row_index": 19,
          "witness_key": "feature:mayotte"
        },
        {
          "row_index": 20,
          "witness_key": "feature:median-valley"
        },
        {
          "row_index": 21,
          "witness_key": "feature:moho"
        },
        {
          "row_index": 22,
          "witness_key": "feature:neo-volcanic-ridge"
        },
        {
          "row_index": 23,
          "witness_key": "feature:ntd1"
        },
        {
          "row_index": 24,
          "witness_key": "feature:ntd1-faults"
        },
        {
          "row_index": 25,
          "witness_key": "feature:ntd2"
        },
        {
          "row_index": 26,
          "witness_key": "feature:ntd2-faults"
        },
        {
          "row_index": 27,
          "witness_key": "feature:occ"
        },
        {
          "row_index": 28,
          "witness_key": "feature:occ-corrugated-surface"
        },
        {
          "row_index": 29,
          "witness_key": "feature:occ-surface-faults"
        },
        {
          "row_index": 30,
          "witness_key": "feature:occ-termination"
        },
        {
          "row_index": 31,
          "witness_key": "feature:rainbow"
        },
        {
          "row_index": 32,
          "witness_key": "feature:rc1"
        },
        {
          "row_index": 33,
          "witness_key": "feature:rc2"
        },
        {
          "row_index": 34,
          "witness_key": "feature:rc2-bounding-faults"
        },
        {
          "row_index": 35,
          "witness_key": "feature:rc3"
        },
        {
          "row_index": 36,
          "witness_key": "feature:romanche-faults"
        },
        {
          "row_index": 37,
          "witness_key": "feature:romanche-tf"
        },
        {
          "row_index": 38,
          "witness_key": "feature:romanche-transform-valley"
        },
        {
          "row_index": 39,
          "witness_key": "feature:rti"
        },
        {
          "row_index": 40,
          "witness_key": "feature:rti-detachment"
        },
        {
          "row_index": 41,
          "witness_key": "feature:suspended-valley"
        },
        {
          "row_index": 42,
          "witness_key": "feature:swir"
        },
        {
          "row_index": 43,
          "witness_key": "feature:swir-oblique"
        },
        {
          "row_index": 44,
          "witness_key": "feature:swir-segment-8"
        },
        {
          "row_index": 45,
          "witness_key": "feature:tf"
        },
        {
          "row_index": 46,
          "witness_key": "feature:transverse-ridge"
        },
        {
          "row_index": 47,
          "witness_key": "feature:volcanic-cones"
        },
        {
          "row_index": 48,
          "witness_key": "feature:west-indian-ocean"
        },
        {
          "row_index": 49,
          "witness_key": "sample:basalt"
        },
        {
          "row_index": 50,
          "witness_key": "sample:morb-obs-network"
        },
        {
          "row_index": 51,
          "witness_key": "sample:morb-rc2"
        },
        {
          "row_index": 52,
          "witness_key": "sample:peridotite"
        },
        {
          "row_index": 53,
          "witness_key": "claim:ab-good-quality"
        },
        {
          "row_index": 54,
          "witness_key": "claim:aml-defines-bdb"
        },
        {
          "row_index": 55,
          "witness_key": "claim:amplitude-measurement"
        },
        {
          "row_index": 56,
          "witness_key": "claim:arrivals-checked-manually"
        },
        {
          "row_index": 57,
          "witness_key": "claim:axial-valley-floor"
        },
        {
          "row_index": 58,
          "witness_key": "claim:axis-relocating"
        },
        {
          "row_index": 59,
          "witness_key": "claim:bdb-shallower-southward"
        },
        {
          "row_index": 60,
          "witness_key": "claim:brittle-ductile-patches"
        },
        {
          "row_index": 61,
          "witness_key": "claim:category-criteria"
        },
        {
          "row_index": 62,
          "witness_key": "claim:co2-from-rb90-ba90"
        },
        {
          "row_index": 63,
          "witness_key": "claim:co2-like-incompatible"
        },
        {
          "row_index": 64,
          "witness_key": "claim:co2-solubility-pressure"
        },
        {
          "row_index": 65,
          "witness_key": "claim:cold-thick-lithosphere"
        },
        {
          "row_index": 66,
          "witness_key": "claim:contexts-differ"
        },
        {
          "row_index": 67,
          "witness_key": "claim:copyright"
        },
        {
          "row_index": 68,
          "witness_key": "claim:correspondence"
        },
        {
          "row_index": 69,
          "witness_key": "claim:criteria-followed"
        },
        {
          "row_index": 70,
          "witness_key": "claim:crust-from-mantle-melt"
        },
        {
          "row_index": 71,
          "witness_key": "claim:deep-eq-alignment"
        },
        {
          "row_index": 72,
          "witness_key": "claim:deep-long-period"
        },
        {
          "row_index": 73,
          "witness_key": "claim:deeper-eq-observed"
        },
        {
          "row_index": 74,
          "witness_key": "claim:deepest-documented"
        },
        {
          "row_index": 75,
          "witness_key": "claim:degassing-volume-change"
        },
        {
          "row_index": 76,
          "witness_key": "claim:depth-resolution-tests"
        },
        {
          "row_index": 77,
          "witness_key": "claim:detachment-inactive"
        },
        {
          "row_index": 78,
          "witness_key": "claim:enriched-mantle-source"
        },
        {
          "row_index": 79,
          "witness_key": "claim:eq-in-mantle"
        },
        {
          "row_index": 80,
          "witness_key": "claim:events-with-eruptions"
        },
        {
          "row_index": 81,
          "witness_key": "claim:faults-favor-migration"
        },
        {
          "row_index": 82,
          "witness_key": "claim:fig3a-content"
        },
        {
          "row_index": 83,
          "witness_key": "claim:fig5-estimated-primary"
        },
        {
          "row_index": 84,
          "witness_key": "claim:fixed-depth-rms"
        },
        {
          "row_index": 85,
          "witness_key": "claim:focal-mechanisms-shown"
        },
        {
          "row_index": 86,
          "witness_key": "claim:focus-on-segments"
        },
        {
          "row_index": 87,
          "witness_key": "claim:forced-depths-values"
        },
        {
          "row_index": 88,
          "witness_key": "claim:global-trends"
        },
        {
          "row_index": 89,
          "witness_key": "claim:hydrothermal-cooling"
        },
        {
          "row_index": 90,
          "witness_key": "claim:hypocentral-distance"
        },
        {
          "row_index": 91,
          "witness_key": "claim:ipgp-contribution"
        },
        {
          "row_index": 92,
          "witness_key": "claim:licence-terms"
        },
        {
          "row_index": 93,
          "witness_key": "claim:local-magnitudes"
        },
        {
          "row_index": 94,
          "witness_key": "claim:magmatic-tectonic"
        },
        {
          "row_index": 95,
          "witness_key": "claim:max-depth-compilation"
        },
        {
          "row_index": 96,
          "witness_key": "claim:max-depth-covariates"
        },
        {
          "row_index": 97,
          "witness_key": "claim:max-depth-influences"
        },
        {
          "row_index": 98,
          "witness_key": "claim:max-depth-not-following"
        },
        {
          "row_index": 99,
          "witness_key": "claim:max-depth-other-factors"
        },
        {
          "row_index": 100,
          "witness_key": "claim:max-depth-selection"
        },
        {
          "row_index": 101,
          "witness_key": "claim:max-likelihood-preferred"
        },
        {
          "row_index": 102,
          "witness_key": "claim:measured-near-solubility"
        },
        {
          "row_index": 103,
          "witness_key": "claim:melt-continues-degassing"
        },
        {
          "row_index": 104,
          "witness_key": "claim:melt-focusing"
        },
        {
          "row_index": 105,
          "witness_key": "claim:melt-freeze-lithosphere"
        },
        {
          "row_index": 106,
          "witness_key": "claim:melt-movement-strain"
        },
        {
          "row_index": 107,
          "witness_key": "claim:melt-resides-fractionates"
        },
        {
          "row_index": 108,
          "witness_key": "claim:migration-unknown"
        },
        {
          "row_index": 109,
          "witness_key": "claim:model-selection"
        },
        {
          "row_index": 110,
          "witness_key": "claim:model1-inappropriate"
        },
        {
          "row_index": 111,
          "witness_key": "claim:more-events-needed"
        },
        {
          "row_index": 112,
          "witness_key": "claim:no-competing-interests"
        },
        {
          "row_index": 113,
          "witness_key": "claim:no-detachment-rc2"
        },
        {
          "row_index": 114,
          "witness_key": "claim:not-location-artifact"
        },
        {
          "row_index": 115,
          "witness_key": "claim:ntd1-origin"
        },
        {
          "row_index": 116,
          "witness_key": "claim:nucleation-similar-volcanoes"
        },
        {
          "row_index": 117,
          "witness_key": "claim:occ-dome-ruptures"
        },
        {
          "row_index": 118,
          "witness_key": "claim:offaxis-magmatism"
        },
        {
          "row_index": 119,
          "witness_key": "claim:peer-review"
        },
        {
          "row_index": 120,
          "witness_key": "claim:peridotites-exhumed-mantle"
        },
        {
          "row_index": 121,
          "witness_key": "claim:polarity-picking"
        },
        {
          "row_index": 122,
          "witness_key": "claim:primary-vs-pre-eruptive"
        },
        {
          "row_index": 123,
          "witness_key": "claim:publisher-note"
        },
        {
          "row_index": 124,
          "witness_key": "claim:ratios-good-proxy"
        },
        {
          "row_index": 125,
          "witness_key": "claim:rb90-ba90-calculation"
        },
        {
          "row_index": 126,
          "witness_key": "claim:rc1-amagmatic"
        },
        {
          "row_index": 127,
          "witness_key": "claim:rc2-basalts"
        },
        {
          "row_index": 128,
          "witness_key": "claim:rc2-magmatic-origin"
        },
        {
          "row_index": 129,
          "witness_key": "claim:rc2-magmatically-robust"
        },
        {
          "row_index": 130,
          "witness_key": "claim:rc2-rc3-analyzed"
        },
        {
          "row_index": 131,
          "witness_key": "claim:recent-tectonic-deformation"
        },
        {
          "row_index": 132,
          "witness_key": "claim:reduced-velocity-preferred"
        },
        {
          "row_index": 133,
          "witness_key": "claim:relocation-inputs"
        },
        {
          "row_index": 134,
          "witness_key": "claim:s-wave-delays-removed"
        },
        {
          "row_index": 135,
          "witness_key": "claim:samples-degassed"
        },
        {
          "row_index": 136,
          "witness_key": "claim:seafloor-basalts-degassed"
        },
        {
          "row_index": 137,
          "witness_key": "claim:selected-model-preferred"
        },
        {
          "row_index": 138,
          "witness_key": "claim:shear-zone"
        },
        {
          "row_index": 139,
          "witness_key": "claim:shear-zone-detachment"
        },
        {
          "row_index": 140,
          "witness_key": "claim:snapshot-limitation"
        },
        {
          "row_index": 141,
          "witness_key": "claim:solutions-not-robust"
        },
        {
          "row_index": 142,
          "witness_key": "claim:station-corrections"
        },
        {
          "row_index": 143,
          "witness_key": "claim:station-corrections-applied"
        },
        {
          "row_index": 144,
          "witness_key": "claim:station-corrections-iterative"
        },
        {
          "row_index": 145,
          "witness_key": "claim:tests-support-depth"
        },
        {
          "row_index": 146,
          "witness_key": "claim:tf-deep-eq"
        },
        {
          "row_index": 147,
          "witness_key": "claim:trace-element-assumption"
        },
        {
          "row_index": 148,
          "witness_key": "claim:ultraslow-co2-high"
        },
        {
          "row_index": 149,
          "witness_key": "claim:updated-depth-data"
        },
        {
          "row_index": 150,
          "witness_key": "claim:velocity-structure-matters"
        },
        {
          "row_index": 151,
          "witness_key": "claim:vent-field-too-far"
        },
        {
          "row_index": 152,
          "witness_key": "claim:volatile-role-unknown"
        },
        {
          "row_index": 153,
          "witness_key": "claim:volatiles-control-magma"
        },
        {
          "row_index": 154,
          "witness_key": "claim:volatiles-extend-melting"
        },
        {
          "row_index": 155,
          "witness_key": "claim:zero-position-rti"
        },
        {
          "row_index": 156,
          "witness_key": "obs:events-identified-760"
        },
        {
          "row_index": 157,
          "witness_key": "obs:fm-new-3"
        },
        {
          "row_index": 158,
          "witness_key": "obs:fm-previous-3"
        },
        {
          "row_index": 159,
          "witness_key": "obs:fm-total-6"
        },
        {
          "row_index": 160,
          "witness_key": "obs:forced-depth-subset"
        },
        {
          "row_index": 161,
          "witness_key": "obs:located-514"
        },
        {
          "row_index": 162,
          "witness_key": "obs:magnitude-groups"
        },
        {
          "row_index": 163,
          "witness_key": "obs:obs-deployed-19"
        },
        {
          "row_index": 164,
          "witness_key": "obs:obs-useful-17"
        },
        {
          "row_index": 165,
          "witness_key": "obs:quality-categories"
        },
        {
          "row_index": 166,
          "witness_key": "obs:relocated-364"
        },
        {
          "row_index": 167,
          "witness_key": "obs:romanche-2016-subevents"
        },
        {
          "row_index": 168,
          "witness_key": "obs:subsection-count"
        },
        {
          "row_index": 169,
          "witness_key": "obs:velest-subdataset"
        },
        {
          "row_index": 170,
          "witness_key": "obs:velocity-models-five"
        },
        {
          "row_index": 171,
          "witness_key": "obs:well-relocated-276"
        },
        {
          "row_index": 172,
          "witness_key": "ratio:co2-ba"
        },
        {
          "row_index": 173,
          "witness_key": "ratio:co2-rb"
        },
        {
          "row_index": 174,
          "witness_key": "obs:abstract-co2-primary"
        },
        {
          "row_index": 175,
          "witness_key": "obs:co2-gas-loss"
        },
        {
          "row_index": 176,
          "witness_key": "obs:eq-atlantic-co2-average"
        },
        {
          "row_index": 177,
          "witness_key": "obs:eq-atlantic-co2-max"
        },
        {
          "row_index": 178,
          "witness_key": "obs:average-depth-uncertainty"
        },
        {
          "row_index": 179,
          "witness_key": "obs:avg-horizontal-uncertainty"
        },
        {
          "row_index": 180,
          "witness_key": "obs:axial-event-depth-stable"
        },
        {
          "row_index": 181,
          "witness_key": "obs:b-value"
        },
        {
          "row_index": 182,
          "witness_key": "obs:brittle-thickness-ntds"
        },
        {
          "row_index": 183,
          "witness_key": "obs:cluster-depth-west"
        },
        {
          "row_index": 184,
          "witness_key": "obs:co2-saturation-depth"
        },
        {
          "row_index": 185,
          "witness_key": "obs:co2-saturation-pressure"
        },
        {
          "row_index": 186,
          "witness_key": "obs:co2-saturation-temperature"
        },
        {
          "row_index": 187,
          "witness_key": "obs:cold-lithosphere-age"
        },
        {
          "row_index": 188,
          "witness_key": "obs:criteria-met-fraction"
        },
        {
          "row_index": 189,
          "witness_key": "obs:criterion-arrivals"
        },
        {
          "row_index": 190,
          "witness_key": "obs:criterion-gap"
        },
        {
          "row_index": 191,
          "witness_key": "obs:criterion-s-distance"
        },
        {
          "row_index": 192,
          "witness_key": "obs:crust-age-west-flank"
        },
        {
          "row_index": 193,
          "witness_key": "obs:crust-thickness-west-flank"
        },
        {
          "row_index": 194,
          "witness_key": "obs:crustal-age-offaxis"
        },
        {
          "row_index": 195,
          "witness_key": "obs:degassing-depth-range"
        },
        {
          "row_index": 196,
          "witness_key": "obs:depth-uncertainty-cap"
        },
        {
          "row_index": 197,
          "witness_key": "obs:dry-melting-depth"
        },
        {
          "row_index": 198,
          "witness_key": "obs:error-ellipsoid-confidence"
        },
        {
          "row_index": 199,
          "witness_key": "obs:expected-brittle-thickness"
        },
        {
          "row_index": 200,
          "witness_key": "obs:expected-depth-slow"
        },
        {
          "row_index": 201,
          "witness_key": "obs:expected-depth-ultraslow"
        },
        {
          "row_index": 202,
          "witness_key": "obs:expected-max-depth-32"
        },
        {
          "row_index": 203,
          "witness_key": "obs:fig3-shading-threshold"
        },
        {
          "row_index": 204,
          "witness_key": "obs:fig3e-elevation-scale"
        },
        {
          "row_index": 205,
          "witness_key": "obs:fig4-isotherm"
        },
        {
          "row_index": 206,
          "witness_key": "obs:fm-fault-plane-uncertainty"
        },
        {
          "row_index": 207,
          "witness_key": "obs:fm-gap"
        },
        {
          "row_index": 208,
          "witness_key": "obs:fm-misfit"
        },
        {
          "row_index": 209,
          "witness_key": "obs:fm-polarities"
        },
        {
          "row_index": 210,
          "witness_key": "obs:fm-probability"
        },
        {
          "row_index": 211,
          "witness_key": "obs:fm-station-ratio"
        },
        {
          "row_index": 212,
          "witness_key": "obs:forced-depth-range"
        },
        {
          "row_index": 213,
          "witness_key": "obs:full-spreading-rate"
        },
        {
          "row_index": 214,
          "witness_key": "obs:group-b-values"
        },
        {
          "row_index": 215,
          "witness_key": "obs:high-frequency-threshold"
        },
        {
          "row_index": 216,
          "witness_key": "obs:horizontal-uncertainty-cap"
        },
        {
          "row_index": 217,
          "witness_key": "obs:lithospheric-age-interval"
        },
        {
          "row_index": 218,
          "witness_key": "obs:magnitude-completeness"
        },
        {
          "row_index": 219,
          "witness_key": "obs:mar-segment-length"
        },
        {
          "row_index": 220,
          "witness_key": "obs:max-event-separation"
        },
        {
          "row_index": 221,
          "witness_key": "obs:mean-horizontal-error"
        },
        {
          "row_index": 222,
          "witness_key": "obs:mean-vertical-error"
        },
        {
          "row_index": 223,
          "witness_key": "obs:median-valley-width"
        },
        {
          "row_index": 224,
          "witness_key": "obs:melting-initiation-depth"
        },
        {
          "row_index": 225,
          "witness_key": "obs:min-catalog-links"
        },
        {
          "row_index": 226,
          "witness_key": "obs:min-obs-per-event"
        },
        {
          "row_index": 227,
          "witness_key": "obs:model1-depth"
        },
        {
          "row_index": 228,
          "witness_key": "obs:model1-p-velocity"
        },
        {
          "row_index": 229,
          "witness_key": "obs:occ-transect-halfwidth"
        },
        {
          "row_index": 230,
          "witness_key": "obs:offaxis-swarm-depth"
        },
        {
          "row_index": 231,
          "witness_key": "obs:perturbed-deep-events"
        },
        {
          "row_index": 232,
          "witness_key": "obs:pore-pressure-trigger"
        },
        {
          "row_index": 233,
          "witness_key": "obs:profile-halfwidth"
        },
        {
          "row_index": 234,
          "witness_key": "obs:profile-tick-interval"
        },
        {
          "row_index": 235,
          "witness_key": "obs:quality-a-uncertainty"
        },
        {
          "row_index": 236,
          "witness_key": "obs:quality-b-uncertainty"
        },
        {
          "row_index": 237,
          "witness_key": "obs:quality-c-uncertainty"
        },
        {
          "row_index": 238,
          "witness_key": "obs:quality-d-uncertainty"
        },
        {
          "row_index": 239,
          "witness_key": "obs:recording-duration"
        },
        {
          "row_index": 240,
          "witness_key": "obs:refraction-constraint-depth"
        },
        {
          "row_index": 241,
          "witness_key": "obs:relocation-gap"
        },
        {
          "row_index": 242,
          "witness_key": "obs:relocation-iterations"
        },
        {
          "row_index": 243,
          "witness_key": "obs:relocation-obs-count"
        },
        {
          "row_index": 244,
          "witness_key": "obs:relocation-rms"
        },
        {
          "row_index": 245,
          "witness_key": "obs:relocation-uncertainty"
        },
        {
          "row_index": 246,
          "witness_key": "obs:rms-residual-cap"
        },
        {
          "row_index": 247,
          "witness_key": "obs:solubility-temperature"
        },
        {
          "row_index": 248,
          "witness_key": "obs:station-gap-cap"
        },
        {
          "row_index": 249,
          "witness_key": "obs:studied-portion-length"
        },
        {
          "row_index": 250,
          "witness_key": "obs:subdataset-arrivals"
        },
        {
          "row_index": 251,
          "witness_key": "obs:subdataset-gap"
        },
        {
          "row_index": 252,
          "witness_key": "obs:subsection-length"
        },
        {
          "row_index": 253,
          "witness_key": "obs:velest-iterations"
        },
        {
          "row_index": 254,
          "witness_key": "obs:velocity-perturbation"
        },
        {
          "row_index": 255,
          "witness_key": "obs:young-crust-age"
        },
        {
          "row_index": 256,
          "witness_key": "rel:askja-in-iceland"
        },
        {
          "row_index": 257,
          "witness_key": "rel:fagradalsfjall-in-iceland"
        },
        {
          "row_index": 258,
          "witness_key": "rel:logachev-of-knipovich"
        },
        {
          "row_index": 259,
          "witness_key": "rel:mar-in-eq-atlantic"
        },
        {
          "row_index": 260,
          "witness_key": "rel:marseg-bounded-chain"
        },
        {
          "row_index": 261,
          "witness_key": "rel:marseg-bounded-romanche"
        },
        {
          "row_index": 262,
          "witness_key": "rel:mayotte-in-indian-ocean"
        },
        {
          "row_index": 263,
          "witness_key": "rel:occ-on-mar"
        },
        {
          "row_index": 264,
          "witness_key": "rel:rc1-bounded-detachment"
        },
        {
          "row_index": 265,
          "witness_key": "rel:rc2-bounded-faults"
        },
        {
          "row_index": 266,
          "witness_key": "rel:romanche-faults-in-tf"
        },
        {
          "row_index": 267,
          "witness_key": "rel:vent-field-on-ntd1"
        },
        {
          "row_index": 268,
          "witness_key": "claim:co2-degassing-mechanism"
        },
        {
          "row_index": 269,
          "witness_key": "claim:co2-lab-melt"
        },
        {
          "row_index": 270,
          "witness_key": "claim:deep-eq-interpretation"
        },
        {
          "row_index": 271,
          "witness_key": "claim:deep-events-not-artifacts"
        },
        {
          "row_index": 272,
          "witness_key": "claim:keller-volatiles-flush"
        },
        {
          "row_index": 273,
          "witness_key": "claim:lab-melt-co2-h2o"
        },
        {
          "row_index": 274,
          "witness_key": "claim:magmatism-dominates"
        },
        {
          "row_index": 275,
          "witness_key": "claim:no-active-vents-rc2"
        },
        {
          "row_index": 276,
          "witness_key": "claim:no-eq-below-20km"
        },
        {
          "row_index": 277,
          "witness_key": "claim:no-eruption-evidence"
        },
        {
          "row_index": 278,
          "witness_key": "claim:small-pressure-increase"
        },
        {
          "row_index": 279,
          "witness_key": "claim:tomography-normal-vpvs"
        },
        {
          "row_index": 280,
          "witness_key": "claim:volatiles-reduce-solidus"
        },
        {
          "row_index": 281,
          "witness_key": "obs:mar-events-317"
        },
        {
          "row_index": 282,
          "witness_key": "obs:romanche-events-197"
        },
        {
          "row_index": 283,
          "witness_key": "obs:co2-ba-rc2"
        },
        {
          "row_index": 284,
          "witness_key": "obs:co2-ba-rc3"
        },
        {
          "row_index": 285,
          "witness_key": "obs:co2-ba90-rc2"
        },
        {
          "row_index": 286,
          "witness_key": "obs:co2-ba90-rc3"
        },
        {
          "row_index": 287,
          "witness_key": "obs:co2-calc-rc2"
        },
        {
          "row_index": 288,
          "witness_key": "obs:co2-calc-rc3"
        },
        {
          "row_index": 289,
          "witness_key": "obs:co2-pre-eruptive-rc2"
        },
        {
          "row_index": 290,
          "witness_key": "obs:co2-primary-rc2-floor"
        },
        {
          "row_index": 291,
          "witness_key": "obs:co2-rb-rc2"
        },
        {
          "row_index": 292,
          "witness_key": "obs:co2-rb-rc3"
        },
        {
          "row_index": 293,
          "witness_key": "obs:co2-rb90-rc2"
        },
        {
          "row_index": 294,
          "witness_key": "obs:co2-rb90-rc3"
        },
        {
          "row_index": 295,
          "witness_key": "obs:lab-water-content"
        },
        {
          "row_index": 296,
          "witness_key": "obs:rc2-ba"
        },
        {
          "row_index": 297,
          "witness_key": "obs:rc2-rb"
        },
        {
          "row_index": 298,
          "witness_key": "obs:swir-highest-co2"
        },
        {
          "row_index": 299,
          "witness_key": "obs:abstract-deep-eq-depth"
        },
        {
          "row_index": 300,
          "witness_key": "obs:bdb-at-ntd2"
        },
        {
          "row_index": 301,
          "witness_key": "obs:bdb-depth-if-cold"
        },
        {
          "row_index": 302,
          "witness_key": "obs:bdb-isotherm-fig6"
        },
        {
          "row_index": 303,
          "witness_key": "obs:bdb-isotherm-slow"
        },
        {
          "row_index": 304,
          "witness_key": "obs:bdb-isotherms-cold"
        },
        {
          "row_index": 305,
          "witness_key": "obs:bdb-shallow-offaxis"
        },
        {
          "row_index": 306,
          "witness_key": "obs:coverage-mar-axis"
        },
        {
          "row_index": 307,
          "witness_key": "obs:coverage-romanche"
        },
        {
          "row_index": 308,
          "witness_key": "obs:crust-thickness-rc2"
        },
        {
          "row_index": 309,
          "witness_key": "obs:deep-eq-bsf"
        },
        {
          "row_index": 310,
          "witness_key": "obs:deep-eq-rc2-1619"
        },
        {
          "row_index": 311,
          "witness_key": "obs:deep-microseismicity-rc2"
        },
        {
          "row_index": 312,
          "witness_key": "obs:depth-range-ntd2"
        },
        {
          "row_index": 313,
          "witness_key": "obs:depth-range-occ"
        },
        {
          "row_index": 314,
          "witness_key": "obs:hot-mantle-temperature"
        },
        {
          "row_index": 315,
          "witness_key": "obs:iceland-depths"
        },
        {
          "row_index": 316,
          "witness_key": "obs:lab-melt-fraction"
        },
        {
          "row_index": 317,
          "witness_key": "obs:mantle-temperature-rc2"
        },
        {
          "row_index": 318,
          "witness_key": "obs:mar-half-spreading-rate"
        },
        {
          "row_index": 319,
          "witness_key": "obs:mayotte-depths"
        },
        {
          "row_index": 320,
          "witness_key": "obs:normal-depth-ntd2"
        },
        {
          "row_index": 321,
          "witness_key": "obs:ntd1-length"
        },
        {
          "row_index": 322,
          "witness_key": "obs:ntd2-eq-depth"
        },
        {
          "row_index": 323,
          "witness_key": "obs:ntd2-offset"
        },
        {
          "row_index": 324,
          "witness_key": "obs:offaxis-microseismicity-depth"
        },
        {
          "row_index": 325,
          "witness_key": "obs:rc2-length"
        },
        {
          "row_index": 326,
          "witness_key": "obs:rc3-length"
        },
        {
          "row_index": 327,
          "witness_key": "obs:shallow-eq-rti"
        },
        {
          "row_index": 328,
          "witness_key": "obs:subsolidus-temperature"
        },
        {
          "row_index": 329,
          "witness_key": "obs:temperature-below-20km"
        },
        {
          "row_index": 330,
          "witness_key": "claim:cruise-thanks"
        },
        {
          "row_index": 331,
          "witness_key": "claim:vp-vs-reasonable"
        },
        {
          "row_index": 332,
          "witness_key": "obs:obs-no-data"
        },
        {
          "row_index": 333,
          "witness_key": "obs:instrument-spacing"
        },
        {
          "row_index": 334,
          "witness_key": "obs:vp-vs-test-range"
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
