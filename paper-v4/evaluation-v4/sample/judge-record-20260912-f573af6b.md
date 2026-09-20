# Independent judge record for a sampled witness set

Blank. Copy this file, edit only the JSON block below, and leave the prose
alone. The judging session fills it under
`paper-v4/evaluation-v4/sample/judge-task.template.md` as the dispatching
session instantiated it.

`sample_sha256` is the digest of the sample file the packet was built from, in
the form `sha256:<hex>`. `judgements` carries one entry per sampled witness,
exactly once each, with that witness's own `cell` and `witness_key` copied from
the packet. `source_support` is one of `SUPPORTED`, `PARTIAL`, `UNSUPPORTED`,
`NOT_EVALUABLE`. Every `rationale` is your own words: a rationale that shares a
sixty-character run with the reading is refused.

This record is a second opinion on a sample. It is not a protocol v3 review, it
is not ratified, and no figure in it reaches the paper on its own. Write no
total, no percentage and no aggregate anywhere in this file.

Hand it back when it is complete. The dispatching session validates it with
`paper-v4/evaluation-v4/sample/validate_judge_record.py`, which needs the sample
file; a judging session does not open that file, because its name says which
stratum the packet came from.

```json
{
  "schema": "malleus.paper-v4.independent-judge-record/v1",
  "sample_sha256": "sha256:f573af6bea6d425b72918d39923e3ca14aff9fe2c9bf03b6510b4cf25fd88338",
  "judge": {
    "evaluator_kind": "INDEPENDENT_MODEL_JUDGE",
    "model_id": "claude-fable-5-1",
    "actor_id": "actor:fable-judge-20260912-f573af6b",
    "reasoning_effort": "harness default, not pinned or observed"
  },
  "judgements": [
    {
      "cell": "run-22-v413",
      "witness_key": "agent:anne-briais",
      "source_support": "SUPPORTED",
      "rationale": "Tested that A.B. is a person contributor; the author-contributions block lists A.B. among those doing structural analysis."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "agent:cedric-hamelin",
      "source_support": "SUPPORTED",
      "rationale": "Tested that C.H. is a person contributor; the block credits C.H. with collecting and interpreting geochemical data."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "agent:lea-grenet",
      "source_support": "SUPPORTED",
      "rationale": "Tested that L.G. is a person contributor; the block names L.G. as a collector of geochemical data."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "boundary:isotherm-750",
      "source_support": "SUPPORTED",
      "rationale": "Tested the entity as a 750 degree isotherm; the figure caption identifies a dashed line as exactly that isotherm."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "claim:axial-valley-floor-character",
      "source_support": "SUPPORTED",
      "rationale": "Tested the three-part description of the axial valley floor (highs, ridge-parallel normal faults, basaltic constructions); the block states all three."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "claim:ba90-rb90-calculated",
      "source_support": "SUPPORTED",
      "rationale": "Tested the procedure claim and its calculated modality; the block opens with the authors computing Ba90 and Rb90 as concentrations in melts at equilibrium with Fo90 olivine."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "claim:bdb-shallower-southward",
      "source_support": "SUPPORTED",
      "rationale": "Tested the expectation that the BDB shallows southward with distance from the RTI; the block's first sentence says so and attributes it to a waning cold-edge effect. The subject BDB is named there under its abbreviation."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "claim:compiled-maximum-depths",
      "source_support": "SUPPORTED",
      "rationale": "Tested that maximum depths and full spreading rates were compiled worldwide for slow and ultraslow ridges; the methods block describes exactly that compilation."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "claim:deep-eq-interpreted-as-degassing",
      "source_support": "SUPPORTED",
      "rationale": "Tested the interpretation of deep events as volume change from CO2 degassing of ascending melt; the figure caption states it in those terms and names the ascending melt as the source."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "claim:deep-events-not-location-artifact",
      "source_support": "SUPPORTED",
      "rationale": "Tested the claim that the unexpected axial depths are not a location artefact; the block draws that conclusion from a shallow off-axis cluster and ties it to the MAR axis."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "claim:deepest-earthquakes-documented",
      "source_support": "SUPPORTED",
      "rationale": "Tested the comparative claim that these are the deepest events recorded at a slow-spreading centre to date; the block asserts it directly."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "claim:fixed-depth-rms-worse",
      "source_support": "PARTIAL",
      "rationale": "The block confirms final RMS residuals were higher when depths were fixed, but the initial-RMS part of the claim rests on a truncated opening clause whose subject is not in the block."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "claim:max-depths-affected-by-processes",
      "source_support": "SUPPORTED",
      "rationale": "Tested the list of processes affecting maximum depth; the caption names detachment faults, hydrothermal vents, volcanoes or hotspots and transform faults with their symbols."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "claim:melt-focused-beneath-ridge-axis",
      "source_support": "SUPPORTED",
      "rationale": "Tested the background statement that melt focuses into a narrow axial zone; the block's closing sentence says so."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "claim:no-competing-interests",
      "source_support": "SUPPORTED",
      "rationale": "Tested the competing-interests declaration and its negated modality; the two-line block is that declaration."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "claim:ntd1-magmatic-tectonic-origin",
      "source_support": "SUPPORTED",
      "rationale": "Tested that pillow basalts plus peridotites are read as evidence of combined magmatic and tectonic origin; the block makes that inference for NTD1."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "claim:primary-vs-pre-eruptive",
      "source_support": "SUPPORTED",
      "rationale": "Tested the distinction between primary melts (in equilibrium with the source) and pre-eruptive melts; the block's final sentence draws exactly that distinction."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "claim:ultraslow-ridges-high-co2",
      "source_support": "SUPPORTED",
      "rationale": "Tested the hypothesised high CO2 at ultraslow ridges with deep mantle earthquakes; the block says it is likely and names the SWIR as one such ridge."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "claim:updated-compiled-data",
      "source_support": "SUPPORTED",
      "rationale": "Tested that two SWIR segments and the Logachev Seamount were updated with relocated data; the block names segment 8, the oblique Supersegment and Logachev as updated."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "claim:velocity-model-set",
      "source_support": "SUPPORTED",
      "rationale": "Tested the composition of the five velocity models; the block enumerates the northern flank, transform valley, southern flank, a low-velocity variant and an average model across the Romanche TF."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "cnt:new-focal-mechanisms",
      "source_support": "SUPPORTED",
      "rationale": "Tested the count of three new well-constrained focal mechanisms; the block reports obtaining three under the stated selection criteria."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "cnt:non-transform-discontinuities",
      "source_support": "SUPPORTED",
      "rationale": "Tested the count of two non-transform discontinuities offsetting the studied ridge portion; the block gives that number."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "cnt:relocated-events",
      "source_support": "SUPPORTED",
      "rationale": "Tested the count of 364 double-difference relocated events; the block states 364 twice."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "feature:detachment-fault-rti",
      "source_support": "SUPPORTED",
      "rationale": "Tested the detachment fault as westward dipping and bounding the RTI segment on the east; the block describes it that way."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "feature:extinct-vent-field",
      "source_support": "SUPPORTED",
      "rationale": "Tested the existence and kind of an extinct hydrothermal vent field; the block reports one on the eastern flank of NTD1."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "feature:gakkel",
      "source_support": "SUPPORTED",
      "rationale": "Tested Gakkel Ridge as a spreading ridge; the block cites it as an example of an ultraslow-spreading ridge."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "feature:ntd1",
      "source_support": "SUPPORTED",
      "rationale": "Tested NTD1 as a non-transform discontinuity oriented N76E; the first block introduces it as the first NTD and the second gives its length and that orientation."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "feature:ntd1-faults",
      "source_support": "SUPPORTED",
      "rationale": "Tested the fault set and its two strike directions; the block says NTD1 is marked by many faults striking N118E and east-west."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "obs:axial-event-depth-stability",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 10 to 20 km range within which most axial events stay across velocity models; the depth-resolution block states that range."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "obs:bdb-depth-ntd2",
      "source_support": "SUPPORTED",
      "rationale": "Tested the BDB depth of about 10 km beneath NTD2; the block infers that value from microseismicity reaching 10 km there."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "obs:brittle-lithospheric-thickness",
      "source_support": "SUPPORTED",
      "rationale": "Tested the brittle lithospheric thickness bound of under 10 km; the block derives it from the expected maximum earthquake depth at this spreading rate."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "obs:dry-melting-depth",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 60 to 70 km onset depth of extensive dry melting in the mantle; the block gives that range and links it to mantle upwelling."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "obs:equatorial-atlantic-co2-average",
      "source_support": "SUPPORTED",
      "rationale": "Tested the roughly 2800 ppm average CO2 at equatorial Atlantic segments as an estimate from prior work; the block reports that average from CO2/Rb and CO2/Ba estimations."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "obs:high-frequency-energy-threshold",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 5 Hz threshold above which some deep events lack energy; the block states the absence of energy above 5 Hz for some deep earthquakes."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "obs:lithosphere-age-cold-edge",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 45 Ma age of the cold lithosphere behind the cold-edge effect; the block gives that age in parentheses."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "obs:mantle-temperature-gt-1100",
      "source_support": "SUPPORTED",
      "rationale": "Tested the mantle temperature bound above 1100 degrees where the events occur; the block's last clause states it."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "obs:mean-vertical-error",
      "source_support": "SUPPORTED",
      "rationale": "Tested the mean vertical error of about 2.9 km; the block reports that value alongside the horizontal error."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "obs:ntd2-eq-depth-down-to",
      "source_support": "SUPPORTED",
      "rationale": "Tested that earthquakes beneath NTD2 reach at most about 10 km; the block gives under 10 km and down to about 10 km for NTD2."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "obs:subsection-length",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 20 to 50 km length of the subsections; the block describes four subsections of that length."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "ref:002",
      "source_support": "SUPPORTED",
      "rationale": "Tested the reference title and journal-article kind; the entry gives that title with a Nature volume, pages and year."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "ref:019",
      "source_support": "SUPPORTED",
      "rationale": "Tested the title, given in the record with the extraction's letter spacing, against the entry for reference 19; the same spaced title appears there with a Geophys. J. Int. citation."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "ref:020",
      "source_support": "SUPPORTED",
      "rationale": "Tested the Bonatti et al. title and journal kind; the two blocks together carry the title and a JGR Solid Earth volume, pages and year."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "ref:023",
      "source_support": "SUPPORTED",
      "rationale": "Tested the SEISAN software reference as a journal article; the paired blocks give the title and a Seismol. Res. Lett. citation."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "ref:031",
      "source_support": "SUPPORTED",
      "rationale": "Tested the Ligi et al. title and kind; the entry carries that title with a Nature citation."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "ref:034",
      "source_support": "SUPPORTED",
      "rationale": "Tested the Cannat et al. title and kind; the entry gives that title with a Geology citation."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "ref:037",
      "source_support": "SUPPORTED",
      "rationale": "Tested the Molnar title and kind; the entry gives that title with a JGR Solid Earth article number and year."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "ref:040",
      "source_support": "SUPPORTED",
      "rationale": "Tested the White et al. title and kind; the paired blocks give the title and a Philosophical Transactions citation."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "ref:070",
      "source_support": "SUPPORTED",
      "rationale": "Tested the Hutton and Boore title and kind; the paired blocks give the title and a BSSA volume, pages and year."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "rel:mar-within-equatorial-atlantic",
      "source_support": "SUPPORTED",
      "rationale": "Tested the located-within relation between the MAR and the equatorial Atlantic; the block introduces the ridge as lying in that ocean and describes its spreading."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "rel:rc1-bounded-by-detachment",
      "source_support": "SUPPORTED",
      "rationale": "Tested that RC1 is bounded by the detachment fault; the block names the RTI segment RC1 and says it is bounded to the east by a westward-dipping detachment."
    },
    {
      "cell": "run-22-v413",
      "witness_key": "source:cc-licence",
      "source_support": "SUPPORTED",
      "rationale": "Tested the licence identity and URL; the block names the CC BY-NC-ND 4.0 licence and gives that address, line-broken where the record shows a space."
    },
    {
      "cell": "run-23",
      "witness_key": "agent:brunelli",
      "source_support": "SUPPORTED",
      "rationale": "Tested Daniele Brunelli as a person; the author line lists him and the contributions block carries his initials."
    },
    {
      "cell": "run-23",
      "witness_key": "agent:singh",
      "source_support": "SUPPORTED",
      "rationale": "Tested Satish C. Singh as a person; he is in the author line and named as a corresponding author."
    },
    {
      "cell": "run-23",
      "witness_key": "award:zjnsf",
      "source_support": "SUPPORTED",
      "rationale": "Tested the Zhejiang foundation award and its identifier; the acknowledgements give that funder with the same grant number."
    },
    {
      "cell": "run-23",
      "witness_key": "claim:all-authors-discussed",
      "source_support": "SUPPORTED",
      "rationale": "Tested the statement that all authors discussed results and commented on the manuscript; the block ends with that sentence."
    },
    {
      "cell": "run-23",
      "witness_key": "claim:co2-solubility-pressure",
      "source_support": "SUPPORTED",
      "rationale": "Tested the solubility argument (pressure and water dependence, dissolved at depth, gas phase near the seafloor); the block lays out each step."
    },
    {
      "cell": "run-23",
      "witness_key": "claim:enriched-basalts-low-melting",
      "source_support": "SUPPORTED",
      "rationale": "Tested the interpretation of enriched basalts as low-degree melting of an enriched source near the Romanche TF; the block states it and cites prior studies."
    },
    {
      "cell": "run-23",
      "witness_key": "claim:extinct-vent-too-far",
      "source_support": "SUPPORTED",
      "rationale": "Tested that the extinct vent field on NTD1's eastern flank is too distant to affect the RC2 lithosphere; the block makes that argument."
    },
    {
      "cell": "run-23",
      "witness_key": "claim:h1-cold-lithosphere",
      "source_support": "SUPPORTED",
      "rationale": "Tested the cold-thick-lithosphere hypothesis for RC2 and its not-supported disposition; the block presents it as one explanation then argues against it from magmatic morphology and hot mantle."
    },
    {
      "cell": "run-23",
      "witness_key": "claim:long-period-events",
      "source_support": "SUPPORTED",
      "rationale": "Tested the inference from missing high-frequency energy to possible long-period events; the block states it with a hedge that matches the hypothesised modality."
    },
    {
      "cell": "run-23",
      "witness_key": "claim:mechanism-similar-volcanoes",
      "source_support": "SUPPORTED",
      "rationale": "Tested the analogy to CO2-driven magma expansion beneath volcanoes and the possible deep long-period events; the block's first two sentences carry both."
    },
    {
      "cell": "run-23",
      "witness_key": "claim:no-active-vents-rc2",
      "source_support": "SUPPORTED",
      "rationale": "Tested the negated observation of active vents on the RC2 axis; the block states none have been observed."
    },
    {
      "cell": "run-23",
      "witness_key": "claim:occ-shallow-ruptures",
      "source_support": "SUPPORTED",
      "rationale": "Tested the attribution of shallow OCC-dome events to high-angle normal faults; the block says they likely result from such ruptures."
    },
    {
      "cell": "run-23",
      "witness_key": "claim:rc2-rc3-analysed",
      "source_support": "SUPPORTED",
      "rationale": "Tested that samples from RC2 and the adjacent southern RC3 were analysed; the methods block says so."
    },
    {
      "cell": "run-23",
      "witness_key": "claim:rti-amagmatic",
      "source_support": "SUPPORTED",
      "rationale": "Tested that the RTI segment RC1 is amagmatic; the block names RC1 and calls it amagmatic."
    },
    {
      "cell": "run-23",
      "witness_key": "claim:tests-support-deep",
      "source_support": "SUPPORTED",
      "rationale": "Tested that depth-resolution tests back the deep depths; the block's last sentence says they do."
    },
    {
      "cell": "run-23",
      "witness_key": "claim:volatile-controls-magma",
      "source_support": "SUPPORTED",
      "rationale": "Tested the general statement on volatiles controlling magma properties and eruption dynamics; the block's final sentence states it."
    },
    {
      "cell": "run-23",
      "witness_key": "claim:vpvs-reasonable",
      "source_support": "SUPPORTED",
      "rationale": "Tested the Vp/Vs 1.7 result (lowest RMS, most located events, deemed reasonable); the block reports all three."
    },
    {
      "cell": "run-23",
      "witness_key": "cnt:new-focal-mechanisms",
      "source_support": "SUPPORTED",
      "rationale": "Tested the count of three new focal mechanisms; the block states three were obtained."
    },
    {
      "cell": "run-23",
      "witness_key": "cnt:relocation-iterations",
      "source_support": "SUPPORTED",
      "rationale": "Tested five relocation iterations and a 6 km maximum event separation; the block gives both values."
    },
    {
      "cell": "run-23",
      "witness_key": "gchem:rc2-co2-preeruptive",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 0.7 to 4.6 wt% pre-eruptive CO2 estimate for RC2; the block gives that range for that segment."
    },
    {
      "cell": "run-23",
      "witness_key": "gchem:rc3-co2-rb",
      "source_support": "SUPPORTED",
      "rationale": "Tested the Rb-derived pre-eruptive CO2 range of 0.07 to 1.0 wt% for RC3; the block reports that range."
    },
    {
      "cell": "run-23",
      "witness_key": "geo:mar",
      "source_support": "SUPPORTED",
      "rationale": "Tested the entity name Mid-Atlantic Ridge; the title block and the introduction block both name it in full."
    },
    {
      "cell": "run-23",
      "witness_key": "geo:moho",
      "source_support": "SUPPORTED",
      "rationale": "Tested the Moho as the expected Moho interface; the figure labels carry Moho and the caption describes the expected interface as a dashed red line."
    },
    {
      "cell": "run-23",
      "witness_key": "geo:ntd1",
      "source_support": "SUPPORTED",
      "rationale": "Tested NTD1 as a non-transform discontinuity oriented N76E; the introduction names it as the first NTD and the second block gives that orientation."
    },
    {
      "cell": "run-23",
      "witness_key": "instr:obs",
      "source_support": "SUPPORTED",
      "rationale": "Tested the OBSs as the ocean-bottom seismometers whose records the study uses; both blocks describe the 19-instrument OBS network that acquired the data."
    },
    {
      "cell": "run-23",
      "witness_key": "obs:axial-event-depth-stability",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 10 to 20 km band in which most axial events stay across five velocity models; the depth-resolution block states that result."
    },
    {
      "cell": "run-23",
      "witness_key": "obs:coverage-mar",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 120 km of MAR axis covered by the network; the results block lists that figure among the network's coverage."
    },
    {
      "cell": "run-23",
      "witness_key": "obs:full-spreading-rate",
      "source_support": "SUPPORTED",
      "rationale": "Tested the roughly 32 mm/yr full spreading rate used to predict maximum depth; the block opens with that rate as the premise of the prediction."
    },
    {
      "cell": "run-23",
      "witness_key": "obs:h1-isotherms",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 600 to 800 degree isotherms tied to a BDB near 20 km under the cold-lithosphere hypothesis; the block gives that pairing inside the hypothesis and the record marks it hypothesised."
    },
    {
      "cell": "run-23",
      "witness_key": "obs:lithosphere-age-45ma",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 45 Ma age of the cold lithosphere behind the RTI cold-edge effect; the block gives that age."
    },
    {
      "cell": "run-23",
      "witness_key": "obs:mean-horizontal-error",
      "source_support": "SUPPORTED",
      "rationale": "Tested the mean horizontal error of about 2.8 km; the block reports it next to the vertical error."
    },
    {
      "cell": "run-23",
      "witness_key": "obs:melting-initiation-depth",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 150 to 300 km onset of small-degree melting; the block gives that approximate range in the presence of volatiles."
    },
    {
      "cell": "run-23",
      "witness_key": "obs:ntd2-offset",
      "source_support": "SUPPORTED",
      "rationale": "Tested the roughly 33 km ridge offset of NTD2; the block gives that offset together with the N110E orientation the subject carries."
    },
    {
      "cell": "run-23",
      "witness_key": "obs:rc2-valley-width",
      "source_support": "PARTIAL",
      "rationale": "The 10 km width of the RC2 median valley is in the block as a plain description, but the record marks the value hypothesised, a status the block reserves for the inference about magmatic robustness, not for the width."
    },
    {
      "cell": "run-23",
      "witness_key": "obs:rc3-length",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 50 km length of RC3; the block's final sentence gives that length and the orientation the subject carries."
    },
    {
      "cell": "run-23",
      "witness_key": "obs:relocation-gap",
      "source_support": "SUPPORTED",
      "rationale": "Tested the azimuthal gap bound under 270 degrees for relocated events; the block lists it among the relocation criteria."
    },
    {
      "cell": "run-23",
      "witness_key": "obs:relocation-obs-threshold",
      "source_support": "SUPPORTED",
      "rationale": "Tested that relocated events were detected on more than six OBSs; the block states that threshold."
    },
    {
      "cell": "run-23",
      "witness_key": "ratio:co2-rb",
      "source_support": "SUPPORTED",
      "rationale": "Tested the global CO2/Rb ratio of 991 plus or minus 129 from undegassed MORBs and melt inclusions; the block gives that value with that provenance."
    },
    {
      "cell": "run-23",
      "witness_key": "rel:rc2-adjacent-ntd1",
      "source_support": "SUPPORTED",
      "rationale": "Tested the adjacency of RC2 to NTD1; the block describes RC2 as the segment lying south of NTD1."
    },
    {
      "cell": "run-23",
      "witness_key": "work:ref-001",
      "source_support": "SUPPORTED",
      "rationale": "Tested author, title, journal, volume, pages and year for reference 1; the two blocks carry each of them."
    },
    {
      "cell": "run-23",
      "witness_key": "work:ref-003",
      "source_support": "SUPPORTED",
      "rationale": "Tested the bibliographic fields for reference 3; the entry matches authors, title, Nature, volume 440, pages and 2006."
    },
    {
      "cell": "run-23",
      "witness_key": "work:ref-005",
      "source_support": "SUPPORTED",
      "rationale": "Tested the bibliographic fields for reference 5; the entry matches authors, title, journal, volume 45, pages and 1979."
    },
    {
      "cell": "run-23",
      "witness_key": "work:ref-013",
      "source_support": "SUPPORTED",
      "rationale": "Tested the bibliographic fields for reference 13; the entry matches authors, title, Geology, volume 47, pages and 2019."
    },
    {
      "cell": "run-23",
      "witness_key": "work:ref-021",
      "source_support": "SUPPORTED",
      "rationale": "Tested the conference-abstract kind, authors, title, container, DOI and year; the entry carries each, with the abstract number the record files under pages."
    },
    {
      "cell": "run-23",
      "witness_key": "work:ref-059",
      "source_support": "SUPPORTED",
      "rationale": "Tested the bibliographic fields for reference 59; the entry matches authors, title, Nature Geoscience, volume 10, pages and 2017."
    },
    {
      "cell": "run-23",
      "witness_key": "work:ref-066",
      "source_support": "SUPPORTED",
      "rationale": "Tested the bibliographic fields for reference 66; the paired blocks carry the four authors, title, journal, volume 99, pages and 1994."
    },
    {
      "cell": "run-23",
      "witness_key": "work:zenodo",
      "source_support": "SUPPORTED",
      "rationale": "Tested Zenodo as a database; the data-availability block says the catalog was deposited in the Zenodo database."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:basaltic-rocks",
      "source_support": "SUPPORTED",
      "rationale": "Tested basaltic rocks as basalt; the block reports basaltic rocks observed on the seafloor confirming basaltic constructions."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:brittle-lithosphere",
      "source_support": "SUPPORTED",
      "rationale": "Tested the brittle lithosphere entity, named with the block's hyphenation break; the block's last sentence discusses its thickness at the NTDs."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:claim:lab-melt",
      "source_support": "SUPPORTED",
      "rationale": "Tested the interpretation that CO2 influences melt beneath the LAB; the abstract's final sentence makes that claim."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:claim:magmatic-tectonic",
      "source_support": "SUPPORTED",
      "rationale": "Tested the magmatic-tectonic hypothesis and its not-supported disposition; the first block introduces it as the third possibility and the second block says the melt-movement mechanism does not apply."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:claim:not-artifact",
      "source_support": "SUPPORTED",
      "rationale": "Tested the negated claim that the depths are a location artefact; the block reaches that conclusion from a shallow off-axis cluster."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:claim:ultraslow-co2-high",
      "source_support": "SUPPORTED",
      "rationale": "Tested the hypothesised high CO2 at ultraslow ridges with deep mantle earthquakes; the block says it is likely based on the model."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:data:zenodo",
      "source_support": "PARTIAL",
      "rationale": "The block confirms the Zenodo deposit and the DOI prefix, but the block ends mid-identifier and the recorded DOI is that truncated prefix, so the identifier claim is incomplete."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:knipovich",
      "source_support": "SUPPORTED",
      "rationale": "Tested the Knipovich Ridge entity; the block names it as the ridge hosting the Logachev Seamount."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:lab",
      "source_support": "SUPPORTED",
      "rationale": "Tested the lithosphere-asthenosphere boundary as a boundary of that kind; both blocks name it in full, the second with its LAB abbreviation."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:main-axial-faults",
      "source_support": "SUPPORTED",
      "rationale": "Tested the main axial normal faults as normal faults; the block says the deep events align parallel to them."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:melt-inclusions",
      "source_support": "SUPPORTED",
      "rationale": "Tested olivine melt inclusions as melt inclusions; the block names them as a source of the global ratio trends."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:melt:primary",
      "source_support": "SUPPORTED",
      "rationale": "Tested primary melts at the primary stage; the abstract names them and the second block describes calculating CO2 in melts in equilibrium with the mantle source."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:model:average-velocity",
      "source_support": "SUPPORTED",
      "rationale": "Tested the average velocity model as a numerical model; the block describes it as one of five 1-D P-wave models and the best fitting."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:model:fastest",
      "source_support": "SUPPORTED",
      "rationale": "Tested the fastest model (Model 1) as a numerical model; the block names it and describes its origin and effect on locations."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:model:iacono-marziano",
      "source_support": "SUPPORTED",
      "rationale": "Tested the Iacono-Marziano solubility model as a numerical model used in calculation; the block says solubility was calculated with it."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:obs",
      "source_support": "SUPPORTED",
      "rationale": "Tested the ocean-bottom seismometers entity; all three blocks name the instruments."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:person:briais",
      "source_support": "SUPPORTED",
      "rationale": "Tested Anne Briais as a person; the author line names her and the contributions block carries her initials."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:b-value-groups",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 0.89 to 0.93 b values for the three groups; the magnitude block gives that range."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:brittle-thickness-ntds",
      "source_support": "SUPPORTED",
      "rationale": "Tested the at-most-10 km brittle thickness at the segment boundaries; the block's closing sentence gives that bound for the NTDs."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:dry-melting-onset",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 60 to 70 km onset of extensive dry melting; the block gives that range."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:fixed-depth-range",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 10 to 20 km depth range of the fixed-depth subset; the block describes the 45-event subset at those depths."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:fixed-depth-subset",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 45-event subset along cross-section cc prime; the block gives that count and scope."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:focal-gap",
      "source_support": "SUPPORTED",
      "rationale": "Tested the under-180 degree azimuthal gap criterion; the block lists it among the focal mechanism selection criteria."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:focal-new",
      "source_support": "SUPPORTED",
      "rationale": "Tested the count of three new focal mechanisms; the block reports three."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:located-514",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 514 located earthquakes near the Romanche RTI; the block opens with that count."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:mar-317",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 317 events along the MAR; the block gives that number."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:no-quakes-below-20",
      "source_support": "SUPPORTED",
      "rationale": "Tested the negated observation of events deeper than 20 km beneath RC2; the block states none are seen there."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:ntd2-offset",
      "source_support": "SUPPORTED",
      "rationale": "Tested the roughly 33 km ridge offset of NTD2; the block gives it with the N110E orientation."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:obs-spacing-focal",
      "source_support": "SUPPORTED",
      "rationale": "Tested the roughly 30 km OBS spacing as the limit on focal mechanism quality; the block cites that spacing as the main reason."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:rc2-primary-ba90",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 0.4 to 3.0 wt% Ba90-based primary melt CO2 for RC2; the block gives that range."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:rc3-co2-rb",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 0.07 to 1.0 wt% Rb-based CO2 for RC3; the block gives that range."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:saturating-melt-co2",
      "source_support": "SUPPORTED",
      "rationale": "Tested the above-0.7 wt% CO2 melt that would saturate under the solubility model; the block gives that threshold and the saturation depth."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:studied-portion-length",
      "source_support": "SUPPORTED",
      "rationale": "Tested the roughly 120 km length and the two offsetting NTDs; the block states both."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:subdataset",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 360-earthquake sub-dataset with its arrival and gap criteria; the block gives count and criteria."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:temp-below-20",
      "source_support": "SUPPORTED",
      "rationale": "Tested the above-1200 degree temperature below 20 km as a modelled hypothesis; the block offers it as a possible cause with a hedge."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:updated-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "Tested the roughly 2.1 km updated horizontal uncertainty; the block's last clause gives it."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:volatile-melting-onset",
      "source_support": "SUPPORTED",
      "rationale": "Tested the roughly 150 to 300 km onset of melting with volatiles; the block gives that range."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:rc2-axial-faults",
      "source_support": "SUPPORTED",
      "rationale": "Tested the ridge-parallel normal faults as normal faults; the block describes them cutting the axial valley floor."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:rc2-median-valley",
      "source_support": "SUPPORTED",
      "rationale": "Tested the median valley as an axial valley; the block describes RC2's typical 10 km wide median valley."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:ref:r17",
      "source_support": "SUPPORTED",
      "rationale": "Tested title, venue, volume, page range and year for reference 17; the entry carries each, the page range with the same spaced digits."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:ref:r18",
      "source_support": "SUPPORTED",
      "rationale": "Tested title, venue, volume, article number and year for reference 18; the paired blocks carry all of them."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:ref:r32",
      "source_support": "SUPPORTED",
      "rationale": "Tested title, venue, volume, article number and year for reference 32; the entry matches."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:ref:r5",
      "source_support": "SUPPORTED",
      "rationale": "Tested title, venue, volume, pages and year for reference 5; the entry matches."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:ref:r56",
      "source_support": "SUPPORTED",
      "rationale": "Tested title, venue, volume, pages and year for reference 56; the entry, despite its spaced author line, carries each."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:ref:r59",
      "source_support": "SUPPORTED",
      "rationale": "Tested title, venue, volume, pages and year for reference 59; the entry matches."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:ref:r70",
      "source_support": "SUPPORTED",
      "rationale": "Tested title, venue, volume, pages and year for reference 70; the paired blocks carry all of them."
    },
    {
      "cell": "run-25",
      "witness_key": "award:nsfc",
      "source_support": "SUPPORTED",
      "rationale": "Tested the two NSFC grant identifiers; the acknowledgements list both numbers after that funder."
    },
    {
      "cell": "run-25",
      "witness_key": "claim:deep-eq-alignment",
      "source_support": "SUPPORTED",
      "rationale": "Tested the alignment of the deep RC2 events along roughly N150E parallel to the main axial normal faults; the block states it."
    },
    {
      "cell": "run-25",
      "witness_key": "claim:focal-mechanisms-shown",
      "source_support": "SUPPORTED",
      "rationale": "Tested that focal mechanisms are displayed as beach balls; the Fig. 2 caption says they are shown as blue and white beach balls."
    },
    {
      "cell": "run-25",
      "witness_key": "claim:licence-terms",
      "source_support": "SUPPORTED",
      "rationale": "Tested the claim that the block states the licence terms; the block is the Open Access licence paragraph itself."
    },
    {
      "cell": "run-25",
      "witness_key": "claim:max-depth-not-following",
      "source_support": "SUPPORTED",
      "rationale": "Tested the negated statement that the maximum depth follows the BDB-depth versus spreading-rate relation; the sentence begins in the first block and its tail is the opening word of the second."
    },
    {
      "cell": "run-25",
      "witness_key": "claim:melt-continues-degassing",
      "source_support": "SUPPORTED",
      "rationale": "Tested the proposal that migrating melt keeps degassing and produces 10 to 20 km events; the block's final sentence makes it with a conditional verb."
    },
    {
      "cell": "run-25",
      "witness_key": "claim:melt-focusing",
      "source_support": "SUPPORTED",
      "rationale": "Tested the focusing of melt beneath the ridge axis; the block's closing sentence says so."
    },
    {
      "cell": "run-25",
      "witness_key": "claim:melt-freeze-lithosphere",
      "source_support": "SUPPORTED",
      "rationale": "Tested the proposed freezing of melt at the lithosphere base yielding sub-horizontal reflections; the block offers it as a possibility."
    },
    {
      "cell": "run-25",
      "witness_key": "claim:melt-movement-strain",
      "source_support": "SUPPORTED",
      "rationale": "Tested the mechanism of melt movement inducing high strain rates and brittle failure in the ductile lower crust; the block's last sentence states it."
    },
    {
      "cell": "run-25",
      "witness_key": "claim:melt-resides-fractionates",
      "source_support": "SUPPORTED",
      "rationale": "Tested the proposed residence, fractionation and evolution of melt at 10 to 20 km; the block infers it from the microseismicity with a hedge."
    },
    {
      "cell": "run-25",
      "witness_key": "claim:occ-dome-ruptures",
      "source_support": "SUPPORTED",
      "rationale": "Tested the proposed origin of shallow events beneath the OCC dome; the block attributes them, with a hedge, to high-angle normal fault ruptures."
    },
    {
      "cell": "run-25",
      "witness_key": "claim:trace-element-assumption",
      "source_support": "SUPPORTED",
      "rationale": "Tested the stated assumption behind trace-element CO2 estimates; the block spells out that trace elements must reflect the source unaltered by secondary processes."
    },
    {
      "cell": "run-25",
      "witness_key": "claim:vp-vs-reasonable",
      "source_support": "SUPPORTED",
      "rationale": "Tested the support for a Vp/Vs of about 1.7 from lowest residuals and most located events; the block reports both and calls the setting reasonable."
    },
    {
      "cell": "run-25",
      "witness_key": "feature:askja",
      "source_support": "SUPPORTED",
      "rationale": "Tested Askja as a volcano; the first block names Askja Volcano in Iceland as a site of magmatic-tectonic events."
    },
    {
      "cell": "run-25",
      "witness_key": "feature:ntd1-faults",
      "source_support": "SUPPORTED",
      "rationale": "Tested the NTD1 faults and their two strike directions; the block gives N118E and east-west."
    },
    {
      "cell": "run-25",
      "witness_key": "feature:ntd2",
      "source_support": "SUPPORTED",
      "rationale": "Tested NTD2 as a non-transform discontinuity oriented N110E; the first block introduces it as the second NTD and the second gives the orientation."
    },
    {
      "cell": "run-25",
      "witness_key": "feature:occ",
      "source_support": "SUPPORTED",
      "rationale": "Tested the OCC as an oceanic core complex; the block introduces the abbreviation with its expansion."
    },
    {
      "cell": "run-25",
      "witness_key": "feature:romanche-tf",
      "source_support": "SUPPORTED",
      "rationale": "Tested the Romanche TF as a transform fault; the blocks name it among the TFs and describe the Romanche transform."
    },
    {
      "cell": "run-25",
      "witness_key": "method:double-difference",
      "source_support": "SUPPORTED",
      "rationale": "Tested the double-difference location method as a named method; the results block says hypocenters were relocated with it."
    },
    {
      "cell": "run-25",
      "witness_key": "method:focal-mechanism",
      "source_support": "SUPPORTED",
      "rationale": "Tested the method entity for determining focal mechanism solutions; the code-availability block names that use for the HASH software."
    },
    {
      "cell": "run-25",
      "witness_key": "method:oct-tree",
      "source_support": "SUPPORTED",
      "rationale": "Tested the non-linear oct-tree search algorithm; the block names it as the NonLinLoc method for initial hypocenters."
    },
    {
      "cell": "run-25",
      "witness_key": "model:north-flank",
      "source_support": "SUPPORTED",
      "rationale": "Tested the northern-flank model as a 1-D P-wave velocity model; the block lists it among the five such models."
    },
    {
      "cell": "run-25",
      "witness_key": "obs:avg-horizontal-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "Tested the roughly 2.1 km average horizontal uncertainty after relocation; the figure caption, the map legend and the methods block all give it."
    },
    {
      "cell": "run-25",
      "witness_key": "obs:co2-pre-eruptive-rc2",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 0.7 to 4.6 wt% pre-eruptive CO2 estimate for RC2; the block gives that range."
    },
    {
      "cell": "run-25",
      "witness_key": "obs:coverage-mar-axis",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 120 km of MAR axis covered by the network; the results block gives that figure."
    },
    {
      "cell": "run-25",
      "witness_key": "obs:coverage-romanche",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 140 km eastern portion of the Romanche TF covered by the network; the results block gives that figure."
    },
    {
      "cell": "run-25",
      "witness_key": "obs:crust-thickness-rc2",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 5.4 plus or minus 0.3 km crustal thickness beneath RC2; the Fig. 6 caption gives that value."
    },
    {
      "cell": "run-25",
      "witness_key": "obs:eq-atlantic-co2-average",
      "source_support": "SUPPORTED",
      "rationale": "Tested the roughly 2800 ppm average CO2 at equatorial Atlantic segments from ratio-based estimates; the block attributes that figure to prior studies' suggestions."
    },
    {
      "cell": "run-25",
      "witness_key": "obs:eq-atlantic-co2-max",
      "source_support": "SUPPORTED",
      "rationale": "Tested the roughly 8799 ppm upper CO2 value at equatorial Atlantic segments; the block gives it as the maximum reached."
    },
    {
      "cell": "run-25",
      "witness_key": "obs:fm-gap",
      "source_support": "SUPPORTED",
      "rationale": "Tested the under-180 degree azimuthal gap criterion; the block lists it."
    },
    {
      "cell": "run-25",
      "witness_key": "obs:fm-polarities",
      "source_support": "SUPPORTED",
      "rationale": "Tested the more-than-8 P-wave polarities criterion; the block lists it first among the selection criteria."
    },
    {
      "cell": "run-25",
      "witness_key": "obs:forced-depth-subset",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 45-event forced-depth subset at 10 to 20 km along cc prime; the block gives count, depth range and the forcing procedure."
    },
    {
      "cell": "run-25",
      "witness_key": "obs:located-514",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 514 located earthquakes; both blocks state that count."
    },
    {
      "cell": "run-25",
      "witness_key": "obs:mar-events-317",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 317 events on the MAR profile; the figure panel label and the methods block both give 317 for the MAR."
    },
    {
      "cell": "run-25",
      "witness_key": "obs:pore-pressure-trigger",
      "source_support": "PARTIAL",
      "rationale": "The 2 to 3 bar pore-pressure threshold is in the block, but stated as an established premise from the literature; the record marks it hypothesised, which the block reserves for the authors' suggestion built on it."
    },
    {
      "cell": "run-25",
      "witness_key": "obs:quality-c-uncertainty",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 5 km uncertainty bound for quality C events; the figure legend text in the block gives that bound for quality C."
    },
    {
      "cell": "run-25",
      "witness_key": "obs:romanche-events-197",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 197 events on the Romanche TF profile; the panel label and the methods block both give 197 for the transform."
    },
    {
      "cell": "run-25",
      "witness_key": "obs:swir-highest-co2",
      "source_support": "SUPPORTED",
      "rationale": "Tested the 1.9 wt% highest reported CO2 at the SWIR; the block gives that value and lists the SWIR as ultraslow-spreading."
    },
    {
      "cell": "run-25",
      "witness_key": "org:eu",
      "source_support": "SUPPORTED",
      "rationale": "Tested the European Union as an organization; the acknowledgements name its Seventh Framework Program."
    },
    {
      "cell": "run-25",
      "witness_key": "org:sio",
      "source_support": "SUPPORTED",
      "rationale": "Tested the Second Institute of Oceanography and its full affiliation description; the affiliation line gives exactly that."
    },
    {
      "cell": "run-25",
      "witness_key": "org:zjnsf",
      "source_support": "SUPPORTED",
      "rationale": "Tested the Zhejiang foundation as an organization; the acknowledgements name it as a funder."
    },
    {
      "cell": "run-25",
      "witness_key": "rel:logachev-of-knipovich",
      "source_support": "SUPPORTED",
      "rationale": "Tested the part-of relation of Logachev Seamount to Knipovich Ridge; the block phrases the seamount as belonging to that ridge in a compilation of slow and ultraslow ridges."
    },
    {
      "cell": "run-25",
      "witness_key": "rel:occ-on-mar",
      "source_support": "SUPPORTED",
      "rationale": "Tested the OCC as located on the MAR; the Fig. 1 caption places it on the ridge's outside corner and expands MAR."
    },
    {
      "cell": "run-25",
      "witness_key": "rel:rc2-bounded-faults",
      "source_support": "SUPPORTED",
      "rationale": "Tested that RC2 is bounded by high-angle NNW-SSE inward-dipping faults; the block states it and adds the absence of detachment faults."
    },
    {
      "cell": "run-25",
      "witness_key": "rel:zmap-used-for-catalog",
      "source_support": "SUPPORTED",
      "rationale": "Tested the ZMAP-to-catalog-analysis use and the access URL; the code-availability block gives both."
    },
    {
      "cell": "run-25",
      "witness_key": "software:gmt",
      "source_support": "SUPPORTED",
      "rationale": "Tested GMT 6 and its download URL; the URL is split across the two blocks and matches when joined."
    },
    {
      "cell": "run-25",
      "witness_key": "software:hypodd",
      "source_support": "SUPPORTED",
      "rationale": "Tested hypoDD, version 1.3 and its URL; the methods block names its use and the code block gives version and address."
    },
    {
      "cell": "run-25",
      "witness_key": "work:ref-13",
      "source_support": "SUPPORTED",
      "rationale": "Tested the bibliographic fields for reference 13; the entry matches authors, title, Geology, volume, pages and year."
    },
    {
      "cell": "run-25",
      "witness_key": "work:ref-27",
      "source_support": "SUPPORTED",
      "rationale": "Tested authors, title, container, pages, DOI, year and the web-resource kind; the entry gives all of them with a DOI and no volume."
    },
    {
      "cell": "run-25",
      "witness_key": "work:ref-32",
      "source_support": "SUPPORTED",
      "rationale": "Tested the bibliographic fields for reference 32; the entry matches."
    },
    {
      "cell": "run-25",
      "witness_key": "work:ref-33",
      "source_support": "SUPPORTED",
      "rationale": "Tested the bibliographic fields for reference 33; the paired blocks carry authors, title, journal, volume, pages and year."
    },
    {
      "cell": "run-25",
      "witness_key": "work:ref-53",
      "source_support": "SUPPORTED",
      "rationale": "Tested the bibliographic fields for reference 53; the entry matches authors, title, Nature, volume, pages and year."
    },
    {
      "cell": "run-25",
      "witness_key": "work:ref-6",
      "source_support": "SUPPORTED",
      "rationale": "Tested the bibliographic fields for reference 6; the paired blocks carry authors, title, JGR, volume 92, article number and year."
    },
    {
      "cell": "run-25",
      "witness_key": "work:ref-67",
      "source_support": "SUPPORTED",
      "rationale": "Tested the bibliographic fields for reference 67; the entry matches authors, title, EPSL, volume, article number and year."
    },
    {
      "cell": "run-25",
      "witness_key": "work:ref-69",
      "source_support": "SUPPORTED",
      "rationale": "Tested the bibliographic fields for reference 69; the entry matches authors, title, Reviews of Geophysics, volume, pages and year."
    },
    {
      "cell": "run-25",
      "witness_key": "work:ref-7",
      "source_support": "SUPPORTED",
      "rationale": "Tested the book-chapter kind, authors, title, series, pages, DOI and year; the paired blocks give an edited series with page range, DOI, publisher and 1992."
    }
  ]
}
```
