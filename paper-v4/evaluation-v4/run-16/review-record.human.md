# Malleus paper v4 run-16 source-grounded review record

Template. The row counts are substituted at freeze, from the frozen cell's own
query result, at the same time as `paper-v4/evaluation-v4/review-task-v4.template.md`.
No placeholder may survive instantiation.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

Fill one `rows` entry per returned row, in order, zero-based: 36 for
CQ-01, 112 for CQ-02, 144 for CQ-03, 141 for
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
  "status": "HUMAN_RATIFIED",
  "inputs": {
    "review_protocol_sha256": "sha256:88b69f6e80a3b9eac3a2c990178186df9c52fed3ced5c4e020162b0c202fa795",
    "review_input_manifest_sha256": "sha256:0bd70670db36c192617e2cbdca76f7c1808096ea45198fd17d8d6b727b7ad876"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-preliminary-run-16",
    "completed_at": "2026-09-05T20:55:28Z"
  },
  "questions": [
    {
      "question_id": "CQ-01",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "The rows name the SMARTIES cruise as the campaign and the ocean-bottom seismometer network as the observing system, tie the two with a part-of-campaign relation, carry nineteen deployed instruments on the campaign record together with a separate count of seventeen useful instruments, and describe the acquisition as a July and August 2019 passive OBS experiment recorded continuously for about three weeks. Every part of the question is answered from the reading. Most of the remaining rows are analysis software and catalogue statistics the question does not ask about, which is noise rather than a gap.",
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
            "page:6:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The Campaign projection carries no subject slot. Both cited blocks name the SMARTIES cruise: one gives the nineteen-instrument ocean-bottom seismometer network that acquired the microseismicity data and the roughly three-week continuous recording, the other gives the July and August 2019 passive OBS experiment. Every projected field is carried by those two blocks."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The Instrument projection carries no subject slot. The cited block states that the microseismicity data were acquired by a network of ocean-bottom seismometers during the SMARTIES cruise, which is what the projected name and description assert."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The Method projection carries no subject slot. The cited block states that five one-dimensional P-wave velocity models were constructed, so the projected name is the prose's own term."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The Method projection carries no subject slot. The cited block applies a CO2 solubility model to the melt, which is the single field the row projects."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The Method projection carries no subject slot. The code-availability block names Global Mapper, states it was used for structural analysis and gives the address the description repeats."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The Method projection carries no subject slot. The code-availability block names the GMT 6 toolbox, which is the only field the row projects."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The Method projection carries no subject slot. One cited block names the HASH package as the tool used to determine focal mechanisms; the other gives its version, the same purpose and the address. Name and description are both carried."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:7:block:006",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The Method projection carries no subject slot. The Results block states hypocenters were relocated with a double-difference location method, the Methods block names the hypoDD program doing it, and the availability block gives the version, the purpose and the address. Name and description are both carried."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The Method projection carries no subject slot. The cited block attributes the theoretical CO2 solubility calculation to the model of Iacono-Marziano and colleagues, which is the projected name."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The Method projection carries no subject slot. The cited block states that earthquake magnitudes were determined on the local magnitude scale ML."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:7:block:004",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The Method projection carries no subject slot. The Results block calls it a non-linear earthquake location algorithm, the Methods block names NonLinLoc locating the initial hypocenters, and the availability block gives the address. Name and description are both carried."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The Method projection carries no subject slot. The cited block states an active-source wide-angle seismic refraction profile was used to find the best 1-D velocity model, which is the projected name."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The Method projection carries no subject slot. One block places the automatic trigger and the earthquake register inside the SEISAN package, the other gives its phase-picking purpose and the address. Name and description are both carried."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The Method projection carries no subject slot. The cited block states that initial arrivals were detected automatically with a short-term-average/long-term-average trigger algorithm."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The Method projection carries no subject slot. One block states VELEST was used to search for the minimum 1-D velocity model, the other gives the inversion purpose and the address. Name and description are both carried."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The Method projection carries no subject slot. One block states ZMAP produced the magnitude completeness and the b value, the other gives the same catalogue-analysis purpose and the address. Name and description are both carried."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DERIVATION_LOCAL The relation's own assertion and the assertions formalizing both endpoints all sit in the same Results block. That block states the microseismicity data were acquired by a network of nineteen ocean-bottom seismometers during the SMARTIES cruise, so the network belonging to that campaign is what the prose asserts, and the direction from instrument to campaign matches it."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:7:block:008"
          ],
          "rationale": "SUBJECT_IN_BLOCK The SMARTIES cruise is named in the block the subject derivation reaches, and that block establishes that the located microseismicity is the cruise's own data. The value block carries the approximate 78 per cent of located earthquakes meeting at least two location-quality criteria. Subject and value rest on different blocks; together they support the row."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:8:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK The subject block names the SMARTIES cruise and ties the earthquake catalogue to it; the value block states the b value of 0.87 was calculated. Subject and value come from different blocks and both hold, and the calculated modality matches the prose."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:8:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK The subject block names the SMARTIES cruise; the value block divides the earthquakes into three groups and gives the small spread of their b values, which is the range the row projects. The two blocks together support both parts."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:8:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK The subject block names the SMARTIES cruise; the value block gives the magnitude completeness of 1.5 as a calculated figure. Subject and value rest on different blocks and both hold."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:7:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The subject block names the SMARTIES cruise and identifies its microseismicity data; the value block gives the approximate mean horizontal error of 2.8 km for the located events. The split across two blocks is the only complication and both halves hold."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:7:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The subject block names the SMARTIES cruise; the same value block that carries the horizontal figure gives the approximate mean vertical error of 2.9 km. Both halves hold."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK Here the value block itself names the SMARTIES cruise and then states that 760 earthquakes were identified and registered, so the count and its attribution to the campaign sit in one place; the second block repeats the cruise as the source of the data."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK The subject block names the ocean-bottom seismometers; the value block states each event was checked manually to confirm detection by at least five OBSs. The quantity counts instruments of the network, so it is a property of the subject, and the open lower bound matches the at-least phrasing."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries both halves: it names the ocean-bottom seismometers and gives the approximate 30 km instrument spacing. Spacing is a property of the network itself, so the subject attribution is what the prose asserts."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries both halves: it names the ocean-bottom seismometers and states that arrivals were detected from 17 useful OBSs. The count is a count of the subject's own instruments."
        },
        {
          "row_index": 27,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:006",
            "page:7:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK The hypoDD program is named in the block the subject derivation reaches and the other block states that 276 events were well relocated, so the value holds. The count is a count of this study's earthquakes, not a property of the relocation program, so the block does not support the record being about hypoDD."
        },
        {
          "row_index": 28,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block names hypoDD and carries the 364 well-constrained relocated events in the same sentence, so the value holds. The count is still of earthquakes rather than of the program, so the subject attribution is not what the prose asserts."
        },
        {
          "row_index": 29,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block names the HASH package and states that three new well-constrained focal mechanism solutions were obtained, so the value holds. The count is of solutions produced in this study, not a property of the software, so the record is not about HASH in the way the subject slot claims."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004",
            "page:7:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK The value block names NonLinLoc and states it estimates a three-dimensional error ellipsoid at 68 per cent confidence. The confidence level is a property of what the program estimates, so both the value and the subject attribution are carried by the prose; the second block is where the program's short name is introduced."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries both halves: the solubility calculation is said to follow the Iacono-Marziano model with a temperature of 1200 degrees Celsius among its parameters. The temperature is a stated parameter of that model's application, so the subject attribution holds with the value."
        },
        {
          "row_index": 32,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block names the HASH package and gives six focal mechanisms as the total, so the value holds. The block also says three of the six come from previously published swarm solutions, and the total is a count of solutions rather than a property of the software, so the record is not about HASH."
        },
        {
          "row_index": 33,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK The block names the VELEST program and states that a 360-earthquake sub-dataset was constructed for the velocity-model check, so the value holds. The count is of earthquakes assembled by the authors, not a property of the program, so the subject attribution is not supported."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries both halves: it states that five 1-D P-wave velocity models were constructed. The quantity counts the subject's own kind, so value and subject attribution are both what the prose asserts."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK The subject block names the active-source wide-angle refraction profile; the value block states that this profile provides velocity constraints down to about 60 km below sea level. The depth constraint is a property of the profile itself, so both halves hold; the approximation on the figure is carried as an upper bound rather than as an approximate value."
        }
      ]
    },
    {
      "question_id": "CQ-02",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The named subsection is answered squarely: the rows carry segment RC2 as a ridge segment and attach the deep-microseismicity depth records to it, with ten to twenty kilometres, sixteen to nineteen kilometres and ten to nineteen kilometres below seafloor all present, alongside the shallower populations at the core complex and the second discontinuity for contrast. The axis-relative part is weaker. No returned row projects a field that says the deep events lie beneath the segment's ridge axis; the depth records carry only a quantity kind of earthquake depth and a subject, and the axis relation exists only in the prose of the blocks they derive from. The vocabulary can express it, since one row's quantity kind marks off-axis shallow microseismicity, which makes its absence on the deep records the gap. Beyond that, most of the returned rows are geochemistry, spreading rates, uncertainties and comparison sites the question does not ask about.",
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
          "rationale": "NO_SUBJECT_IN_ROW The tectonic-feature projection carries no subject slot. The cited block names Askja Volcano among the Icelandic magmatic-tectonic settings, and the volcano kind is the noun the source itself uses."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW No subject slot on this projection. The cited block introduces the brittle-ductile boundary as what separates cooled brittle lithosphere above from the partially molten material below, which carries both the name and the boundary classification."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW No subject slot on this projection. The cited block says the RTI segment is bounded to the east by a westward dipping detachment fault, giving both the name and the fault kind."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW No subject slot on this projection. The cited block names the Fagradalsfjall Peninsula among the Icelandic comparison sites; the kind is left unspecified, which the block also does."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW No subject slot on this projection. The cited block names the Gakkel Ridge as an ultraslow-spreading ridge where deep mantle earthquakes have been observed."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW No subject slot on this projection. The cited block reports an extinct hydrothermal vent field on the eastern flank of NTD1, giving both the name and the vent-field kind."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW No subject slot on this projection. The cited block refers to reflections observed beneath the young Juan de Fuca plate, so the name and the plate classification are the source's own."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW No subject slot on this projection. The cited block names Knipovich Ridge in the list of sites whose reported depths were updated."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW No subject slot on this projection. The cited block names the lithosphere-asthenosphere boundary as the place melt may accumulate, giving the name and its boundary character."
        },
        {
          "row_index": 9,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW No subject slot on this projection. The cited block names the Logachev Seamount of Knipovich Ridge, so the name holds, but nothing in the block says the seamount is a volcano; that classification comes from outside the reading."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW No subject slot on this projection. The cited block names the Mid-Atlantic Ridge in the equatorial Atlantic as the study's setting; the kind is left unspecified."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW No subject slot on this projection. The cited block names offshore Mayotte Island in the western Indian Ocean, and the island kind is the source's own noun."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "NO_SUBJECT_IN_ROW No subject slot on this projection. The cited figure caption names the expected Moho interface, which supports both the name and its treatment as a boundary."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW No subject slot on this projection. The cited block lists the first NTD among the four subsections and says the studied ridge is offset by two non-transform discontinuities, which is where the kind comes from."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW No subject slot on this projection. The same block names the second NTD as one of the four subsections and identifies the NTDs as non-transform discontinuities."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW No subject slot on this projection. The cited block names the prominent oceanic core complex on the eastern side of the ridge axis, carrying both name and kind."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW No subject slot on this projection. The cited block names the Rainbow massif and says it sits at a non-transform discontinuity; the row leaves the kind unspecified, which the block does not contradict."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW No subject slot on this projection. The cited block names the RTI segment as one of the ridge subsections and describes it as amagmatic, so the name and the ridge-segment classification both hold."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW No subject slot on this projection. The cited block introduces a short ridge segment named RC2 among the four subsections of the studied ridge, which is exactly the name and the kind the row carries."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW No subject slot on this projection. The cited block says the ridge segment south of NTD2 is named RC3, carrying name and kind together."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW No subject slot on this projection. The cited block names the Romanche TF as part of the area covered by the network; the transform-fault reading of the abbreviation is the one the source uses throughout."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW No subject slot on this projection. The cited block names the Southwest Indian Ridge as the comparison ridge for the cold-lithosphere explanation."
        },
        {
          "row_index": 22,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:5:block:010",
            "page:1:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The relation's assertion and the assertions formalizing both endpoints all sit in the same block. That block carries the source claim, Keller and colleagues' suggestion that volatiles flush melt away from the axis to the LAB, and the abstract block carries the target claim about CO2 in the primitive melt influencing melt at that boundary. Neither cited block states that the first supports the second; the paper makes that connection in a later block the derivation does not reach, so the endpoints hold and the supporting link does not."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:012",
            "page:1:block:005",
            "page:5:block:002"
          ],
          "rationale": "DERIVATION_LOCAL The relation's block is also one of the blocks that formalize the source observation. That figure caption states the ten to nineteen kilometre deep earthquakes beneath the ridge axis are interpreted as a consequence of CO2 degassing from ascending melts, which is the supporting link, the depth figures and the preferred hypothesis in one place."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The relation's block also formalizes the source observation. That block sets out the cold and thick lithosphere explanation and then turns against it with the segment's volcanic morphology and magmatic origin, so the challenging direction is what the prose does."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001",
            "page:3:block:003"
          ],
          "rationale": "DERIVATION_LOCAL The relation's block also formalizes the source observation. The mylonite shear-zone hypothesis is stated in the earlier block, which then says the observations do not support it and runs straight into the cited block's statement that the segment shows no evidence of detachment faults, so the challenge is explicit across the sentence boundary."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003",
            "page:4:block:002",
            "page:5:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The relation's block is among those formalizing the source observation. The magmatic-tectonic possibility is raised in one block, and the cited block sets the study apart from it, noting no evidence of a current eruption, before the following block rejects the melt-movement mechanism outright."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002",
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The relation's block also formalizes the source observation. One block carries both sides: the hydrothermal cooling hypothesis, then the absence of active vents on the segment axis and the reasoning that the one extinct field is too far away to matter."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005",
            "page:5:block:002"
          ],
          "rationale": "DERIVATION_LOCAL The relation's block also formalizes the source observation. That block gives the calculated CO2 enrichment for the segment and, in the same clause, marks it as the segment where the deep mantle earthquakes are observed, which is the evidential tie to the preferred hypothesis stated in the other cited block."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:004",
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_NON_LOCAL The relation is formalized in a block that formalizes neither endpoint; both features are introduced on page one and the pairing is asserted later. On the reading the pairing holds: the block states that microseismicity down to ten kilometres beneath NTD2 shows the boundary is indeed at about that depth, which places the boundary at that discontinuity."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL One block formalizes the relation and both endpoints. It says the RTI segment is bounded to the east by the westward dipping detachment fault, which is the relation and its direction."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002",
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The relation's block also formalizes the source feature. That block places the extinct vent field on the eastern flank of NTD1, which supports locating the field at that discontinuity."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002",
            "page:5:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK The segment is named in the block the subject derivation reaches and again in the block that gives the claim. The prose calls CO2 degassing from ascending melt the fourth possibility and the authors' preferred one for the deep microseismicity beneath that segment, which matches the hypothesised modality and the preferred disposition."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010",
            "page:1:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The boundary is named in the block the subject derivation reaches and in the abstract block. The abstract states that the large CO2 concentration in the primitive melt will influence the presence of melt beneath that boundary, which is the claim and its forward-looking, not-yet-established character."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The segment is named in both cited blocks. The second gives the cold and thick lithosphere as one explanation for the deep earthquakes and then argues against it from the segment's magmatic morphology, matching the hypothesised modality and the not-supported disposition."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK The segment is named in both cited blocks. The second states the hydrothermal cooling hypothesis for the large earthquake depths and then finds no active vents on the segment axis, which is where the not-supported disposition comes from."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It attributes to Keller and colleagues the suggestion that volatiles in ascending melt flush melt away from the axial area to accumulate at the boundary, which is the claim, its subject and its reported-statement character."
        },
        {
          "row_index": 37,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:4:block:002",
            "page:5:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The segment is named in the block the subject derivation reaches. The other two blocks carry the magmatic-tectonic possibility and its rejection, which supports the claim and its not-supported disposition, but neither ties that possibility to this segment; they say only these deep earthquakes, and the block that names the segment says nothing about earthquakes."
        },
        {
          "row_index": 38,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:002",
            "page:3:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK The transform fault is named in the block the subject derivation reaches. The hypothesis and its rejection are supported by the other block, but the hypothesis there is about deep earthquakes in the mantle along transform faults generally and is rejected for the study's own axial valley, so making this particular transform fault the subject is not what the prose asserts."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK The fault is named in the block the subject derivation reaches, which also places the core complex beside it. The other block says the absence of deep microseismicity near the core-complex termination suggests that detachment fault is inactive, so the two together identify the fault and give its activity state."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK The segment is named in both cited blocks. The second says the calculated solubility values are very close to the measured contents and concludes the samples are degassed, which is the claim. The block reaches that conclusion for two segments and the row pins it to one, which narrows the scope without misstating it."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row: the abstract reports deep earthquakes at ten to twenty kilometres depth in the mantle along the ridge axis, naming the ridge, so the depth range and its attachment to that ridge are both there."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It names Askja Volcano and gives depths greater than ten kilometres for the Icelandic sites, which is the open lower bound the row records."
        },
        {
          "row_index": 43,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:7:block:009"
          ],
          "rationale": "SUBJECT_IN_BLOCK The segment is named in the block the subject derivation reaches. The value block gives the approximate average depth uncertainty for the axial events and supports the figure, but it never names the segment, and the naming block says nothing about earthquakes, so the attachment of this uncertainty to that segment is not carried by either cited block."
        },
        {
          "row_index": 44,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:002",
            "page:3:block:004",
            "page:7:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK The transform fault is named in two of the cited blocks. The approximate average horizontal uncertainty after relocation is supported, but the prose gives it as a property of the relocated catalogue as a whole, not of the transform fault, so the value holds and the subject attribution does not."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It says the microseismicity down to ten kilometres beneath the second discontinuity reveals the boundary is indeed at about that depth, which is the quantity, its approximation and its subject."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. The figure caption says the line representing the boundary corresponds to the 750 degree isotherm, which is the modelled temperature the row records."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It states that off-axis shallow microseismicity indicates the boundary remains shallow, below ten kilometres depth, near the ridge, which is the open upper bound recorded."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:1:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK The boundary is named in both cited blocks. The second states that the maximum depth of earthquakes, corresponding to the 700 plus or minus 100 degree isotherms, is what defines the boundary at slow-spreading ridges, which gives the value and the stated uncertainty."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK The discontinuity is named in both cited blocks. The second says the brittle lithosphere is at most about ten kilometres thick at the segment boundaries, and separately puts the earthquakes beneath this discontinuity down to about ten kilometres, so the upper bound holds for it; the source states it for the discontinuities as a class and the row pins it to one of them."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK The segment is named in both cited blocks. The value block says degassed CO2 stays dissolved at depth but saturates and nucleates a gas phase, with eighty to ninety per cent lost, by the time it reaches the seafloor, and it frames that inside the argument for this segment's earthquakes; the figure is a general solubility result applied to the segment rather than a measurement on it."
        },
        {
          "row_index": 51,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK The segment is named in both cited blocks. The underlying statement is that the CO2 to rubidium and CO2 to barium ratios are a good proxy for CO2 concentration, which is a statement about the method and not about the segment, so the subject attribution is not what the prose asserts. The projection also carries no name or description, so the row shows only modality and determination."
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK The segment is named in both cited blocks. The value block says the melt would saturate with CO2 at about twenty-five kilometres depth and start degassing, which is the approximate saturation depth recorded."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK The segment is named in both cited blocks. The same sentence gives the saturation pressure of about 0.7 gigapascals, matching the value and its approximation."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK The segment is named in both cited blocks. The same sentence gives 1250 degrees as the saturation temperature, stated without hedging, which is how the row records it."
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:006",
            "page:7:block:011"
          ],
          "rationale": "SUBJECT_IN_BLOCK The segment is named in all three cited blocks. One gives the crustal thickness of 5.4 plus or minus 0.3 kilometres from refraction work on the western flank and the figure caption states the same thickness for the crust beneath this segment, so value, uncertainty and subject all hold."
        },
        {
          "row_index": 56,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:7:block:012"
          ],
          "rationale": "SUBJECT_IN_BLOCK The segment is named in the block the subject derivation reaches. The value block gives the ten to nineteen kilometre depth range below seafloor but places those earthquakes beneath the ridge axis without naming this segment, so the depth range holds while the attachment to this particular segment is not carried by either cited block."
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It reports deep earthquakes at sixteen to nineteen kilometres beneath this segment's axis, which is the measured range and its subject in one sentence."
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It states that deep microseismicity at roughly ten to twenty kilometres lies beneath the ridge axis of this segment, giving the depth range, its approximation and the segment together."
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:009"
          ],
          "rationale": "SUBJECT_IN_BLOCK The ridge is named in the block the subject derivation reaches, which also places it in the equatorial Atlantic. The value block reports an average of about 2800 parts per million across several segments in that same equatorial Atlantic range, so the segments in question are that ridge's and the figure holds."
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:009"
          ],
          "rationale": "SUBJECT_IN_BLOCK Same pairing as the average figure: the naming block places the ridge in the equatorial Atlantic and the value block reports concentrations reaching up to about 8799 parts per million across several segments there, which the row records as an upper bound."
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK The ridge is named in the block the subject derivation reaches, where its half-spreading rate is also given. The value block says that at a full spreading rate of about thirty-two millimetres a year the maximum earthquake depth should be under ten kilometres, which is the expectation for this ridge at that rate."
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK The ridge is named in the block the subject derivation reaches, which gives sixteen millimetres a year as the half rate. The value block states the full rate of about thirty-two millimetres a year for the same setting, so value and subject both hold."
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row: it names the ridge and states that it spreads here at a half-spreading rate of sixteen millimetres a year."
        },
        {
          "row_index": 64,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:008"
          ],
          "rationale": "SUBJECT_IN_BLOCK The segment is named in the block the subject derivation reaches. The value block says spectral analyses show some deep earthquakes without high-frequency energy above five hertz, which supports the threshold and the negated character, but that block never names the segment and the naming block says nothing about earthquakes."
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It concludes that these earthquakes occur in a hot mantle at temperatures above 1100 degrees and names the segment in the same passage, which is the open lower bound and its subject."
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It states that under the cold and thick lithosphere explanation the boundary would be about twenty kilometres deep, which is the value together with its hypothetical standing."
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It reports the proposal that about 1.1 per cent of melt is required at the base of that boundary, which is the modelled fraction; the source's approximation mark is not reflected in the row's qualification."
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. The same proposal gives a water content of up to 332 parts per million at that boundary, which the row records as an upper bound."
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It concludes that magmatism dominates the crustal accretion process at this segment, which is the observation and its subject; the projection carries no name or description, so modality and determination are all the row shows."
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It says the network covered 120 kilometres of the ridge axis, naming the ridge, which is the along-strike coverage recorded."
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It gives depths greater than thirty kilometres offshore Mayotte Island, which is the open lower bound and its subject."
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It states there are no observations of active hydrothermal vents on this segment's axis, which is the negated observation and its subject."
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It says no earthquakes are observed deeper than twenty kilometres beneath this segment's ridge axis, giving the bound, its negated character and the subject together."
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It places normal-depth earthquakes of four to ten kilometres beneath the southern second discontinuity, which is the range and its subject."
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It states the first discontinuity is about thirty-five kilometres long, matching the value and its approximation."
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It states the second discontinuity has an approximately thirty-three kilometre ridge offset, which is the quantity kind, the value and the subject."
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It says the expected depth range is observed beneath the second discontinuity at under ten kilometres, which is the observed maximum recorded as an upper bound."
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. The same sentence gives under six kilometres beneath the core complex, which is this row's upper bound and subject."
        },
        {
          "row_index": 79,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The segment is named in the block the subject derivation reaches. The value block describes swarm-like off-axis shallow microseismicity under ten kilometres west of the ridge axis, which supports the bound and the off-axis character, but it does not name the segment and the naming block carries no seismicity, so the attachment is not in either cited block."
        },
        {
          "row_index": 80,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:1:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK The segment is named in the block the subject derivation reaches. The abstract block gives the calculated CO2 quantity of roughly 0.4 to 3.0 weight per cent in the primary melts, so the value and its approximation hold, but the abstract speaks of primary melts without naming a segment, so pinning it to this one is not supported by either cited block."
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It says all samples in this segment are enriched in incompatible trace elements with barium above 89 parts per million, which is the value, the bound and the subject."
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It gives the barium-based pre-eruptive estimate of 0.7 to 4.6 weight per cent for this segment, matching value, quantity kind and subject."
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It gives the barium-ninety primary-melt estimate of 0.4 to 3.0 weight per cent for this segment, which is exactly what the row records."
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It reports melts along this segment as significantly enriched in volatiles at a calculated 0.4 to 3.0 weight per cent CO2, which is the value, its calculated status and its subject."
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It gives the rubidium-based pre-eruptive estimate of 0.9 to 4.3 weight per cent for this segment."
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It gives the rubidium-ninety primary-melt estimate of 0.5 to 2.8 weight per cent for this segment."
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It concludes that the deep events beneath the ridge axis of this segment are well constrained, required by the data and not artifacts, naming the segment in the same sentence."
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It says the segment south of the first discontinuity is about twenty-two kilometres long, matching value, approximation and subject."
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It infers from hummocky volcanic morphology, volcanic cones and a neo-volcanic ridge that this segment is of magmatic origin; the projection carries no name or description, so only modality and determination show."
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. The same sentence that gives the segment's length gives its typical ten-kilometre-wide median valley, which is the width recorded; the source's word typical is not reflected in a qualification."
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:4:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK The segment is named in both cited blocks. The value block states there is no evidence of a current volcanic eruption in the axial valley and, in the same passage, discusses the deep earthquakes beneath this segment's axis, so the negated observation and its subject both hold."
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It says this segment is bounded by high-angle inward dipping faults and shows no evidence for detachment faults, which is the negated observation and its subject."
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It states that tomographic results indicate normal velocity ratios in this segment, naming it directly."
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It gives estimated pre-eruptive CO2 concentrations from 0.7 to 4.6 weight per cent for this segment, matching value, estimated status and subject."
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. The same enrichment sentence gives rubidium above 8 parts per million for this segment's samples, which is the value and its lower bound."
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It gives the barium-based pre-eruptive estimate of 0.06 to 0.8 weight per cent for the southern segment named in the row."
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It gives the barium-ninety primary-melt estimate of 0.04 to 0.5 weight per cent for that southern segment."
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It gives the calculated CO2 of 0.04 to 0.7 weight per cent for the southern segment as the comparison against the studied one."
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It gives the rubidium-based pre-eruptive estimate of 0.07 to 1.0 weight per cent for the southern segment."
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It gives the rubidium-ninety primary-melt estimate of 0.05 to 0.7 weight per cent for the southern segment."
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It says the southern segment is a fifty-kilometre-long magmatic segment, which is the length and the subject."
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:7:block:010"
          ],
          "rationale": "SUBJECT_IN_BLOCK The segment is named in both cited blocks. The value block says a subset of forty-five events at ten to twenty kilometres depth was built to validate the deep locations beneath this segment, so the count is of that segment's own events and both value and subject hold."
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It says the network covered the 140-kilometre eastern part of the transform fault, which is the along-strike coverage and its subject."
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It places the majority of shallow earthquakes at zero to six kilometres on the outside corner of the intersection beneath the core-complex faulted dome, which is the range and the subject."
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It names the ridge and states that the studied portion is about 120 kilometres in length, matching the value and its approximation."
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It reports the highest melt CO2 amount at that ridge as 1.9 weight per cent, which is the value and its subject."
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It attributes the absence of earthquakes below twenty kilometres beneath this segment's axis to higher temperatures above 1200 degrees at those depths, which is the modelled lower bound recorded."
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK One block carries the whole row. It says thermal modelling suggests 1100 to 1200 degrees at ten to twenty kilometres depth and concludes the mantle beneath this segment's axis is hot, giving value, modelled status and subject."
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:004",
            "page:7:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK The ridge is named in all three cited blocks. One states plainly that 317 events were located along that ridge, so the count and its attachment to the ridge are both what the prose asserts."
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:3:block:003",
            "page:7:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK The transform fault is named in all three cited blocks. The same sentence that gives the ridge total says 197 events were located along the transform fault, so count and subject both hold."
        },
        {
          "row_index": 111,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:002",
            "page:2:block:003",
            "page:6:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK The transform fault is named in the block the subject derivation reaches. The count of 514 located earthquakes is supported twice over, but the block that gives it places those events in the vicinity of the whole ridge-transform intersection region rather than on the transform fault, and the reading elsewhere splits that total between the ridge and the fault, so the value holds and the subject attribution does not."
        }
      ]
    },
    {
      "question_id": "CQ-03",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The returned rows do carry the parts the question asks for: earthquake depths at the central ridge segment, the calculated primary-melt carbon-dioxide range for that segment, a unit on every quantity, and a determination and modality that separate measured from calculated values. What they do not do is single out one answer. Several competing depth ranges are returned for overlapping subjects, and several carbon-dioxide ranges sit side by side for the same segment, primary against pre-eruptive and one trace-element proxy against the other, with the neighbouring southern segment's values in the same list and no field marking which pair the question is asking after. That ambiguity is material, so the rows address the question without resolving it. One further note on how I read the subject token on these rows: where a record's subject derives from a different assertion than its values, I based the token on the block carrying the values, since the naming block names every subject by construction and would make the token say nothing.",
      "source_locators": [
        "page:2:block:006",
        "page:5:block:005",
        "page:7:block:012",
        "page:8:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the methods block names the five one-dimensional P-wave velocity models the record is named for, which is the only field it projects."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the block the derivation reaches names the CO2 solubility model used to work out saturation conditions, matching the only projected field."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the code-availability block names Global Mapper and gives the structural-analysis use and address that the description projects."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the same availability block names the GMT 6 toolbox, which is all this record projects."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW one block names the package used for focal mechanisms and the other gives its version, use and address, covering both projected fields."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:7:block:006",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW between them the three blocks carry the relocation method, the program, its version and its address, so every projected field sits in the prose."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the methods block attributes the theoretical solubility calculation to the model the record is named after."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the magnitude block states that magnitudes were determined on the local magnitude scale, which is the only projected field."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:7:block:004",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the location algorithm, the program name and the address each appear in one of the blocks the derivations reach."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the results block names the active-source wide-angle refraction profile and its role in choosing the velocity model."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW one block names the package used in detection and the other gives the phase-picking use and address the description projects."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the results block names the trigger algorithm used for automatic detection."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW one block records the VELEST run and the other its inversion use and address."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the magnitude block attributes the completeness and b-value calculation to ZMAP and the availability block gives the use and address."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the figure block lists melt inclusions among the plotted sample sets, matching the projected name and sample kind."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the same figure block lists popping rocks among the plotted sample sets."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:6:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the geochemistry block establishes a sample set from segment RC2 and the figure block classes the plotted rocks as whole-rock MORB, covering both projected fields."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:6:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the same two blocks give the southern RC3 sample set and its whole-rock MORB character."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the alternative-hypothesis block names Askja Volcano, so both the name and the volcano classification sit in the prose."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the introduction block defines the brittle-ductile boundary as a lithospheric boundary fixed by the maximum earthquake depth."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the study-area block names the westward dipping detachment fault that bounds the ridge-transform intersection segment."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the block names Fagradalsfjall Peninsula and the record classifies it only as OTHER, which the prose does not contradict."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the assertion cited is about the Southwest Indian Ridge maximum, but the block it sits in names Gakkel Ridge among the ultraslow-spreading ridges with deep mantle earthquakes, so the projected name is in the block."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the hypothesis block reports an extinct vent field on the eastern flank of NTD1, matching the projected name and the vent-field classification."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the discussion block refers to the young Juan de Fuca plate, supporting both the name and the plate classification."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the maximum-depth block names Knipovich Ridge and the record classifies it only as OTHER."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the block that names the lithosphere-asthenosphere boundary carries both the name and its boundary character."
        },
        {
          "row_index": 27,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the block names the Logachev Seamount, but nothing in that prose makes it a volcano, so the projected feature kind is not carried by the block the derivation reaches."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the study-area block names the Mid-Atlantic Ridge and the record classifies it only as OTHER."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the block names Mayotte Island, supporting both the name and the island classification."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the figure block refers to the expected Moho interface, which supports the name and treating it as a boundary."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the subdivision block names the first non-transform discontinuity and identifies the two offsets as non-transform."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the same block names the second non-transform discontinuity."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the study-area block names the oceanic core complex east of the ridge axis."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the maximum-depth block names the Rainbow massif and the record classifies it only as OTHER."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the subdivision block names the ridge-transform intersection segment as one of the four subsections."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the subdivision block introduces segment RC2 as a ridge segment."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the same block names RC3 as the ridge segment south of the second discontinuity."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the assertion cited concerns the instrument network, but the block it belongs to names the Romanche transform fault, which carries both the projected name and the transform classification as the paper writes it."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the alternative-hypothesis block names the Southwest Indian Ridge and the record classifies it only as OTHER."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the geochemistry block gives the carbon-dioxide to barium ratio and its uncertainty exactly as projected."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the same block gives the carbon-dioxide to rubidium ratio and its uncertainty as projected."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the methods block gives the compressional-to-shear velocity ratio the record projects."
        },
        {
          "row_index": 43,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010"
          ],
          "rationale": "DERIVATION_LOCAL the block the relation derives from reports the earlier authors' suggestion that volatiles carry melt to the boundary, and both endpoint claims are carried, but that block does not itself say the earlier finding supports the authors' own claim; the connective sits in the following block."
        },
        {
          "row_index": 44,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002",
            "page:5:block:003",
            "page:1:block:005",
            "page:7:block:012"
          ],
          "rationale": "DERIVATION_LOCAL the figure block states the interpretation that ties the deep-earthquake depths to degassing-driven volume change, so the relation type holds, but it attaches those depths to the ridge axis generally while the row's source projects segment RC2, whose binding comes from the naming block instead."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL one block states the rival cold-lithosphere explanation and then the morphological evidence against it, so both endpoints and the challenging direction sit where the relation derives."
        },
        {
          "row_index": 46,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:4:block:001",
            "page:2:block:002",
            "page:3:block:003"
          ],
          "rationale": "DERIVATION_LOCAL the block the relation derives from records the absence of detachment-fault evidence at the segment, but the statement that this defeats the shear-zone hypothesis is in the preceding block, and the target claim is attached to the transform rather than to the segment whose earthquakes it explains."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:001",
            "page:4:block:002",
            "page:4:block:003",
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL the block sets the magmatic-tectonic analogues against the absence of any current eruption in the study valley, which is the challenge the relation encodes."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002",
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL the block states the hydrothermal-cooling hypothesis and then the absence of active vents on the segment axis, so the challenging direction is carried where the relation derives."
        },
        {
          "row_index": 49,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002",
            "page:5:block:003",
            "page:5:block:005"
          ],
          "rationale": "DERIVATION_LOCAL both endpoints are carried, but the block the relation's own derivation reaches attributes the enrichment to low-degree melting of an enriched source and does not assert that it supports the degassing hypothesis; that chaining appears in the abstract block the row also reaches."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:6:block:005",
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL the geochemistry block places the sample set inside segment RC2, which is what the sampling relation asserts."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:6:block:005",
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL the same block distinguishes the southern RC3 samples, which is what the second sampling relation asserts."
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:004",
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_NON_LOCAL the block the relation derives from puts the brittle-ductile boundary at about ten kilometres beneath the second discontinuity, which is the relation asserted; neither endpoint is formalised from that block, so the pointer is not local."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL one block carries the relation and both endpoints, stating that the intersection segment is bounded to the east by the westward dipping detachment fault."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002",
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL the block places the extinct vent field on the eastern flank of the first discontinuity, which is the relation asserted."
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002",
            "page:5:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block states the degassing explanation as the authors' preferred fourth possibility for the deep microseismicity at the segment, matching the hypothesised modality and the preferred disposition; the abstract block the same derivation reaches does not name the segment."
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010"
          ],
          "rationale": "SUBJECT_IN_BLOCK the abstract block asserts the influence of high primitive-melt carbon dioxide on melt at the boundary as a forward claim, and the later block that fixes the subject names that boundary."
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block states the cold and thick lithosphere as one explanation and then argues against it, matching the hypothesised modality and the not-supported disposition, and it names the segment."
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002",
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block states the hydrothermal-cooling hypothesis and then the finding that magmatism dominates at the segment, which is the disposition the record carries."
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "SUBJECT_IN_BLOCK one block carries the earlier authors' statement about volatiles flushing melt to the boundary and names that boundary, so subject and content come from the same prose."
        },
        {
          "row_index": 60,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:5:block:001",
            "page:4:block:002",
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the rival magmatic-tectonic explanation and its rejection are both carried, but neither block that supplies them names segment RC2; the subject binding comes only from the naming block, which carries none of the claim."
        },
        {
          "row_index": 61,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:002",
            "page:3:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block carries the shear-zone hypothesis and its rejection, but the hypothesis is offered as an explanation for the segment's deep earthquakes rather than as a claim about the Romanche transform, so the subject shown is not what the block's claim is about."
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the block carrying the claim refers to the fault by description rather than by the projected name, but it plainly concerns the same detachment fault near the core-complex termination and states that it is inactive."
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK the methods block reports measured carbon dioxide close to theoretical solubility and concludes the samples are degassed, and it names the segment."
        },
        {
          "row_index": 64,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:006",
            "page:7:block:007"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the block supports a figure of 276 successfully relocated events, but that count is a property of the earthquake catalogue rather than of the relocation program the row shows as its subject, and the block does not name the program."
        },
        {
          "row_index": 65,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives the 364 well-constrained relocations and names the program, but the count is of events, not a property of the software the row makes the subject."
        },
        {
          "row_index": 66,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block supports the three new focal-mechanism solutions and names the package, yet the count belongs to the solutions obtained rather than to the software the row makes the subject."
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block attributes the sixty-eight percent error-ellipsoid confidence to the location program itself, so the value is a property of the subject shown."
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives twelve hundred degrees as a parameter of the solubility calculation and names the model, so the value belongs to the subject shown."
        },
        {
          "row_index": 69,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives six as a combined total that includes three solutions from earlier work, so the count is neither wholly the named package's output nor a property of it."
        },
        {
          "row_index": 70,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block supports a 360-earthquake validation subset and names the program, but the count describes the dataset rather than the program the row makes the subject."
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block states that five such velocity models were constructed, which is a count of the subject entity itself."
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block ties the roughly sixty kilometre velocity constraint to the refraction profile, so the depth limit is a property of the subject shown; the naming block supplies the subject."
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the abstract block reports deep earthquakes at ten to twenty kilometres along the ridge axis and names the ridge, matching value, unit and subject."
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives the Icelandic depths greater than ten kilometres alongside the volcano the row makes the subject."
        },
        {
          "row_index": 75,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:7:block:009"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the block supports the roughly 2.6 kilometre average depth uncertainty for axial events but does not identify the segment, and the subject binding rests on the naming block, which carries no uncertainty."
        },
        {
          "row_index": 76,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:002",
            "page:3:block:004",
            "page:7:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK the blocks give a horizontal location uncertainty averaging about 2.1 kilometres across the entire relocated catalogue, which covers ridge and transform events alike, so attaching it to the transform alone is narrower than the prose."
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block puts the brittle-ductile boundary at about ten kilometres from the microseismicity beneath the second discontinuity and names the boundary."
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "SUBJECT_IN_BLOCK the figure block ties the boundary to the 750 degree isotherm, matching value, unit and the modelled determination."
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block states that the boundary stays shallower than ten kilometres out to about 1.3 million years of crustal age."
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the introduction block gives the 700 plus or minus 100 degree isotherm criterion and the other block names the boundary."
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block concludes that brittle lithosphere is no thicker than about ten kilometres where the segments meet, and it names the second discontinuity."
        },
        {
          "row_index": 82,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:5:block:003",
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives the eighty to ninety percent exsolution loss as a general property of ascending carbon-dioxide-bearing melt taken from earlier work, not as a quantity determined for the segment the row makes the subject, although that segment is named later in the same block."
        },
        {
          "row_index": 83,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block supports that the trace-element ratios are a good proxy for carbon dioxide, which is a methodological statement rather than an observation about the segment the row shows as subject, and the row projects no quantity of its own."
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives roughly twenty-five kilometres as the saturation depth for the segment's melt and names the segment."
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the same block gives roughly 0.7 gigapascals as the saturation pressure for that melt."
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the same block gives 1250 degrees as the saturation temperature for that melt."
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:006",
            "page:7:block:011"
          ],
          "rationale": "SUBJECT_IN_BLOCK both blocks give the 5.4 plus or minus 0.3 kilometre crustal thickness and one of them ties it to the segment."
        },
        {
          "row_index": 88,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:7:block:012"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the figure block gives ten to nineteen kilometres below sea floor but places them beneath the ridge axis rather than the segment, and the subject binding comes from the naming block, which carries no depths."
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block reports earthquakes of sixteen to nineteen kilometres under the axis of the segment it names, carrying value and subject together."
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK the observations block puts microseismicity of roughly ten to twenty kilometres under the axis of the named segment."
        },
        {
          "row_index": 91,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:009"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the block gives the roughly 2800 parts per million average but attributes it to several equatorial Atlantic segments from earlier work and does not name the ridge entity the row makes the subject."
        },
        {
          "row_index": 92,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:009"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the same block gives the roughly 8799 parts per million upper figure for those earlier-study segments, again without naming the subject shown."
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the block states the expected maximum depth of under ten kilometres for the study ridge's full spreading rate, identifying the ridge by description rather than by name."
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the same block gives the roughly thirty-two millimetre per year full spreading rate the record projects."
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the study-area block gives the sixteen millimetre per year half-spreading rate and names the ridge."
        },
        {
          "row_index": 96,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:008"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the block supports that some deep earthquakes lack energy above five hertz but does not tie those events to the segment, and the subject comes from the naming block."
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block concludes that the earthquakes occur in mantle hotter than eleven hundred degrees at the segment it names."
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives the roughly twenty kilometre boundary depth the rejected cold-lithosphere hypothesis would require, matching the hypothesised modality."
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block puts the melt fraction needed at the boundary's base at about 1.1 percent and names that boundary."
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the same block gives the water content of up to 332 parts per million."
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block concludes that magmatism dominates crustal accretion at the segment it names; the row projects only modality and determination, both of which fit."
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK the results block gives 120 kilometres of ridge axis covered by the network and names the ridge."
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives depths greater than thirty kilometres offshore the island the row makes the subject."
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block states that no active vents are observed on the segment axis, matching the negated modality."
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block states that no earthquakes are seen deeper than twenty kilometres beneath the segment axis."
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK the observations block gives four to ten kilometre earthquakes beneath the southern discontinuity."
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the morphology block gives the roughly thirty-five kilometre length of the first discontinuity."
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the same block gives the roughly thirty-three kilometre ridge offset at the second discontinuity."
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives the under-ten-kilometre observed maximum depth at the second discontinuity."
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the same block gives the under-six-kilometre maximum depth beneath the core complex."
        },
        {
          "row_index": 111,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:5:block:001",
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the block gives shallow microseismicity under ten kilometres, off axis and to the west, but does not name the segment, so the subject rests on the naming block alone."
        },
        {
          "row_index": 112,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the abstract block gives roughly 0.4 to 3.0 weight percent carbon dioxide in the primary melts without naming the segment, and the subject binding comes from the naming block."
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK the geochemistry block gives the barium enrichment above eighty-nine parts per million for the segment's samples."
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the methods block gives 0.7 to 4.6 weight percent pre-eruptive carbon dioxide from barium for the segment."
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK the methods block gives 0.4 to 3.0 weight percent primary-melt carbon dioxide from the barium correction for the segment."
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the results block gives the calculated 0.4 to 3.0 weight percent for the melts formed along that segment."
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the methods block gives 0.9 to 4.3 weight percent pre-eruptive carbon dioxide from rubidium for the segment."
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK the methods block gives 0.5 to 2.8 weight percent primary-melt carbon dioxide from the rubidium correction for the segment."
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block concludes that the deep events under the segment axis are demanded by the data rather than being location artefacts."
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the morphology block gives the segment's roughly twenty-two kilometre length."
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block reports the volcanic axial morphology that indicates the segment is magmatic."
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the morphology block gives the ten kilometre wide median valley of the segment."
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003",
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block finds no evidence of an eruption underway in the axial valley and names the segment."
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block states that the segment shows no evidence of detachment faults."
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block reports normal velocity ratios at the segment from tomography."
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives the estimated 0.7 to 4.6 weight percent pre-eruptive carbon dioxide for the segment."
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK the geochemistry block gives the rubidium enrichment above eight parts per million for the segment's samples."
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the methods block gives 0.06 to 0.8 weight percent pre-eruptive carbon dioxide from barium for the southern segment."
        },
        {
          "row_index": 129,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK the methods block gives 0.04 to 0.5 weight percent primary-melt carbon dioxide from barium for the southern segment."
        },
        {
          "row_index": 130,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the results block gives the calculated 0.04 to 0.7 weight percent for the southern segment."
        },
        {
          "row_index": 131,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the methods block gives 0.07 to 1.0 weight percent pre-eruptive carbon dioxide from rubidium for the southern segment."
        },
        {
          "row_index": 132,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK the methods block gives 0.05 to 0.7 weight percent primary-melt carbon dioxide from rubidium for the southern segment."
        },
        {
          "row_index": 133,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the morphology block gives the southern segment's fifty kilometre length."
        },
        {
          "row_index": 134,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:7:block:010"
          ],
          "rationale": "SUBJECT_IN_BLOCK the depth-resolution block gives the forty-five event subset used to test the deep locations and names the segment."
        },
        {
          "row_index": 135,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK the results block gives the 140 kilometres of transform covered by the network."
        },
        {
          "row_index": 136,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK the observations block gives the zero to six kilometre shallow earthquakes beneath the core-complex dome."
        },
        {
          "row_index": 137,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the study-area block gives the roughly 120 kilometre studied portion of the ridge."
        },
        {
          "row_index": 138,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives the 1.9 weight percent highest reported melt carbon dioxide at the Southwest Indian Ridge."
        },
        {
          "row_index": 139,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives temperatures above twelve hundred degrees below twenty kilometres as the modelled reason no deeper events occur."
        },
        {
          "row_index": 140,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives the modelled eleven hundred to twelve hundred degrees at ten to twenty kilometres beneath the segment axis."
        },
        {
          "row_index": 141,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:004",
            "page:1:block:005",
            "page:7:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives 317 events located along the ridge, matching value and subject."
        },
        {
          "row_index": 142,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:3:block:003",
            "page:7:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK the same block gives 197 events along the transform, matching value and subject."
        },
        {
          "row_index": 143,
          "source_support": "UNSUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:2:block:003",
            "page:6:block:005"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the blocks give 514 as the total located across the whole study region, and the reading splits that total into separate ridge and transform counts, so assigning all 514 to the transform contradicts the prose."
        }
      ]
    },
    {
      "question_id": "CQ-04",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The preferred mechanism is present as a hypothesis and not as a fact: one claim record carries a hypothesised modality together with a preferred disposition, the three rival explanations are each returned with a not-supported disposition, and relation rows connect the observations that challenge them. The epistemic half of the question is therefore answered directly. The mechanism half is only partly answered. The preferred claim's own projected fields describe it generically as an explanation for the deep mantle earthquakes and never name carbon dioxide, degassing or ascending melt; those words are recoverable only by following the derivation into the capture, whereas the rejected rivals do carry their mechanisms in their projected fields. Volume and pressure change appear only in the underlying assertion text, and the extensional-stress condition the mechanism depends on is not represented by any returned row. The same subject-token convention noted for the other question applies here.",
      "source_locators": [
        "page:1:block:001",
        "page:3:block:001",
        "page:5:block:002",
        "page:5:block:003"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the methods block names the five one-dimensional P-wave velocity models the record is named for, which is the only field it projects."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the block the derivation reaches names the CO2 solubility model used to work out saturation conditions, matching the only projected field."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the code-availability block names Global Mapper and gives the structural-analysis use and address that the description projects."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the same availability block names the GMT 6 toolbox, which is all this record projects."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW one block names the package used for focal mechanisms and the other gives its version, use and address, covering both projected fields."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:7:block:006",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW between them the three blocks carry the relocation method, the program, its version and its address, so every projected field sits in the prose."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the methods block attributes the theoretical solubility calculation to the model the record is named after."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the magnitude block states that magnitudes were determined on the local magnitude scale, which is the only projected field."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:7:block:004",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the location algorithm, the program name and the address each appear in one of the blocks the derivations reach."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the results block names the active-source wide-angle refraction profile and its role in choosing the velocity model."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW one block names the package used in detection and the other gives the phase-picking use and address the description projects."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the results block names the trigger algorithm used for automatic detection."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW one block records the VELEST run and the other its inversion use and address."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the magnitude block attributes the completeness and b-value calculation to ZMAP and the availability block gives the use and address."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the figure block lists melt inclusions among the plotted sample sets, matching the projected name and sample kind."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the same figure block lists popping rocks among the plotted sample sets."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:6:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the geochemistry block establishes a sample set from segment RC2 and the figure block classes the plotted rocks as whole-rock MORB, covering both projected fields."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:6:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the same two blocks give the southern RC3 sample set and its whole-rock MORB character."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the alternative-hypothesis block names Askja Volcano, so both the name and the volcano classification sit in the prose."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the introduction block defines the brittle-ductile boundary as a lithospheric boundary fixed by the maximum earthquake depth."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the study-area block names the westward dipping detachment fault that bounds the ridge-transform intersection segment."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the block names Fagradalsfjall Peninsula and the record classifies it only as OTHER, which the prose does not contradict."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the assertion cited is about the Southwest Indian Ridge maximum, but the block it sits in names Gakkel Ridge among the ultraslow-spreading ridges with deep mantle earthquakes, so the projected name is in the block."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the hypothesis block reports an extinct vent field on the eastern flank of NTD1, matching the projected name and the vent-field classification."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the discussion block refers to the young Juan de Fuca plate, supporting both the name and the plate classification."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the maximum-depth block names Knipovich Ridge and the record classifies it only as OTHER."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the block that names the lithosphere-asthenosphere boundary carries both the name and its boundary character."
        },
        {
          "row_index": 27,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the block names the Logachev Seamount, but nothing in that prose makes it a volcano, so the projected feature kind is not carried by the block the derivation reaches."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the study-area block names the Mid-Atlantic Ridge and the record classifies it only as OTHER."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the block names Mayotte Island, supporting both the name and the island classification."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the figure block refers to the expected Moho interface, which supports the name and treating it as a boundary."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the subdivision block names the first non-transform discontinuity and identifies the two offsets as non-transform."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the same block names the second non-transform discontinuity."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the study-area block names the oceanic core complex east of the ridge axis."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the maximum-depth block names the Rainbow massif and the record classifies it only as OTHER."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the subdivision block names the ridge-transform intersection segment as one of the four subsections."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the subdivision block introduces segment RC2 as a ridge segment."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the same block names RC3 as the ridge segment south of the second discontinuity."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the assertion cited concerns the instrument network, but the block it belongs to names the Romanche transform fault, which carries both the projected name and the transform classification as the paper writes it."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW the alternative-hypothesis block names the Southwest Indian Ridge and the record classifies it only as OTHER."
        },
        {
          "row_index": 40,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010"
          ],
          "rationale": "DERIVATION_LOCAL the block the relation derives from reports the earlier authors' suggestion that volatiles carry melt to the boundary, and both endpoint claims are carried, but that block does not itself say the earlier finding supports the authors' own claim; the connective sits in the following block."
        },
        {
          "row_index": 41,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002",
            "page:5:block:003",
            "page:1:block:005",
            "page:7:block:012"
          ],
          "rationale": "DERIVATION_LOCAL the figure block states the interpretation that ties the deep-earthquake depths to degassing-driven volume change, so the relation type holds, but it attaches those depths to the ridge axis generally while the row's source projects segment RC2, whose binding comes from the naming block instead."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL one block states the rival cold-lithosphere explanation and then the morphological evidence against it, so both endpoints and the challenging direction sit where the relation derives."
        },
        {
          "row_index": 43,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:4:block:001",
            "page:2:block:002",
            "page:3:block:003"
          ],
          "rationale": "DERIVATION_LOCAL the block the relation derives from records the absence of detachment-fault evidence at the segment, but the statement that this defeats the shear-zone hypothesis is in the preceding block, and the target claim is attached to the transform rather than to the segment whose earthquakes it explains."
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:001",
            "page:4:block:002",
            "page:4:block:003",
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL the block sets the magmatic-tectonic analogues against the absence of any current eruption in the study valley, which is the challenge the relation encodes."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002",
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL the block states the hydrothermal-cooling hypothesis and then the absence of active vents on the segment axis, so the challenging direction is carried where the relation derives."
        },
        {
          "row_index": 46,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002",
            "page:5:block:003",
            "page:5:block:005"
          ],
          "rationale": "DERIVATION_LOCAL both endpoints are carried, but the block the relation's own derivation reaches attributes the enrichment to low-degree melting of an enriched source and does not assert that it supports the degassing hypothesis; that chaining appears in the abstract block the row also reaches."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:6:block:005",
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL the geochemistry block places the sample set inside segment RC2, which is what the sampling relation asserts."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:6:block:005",
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL the same block distinguishes the southern RC3 samples, which is what the second sampling relation asserts."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:004",
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_NON_LOCAL the block the relation derives from puts the brittle-ductile boundary at about ten kilometres beneath the second discontinuity, which is the relation asserted; neither endpoint is formalised from that block, so the pointer is not local."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL one block carries the relation and both endpoints, stating that the intersection segment is bounded to the east by the westward dipping detachment fault."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002",
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL the block places the extinct vent field on the eastern flank of the first discontinuity, which is the relation asserted."
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002",
            "page:5:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block states the degassing explanation as the authors' preferred fourth possibility for the deep microseismicity at the segment, matching the hypothesised modality and the preferred disposition; the abstract block the same derivation reaches does not name the segment."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010"
          ],
          "rationale": "SUBJECT_IN_BLOCK the abstract block asserts the influence of high primitive-melt carbon dioxide on melt at the boundary as a forward claim, and the later block that fixes the subject names that boundary."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block states the cold and thick lithosphere as one explanation and then argues against it, matching the hypothesised modality and the not-supported disposition, and it names the segment."
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002",
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block states the hydrothermal-cooling hypothesis and then the finding that magmatism dominates at the segment, which is the disposition the record carries."
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "SUBJECT_IN_BLOCK one block carries the earlier authors' statement about volatiles flushing melt to the boundary and names that boundary, so subject and content come from the same prose."
        },
        {
          "row_index": 57,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:5:block:001",
            "page:4:block:002",
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the rival magmatic-tectonic explanation and its rejection are both carried, but neither block that supplies them names segment RC2; the subject binding comes only from the naming block, which carries none of the claim."
        },
        {
          "row_index": 58,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:002",
            "page:3:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block carries the shear-zone hypothesis and its rejection, but the hypothesis is offered as an explanation for the segment's deep earthquakes rather than as a claim about the Romanche transform, so the subject shown is not what the block's claim is about."
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the block carrying the claim refers to the fault by description rather than by the projected name, but it plainly concerns the same detachment fault near the core-complex termination and states that it is inactive."
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK the methods block reports measured carbon dioxide close to theoretical solubility and concludes the samples are degassed, and it names the segment."
        },
        {
          "row_index": 61,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:006",
            "page:7:block:007"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the block supports a figure of 276 successfully relocated events, but that count is a property of the earthquake catalogue rather than of the relocation program the row shows as its subject, and the block does not name the program."
        },
        {
          "row_index": 62,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives the 364 well-constrained relocations and names the program, but the count is of events, not a property of the software the row makes the subject."
        },
        {
          "row_index": 63,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block supports the three new focal-mechanism solutions and names the package, yet the count belongs to the solutions obtained rather than to the software the row makes the subject."
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block attributes the sixty-eight percent error-ellipsoid confidence to the location program itself, so the value is a property of the subject shown."
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives twelve hundred degrees as a parameter of the solubility calculation and names the model, so the value belongs to the subject shown."
        },
        {
          "row_index": 66,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives six as a combined total that includes three solutions from earlier work, so the count is neither wholly the named package's output nor a property of it."
        },
        {
          "row_index": 67,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block supports a 360-earthquake validation subset and names the program, but the count describes the dataset rather than the program the row makes the subject."
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block states that five such velocity models were constructed, which is a count of the subject entity itself."
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block ties the roughly sixty kilometre velocity constraint to the refraction profile, so the depth limit is a property of the subject shown; the naming block supplies the subject."
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the abstract block reports deep earthquakes at ten to twenty kilometres along the ridge axis and names the ridge, matching value, unit and subject."
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives the Icelandic depths greater than ten kilometres alongside the volcano the row makes the subject."
        },
        {
          "row_index": 72,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:7:block:009"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the block supports the roughly 2.6 kilometre average depth uncertainty for axial events but does not identify the segment, and the subject binding rests on the naming block, which carries no uncertainty."
        },
        {
          "row_index": 73,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:002",
            "page:3:block:004",
            "page:7:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK the blocks give a horizontal location uncertainty averaging about 2.1 kilometres across the entire relocated catalogue, which covers ridge and transform events alike, so attaching it to the transform alone is narrower than the prose."
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block puts the brittle-ductile boundary at about ten kilometres from the microseismicity beneath the second discontinuity and names the boundary."
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "SUBJECT_IN_BLOCK the figure block ties the boundary to the 750 degree isotherm, matching value, unit and the modelled determination."
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block states that the boundary stays shallower than ten kilometres out to about 1.3 million years of crustal age."
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the introduction block gives the 700 plus or minus 100 degree isotherm criterion and the other block names the boundary."
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block concludes that brittle lithosphere is no thicker than about ten kilometres where the segments meet, and it names the second discontinuity."
        },
        {
          "row_index": 79,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:5:block:003",
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives the eighty to ninety percent exsolution loss as a general property of ascending carbon-dioxide-bearing melt taken from earlier work, not as a quantity determined for the segment the row makes the subject, although that segment is named later in the same block."
        },
        {
          "row_index": 80,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block supports that the trace-element ratios are a good proxy for carbon dioxide, which is a methodological statement rather than an observation about the segment the row shows as subject, and the row projects no quantity of its own."
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives roughly twenty-five kilometres as the saturation depth for the segment's melt and names the segment."
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the same block gives roughly 0.7 gigapascals as the saturation pressure for that melt."
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the same block gives 1250 degrees as the saturation temperature for that melt."
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:006",
            "page:7:block:011"
          ],
          "rationale": "SUBJECT_IN_BLOCK both blocks give the 5.4 plus or minus 0.3 kilometre crustal thickness and one of them ties it to the segment."
        },
        {
          "row_index": 85,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:7:block:012"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the figure block gives ten to nineteen kilometres below sea floor but places them beneath the ridge axis rather than the segment, and the subject binding comes from the naming block, which carries no depths."
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block reports earthquakes of sixteen to nineteen kilometres under the axis of the segment it names, carrying value and subject together."
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK the observations block puts microseismicity of roughly ten to twenty kilometres under the axis of the named segment."
        },
        {
          "row_index": 88,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:009"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the block gives the roughly 2800 parts per million average but attributes it to several equatorial Atlantic segments from earlier work and does not name the ridge entity the row makes the subject."
        },
        {
          "row_index": 89,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:009"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the same block gives the roughly 8799 parts per million upper figure for those earlier-study segments, again without naming the subject shown."
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the block states the expected maximum depth of under ten kilometres for the study ridge's full spreading rate, identifying the ridge by description rather than by name."
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the same block gives the roughly thirty-two millimetre per year full spreading rate the record projects."
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the study-area block gives the sixteen millimetre per year half-spreading rate and names the ridge."
        },
        {
          "row_index": 93,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:008"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the block supports that some deep earthquakes lack energy above five hertz but does not tie those events to the segment, and the subject comes from the naming block."
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block concludes that the earthquakes occur in mantle hotter than eleven hundred degrees at the segment it names."
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives the roughly twenty kilometre boundary depth the rejected cold-lithosphere hypothesis would require, matching the hypothesised modality."
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block puts the melt fraction needed at the boundary's base at about 1.1 percent and names that boundary."
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the same block gives the water content of up to 332 parts per million."
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block concludes that magmatism dominates crustal accretion at the segment it names; the row projects only modality and determination, both of which fit."
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK the results block gives 120 kilometres of ridge axis covered by the network and names the ridge."
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives depths greater than thirty kilometres offshore the island the row makes the subject."
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block states that no active vents are observed on the segment axis, matching the negated modality."
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block states that no earthquakes are seen deeper than twenty kilometres beneath the segment axis."
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK the observations block gives four to ten kilometre earthquakes beneath the southern discontinuity."
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the morphology block gives the roughly thirty-five kilometre length of the first discontinuity."
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the same block gives the roughly thirty-three kilometre ridge offset at the second discontinuity."
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives the under-ten-kilometre observed maximum depth at the second discontinuity."
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the same block gives the under-six-kilometre maximum depth beneath the core complex."
        },
        {
          "row_index": 108,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:5:block:001",
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the block gives shallow microseismicity under ten kilometres, off axis and to the west, but does not name the segment, so the subject rests on the naming block alone."
        },
        {
          "row_index": 109,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the abstract block gives roughly 0.4 to 3.0 weight percent carbon dioxide in the primary melts without naming the segment, and the subject binding comes from the naming block."
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK the geochemistry block gives the barium enrichment above eighty-nine parts per million for the segment's samples."
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the methods block gives 0.7 to 4.6 weight percent pre-eruptive carbon dioxide from barium for the segment."
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK the methods block gives 0.4 to 3.0 weight percent primary-melt carbon dioxide from the barium correction for the segment."
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the results block gives the calculated 0.4 to 3.0 weight percent for the melts formed along that segment."
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the methods block gives 0.9 to 4.3 weight percent pre-eruptive carbon dioxide from rubidium for the segment."
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK the methods block gives 0.5 to 2.8 weight percent primary-melt carbon dioxide from the rubidium correction for the segment."
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block concludes that the deep events under the segment axis are demanded by the data rather than being location artefacts."
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the morphology block gives the segment's roughly twenty-two kilometre length."
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block reports the volcanic axial morphology that indicates the segment is magmatic."
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the morphology block gives the ten kilometre wide median valley of the segment."
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003",
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block finds no evidence of an eruption underway in the axial valley and names the segment."
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block states that the segment shows no evidence of detachment faults."
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:003"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block reports normal velocity ratios at the segment from tomography."
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives the estimated 0.7 to 4.6 weight percent pre-eruptive carbon dioxide for the segment."
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK the geochemistry block gives the rubidium enrichment above eight parts per million for the segment's samples."
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the methods block gives 0.06 to 0.8 weight percent pre-eruptive carbon dioxide from barium for the southern segment."
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK the methods block gives 0.04 to 0.5 weight percent primary-melt carbon dioxide from barium for the southern segment."
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the results block gives the calculated 0.04 to 0.7 weight percent for the southern segment."
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "SUBJECT_IN_BLOCK the methods block gives 0.07 to 1.0 weight percent pre-eruptive carbon dioxide from rubidium for the southern segment."
        },
        {
          "row_index": 129,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK the methods block gives 0.05 to 0.7 weight percent primary-melt carbon dioxide from rubidium for the southern segment."
        },
        {
          "row_index": 130,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the morphology block gives the southern segment's fifty kilometre length."
        },
        {
          "row_index": 131,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:7:block:010"
          ],
          "rationale": "SUBJECT_IN_BLOCK the depth-resolution block gives the forty-five event subset used to test the deep locations and names the segment."
        },
        {
          "row_index": 132,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "SUBJECT_IN_BLOCK the results block gives the 140 kilometres of transform covered by the network."
        },
        {
          "row_index": 133,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "SUBJECT_IN_BLOCK the observations block gives the zero to six kilometre shallow earthquakes beneath the core-complex dome."
        },
        {
          "row_index": 134,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "SUBJECT_IN_BLOCK the study-area block gives the roughly 120 kilometre studied portion of the ridge."
        },
        {
          "row_index": 135,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives the 1.9 weight percent highest reported melt carbon dioxide at the Southwest Indian Ridge."
        },
        {
          "row_index": 136,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives temperatures above twelve hundred degrees below twenty kilometres as the modelled reason no deeper events occur."
        },
        {
          "row_index": 137,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives the modelled eleven hundred to twelve hundred degrees at ten to twenty kilometres beneath the segment axis."
        },
        {
          "row_index": 138,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:004",
            "page:1:block:005",
            "page:7:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK the block gives 317 events located along the ridge, matching value and subject."
        },
        {
          "row_index": 139,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:3:block:003",
            "page:7:block:007"
          ],
          "rationale": "SUBJECT_IN_BLOCK the same block gives 197 events along the transform, matching value and subject."
        },
        {
          "row_index": 140,
          "source_support": "UNSUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:2:block:003",
            "page:6:block:005"
          ],
          "rationale": "SUBJECT_NOT_IN_BLOCK the blocks give 514 as the total located across the whole study region, and the reading splits that total into separate ridge and transform counts, so assigning all 514 to the transform contradicts the prose."
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
