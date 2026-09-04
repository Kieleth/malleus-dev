# Malleus paper v4 run-02 source-grounded review record

Preliminary inspection by a fresh Claude session, recorded as `CLAUDE_PRELIMINARY`
under the deviation the input manifest declares. `PRELIMINARY_COMPLETE` is not
paper evidence; Luis must ratify. The whole `ratification` block is left pending.

Each row was traced from its witness through the query trace summary, by record
id, to the derivation locators, and from those locators to reading blocks in the
retained capture. Every witness resolved. Where a row's claim rests on a block
the derivation does not reach, the rationale says so and the row is judged on the
reading alone. Reasons are in the reviewer's own words; no source passage is
copied and no aggregate is recorded.

```json
{
  "schema": "malleus.paper-v4.source-grounded-review/v2",
  "status": "PRELIMINARY_COMPLETE",
  "inputs": {
    "review_protocol_sha256": "sha256:7cee52a7d6ea5018fe8443e621c72280b05c2bb5cc1e4a2eeaa27208665ed379",
    "review_input_manifest_sha256": "sha256:785d05f031bd3954cccb14895cd31b84a9f0d03e470a5bb8ab1ee906e57110a5"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-preliminary-run-02",
    "completed_at": "2026-09-04T19:45:00Z"
  },
  "questions": [
    {
      "question_id": "CQ-01",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "One row carries the observing network, its instrument count and the campaign that acquired the microseismicity data, which is every part the question asks for, and the reading supports all three. The count is the number of instruments deployed, which is what was asked, rather than the smaller number that yielded usable arrivals. The other three rows add a funder and two cruise participants; they are outside the question but do not obscure the answer.",
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
          "rationale": "The results text says the microseismicity data were acquired by a nineteen-instrument ocean-bottom seismometer network during the named cruise, and the methods text repeats that nineteen such instruments were deployed. Network identity, instrument count, the deployment scope and the link to the campaign are all covered."
        },
        {
          "row_index": 1,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:10:block:044"
          ],
          "rationale": "The acknowledgement does name the fleet as a funding route for the cruise, but only for its ship time. The row states an unqualified funding relation to the whole campaign and types the fleet as research infrastructure; the narrower scope the prose gives is not carried, and the agent type is read off the name rather than stated."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:023",
            "page:10:block:046",
            "page:1:block:001"
          ],
          "rationale": "The reference entry carries this person's name in the surname-initial form the row uses and attaches it to the cruise, the contributions paragraph lists their initials among the people who collected data during that cruise, and the byline resolves the initials to the full name. Person, campaign and participation all hold."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:10:block:046"
          ],
          "rationale": "The byline carries this person's name as the row records it, and the contributions paragraph puts their initials among those who took part in the data collection during the cruise. The participation relation and both endpoints are covered."
        }
      ]
    },
    {
      "question_id": "CQ-02",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The named subsection is answered: two rows attach deep-earthquake depth observations to the segment the reading names, and the reading supports both. The second half of the question is weaker. The position of the events relative to the ridge axis survives only inside the free-text label of the observation, never as a returned relation, so a reader must parse a property string to recover it. The rest of the returned set is dominated by segment lengths, ridge offsets, seafloor structures and a massif on an unrelated ridge, with nothing marking which rows bear on the question, and several rows attach earthquakes to other subsections at the same level.",
      "source_locators": [
        "page:2:block:004",
        "page:1:block:005",
        "page:2:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004",
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "The key-observations paragraph places the deep microseismicity between ten and twenty kilometres beneath the axis of the named segment, the introduction names that segment among the four subsections of the studied ridge, and the morphology paragraph gives it a magmatic character. The row keeps the endpoints of the range but drops the approximation marker the prose puts on it."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:1:block:005"
          ],
          "rationale": "The results state that a body of earthquakes was located around the named ridge-transform intersection, and the introduction names that intersection as the setting of the study area. The subject of the quantity and its attachment to that region hold; the projection carries no value for the count, so nothing further in the row is open to checking."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "The introduction gives the ridge segment between the two named transform faults a length of about two hundred kilometres. The row keeps that figure and its unit, dropping only the approximation marker."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "The discussion states that no earthquakes appear deeper than twenty kilometres beneath the axis of that segment. The negated modality, the depth bound and the unit all match the prose."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004",
            "page:1:block:005"
          ],
          "rationale": "The key-observations paragraph puts earthquakes of ordinary depth, four to ten kilometres, beneath the southern part of the second non-transform discontinuity, and the introduction names that discontinuity. Depths, unit and subject hold."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:1:block:005"
          ],
          "rationale": "The morphology paragraph gives the first non-transform discontinuity a length of about thirty-five kilometres and calls its origin both magmatic and tectonic, and the introduction names it. The length, unit and character in the row follow the prose."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "The discussion states that microseismicity reaching ten kilometres beneath that discontinuity shows the brittle-ductile boundary sits at about that depth. The quantity, its subject and its unit match."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "The results state that earthquakes beneath that discontinuity reach down to about ten kilometres. The upper bound and the unit match, and no lower bound is claimed."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "The same paragraph gives the depth range beneath that discontinuity as under ten kilometres. The row records only an upper bound, which is what the prose supplies; it restates the same fact as the preceding row from the same block."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "The morphology paragraph gives that discontinuity a ridge offset of about thirty-three kilometres. Value, unit and subject match, with the approximation marker dropped."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "The results state that earthquakes between sixteen and nineteen kilometres deep were observed beneath the axis of the named segment. The bounds, the unit and the measured status all follow the prose."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "The discussion concludes that these earthquakes occur in mantle hotter than eleven hundred degrees. The row turns the strict inequality into a lower bound with no upper bound, which preserves the claim; subject and unit match."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "The morphology paragraph gives the segment a length of about twenty-two kilometres. Value, unit and subject match."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "The discussion attributes a temperature of eleven hundred to twelve hundred degrees at ten to twenty kilometres depth to thermal modelling. The bounds, the unit, the calculated modality and the modelled determination all follow the prose."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "The morphology paragraph gives the southern segment a length of fifty kilometres and calls it magmatic. Value, unit, subject and character match."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004",
            "page:1:block:005"
          ],
          "rationale": "The key-observations paragraph puts most shallow earthquakes, zero to six kilometres, on the outside corner of the intersection, and the introduction identifies the intersection segment by the name the row's target carries and calls it amagmatic. Depths, unit, subject and character all hold."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:006",
            "page:1:block:005"
          ],
          "rationale": "The figure caption attributes the corrugated surface to the core complex in the intersection area, and the introduction places that core complex at the intersection segment, so the structure, its kind and its host all hold. The block the derivation reaches carries only the bare legend word, without the attribution; the support comes from the caption block instead."
        },
        {
          "row_index": 17,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "The morphology paragraph does say the first non-transform discontinuity is characterised by many faults with the stated strikes, so the structure and its host hold. It does not call them normal faults, and no other block does; the row's fault kind is a narrowing the prose does not make, although the same paragraph does use that kind for other structures."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "The discussion reports an extinct hydrothermal vent field on the eastern flank of that discontinuity. Structure, kind, location wording and host all follow the prose."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "The morphology paragraph says large areas of the second non-transform discontinuity are affected by a complex pattern of normal faults. Structure, kind and host all hold."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:1:block:005"
          ],
          "rationale": "The morphology paragraph says the surface of the core complex is heavily cut by normal faults, and the introduction places that core complex at the intersection segment. Structure, kind and host all hold."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005",
            "page:1:block:005"
          ],
          "rationale": "The results name the termination of the core complex and treat the associated structure as a detachment fault in the same sentence, and the introduction places the core complex and its detachment fault at the intersection segment. Structure, kind and host all hold."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "The introduction places a prominent oceanic core complex on the eastern side of the axis at the intersection segment. Structure, kind and host all follow directly."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "The methods paragraph on maximum earthquake depths says this massif sits at a non-transform discontinuity. Structure, kind and the discontinuity it is hosted by all hold, though the prose introduces it only as a comparison point in a compilation, not as part of the study area."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "The introduction says the intersection segment is bounded on its east by a westward dipping detachment fault. Structure, kind, dip direction and host all follow the prose."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "The discussion cites hummocky volcanic axial morphology on the named segment as evidence of its magmatic origin. Structure, kind and host all hold."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "The morphology paragraph gives the segment a median valley about ten kilometres wide. Structure, kind and host all hold."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "The morphology paragraph gives the segment a neo-volcanic ridge with the stated orientation. Structure, kind and host all hold."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "The discussion lists volcanic cones in the axial valley of the segment among the signs of its magmatic origin. Structure, kind and host all hold."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:004"
          ],
          "rationale": "The discussion states that microseismicity reaching ten kilometres beneath that discontinuity shows the brittle-ductile boundary lies there, which places the horizon beneath the named subsection. The introduction is where the abbreviation in the horizon's recorded name is defined; the abstract block the derivation reaches uses the unabbreviated term."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:3:block:001",
            "page:7:block:011"
          ],
          "rationale": "The results discuss the depth of the brittle-ductile boundary beneath this part of the ridge, the discussion argues about how deep it lies under the named segment, and the schematic caption places it under the illustrated segments. The horizon and its position beneath that subsection hold."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "The schematic caption states the crustal thickness beneath the named segment and marks the expected crust-mantle interface there. The horizon, its kind and its position beneath that subsection all hold."
        }
      ]
    },
    {
      "question_id": "CQ-03",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "Both requested quantities are present with their units and their observed or calculated status: the earthquake depth range in kilometres with a measured modality, and primary-melt carbon dioxide in weight per cent with a calculated modality and a derived or estimated determination. What is missing is the pairing. No returned relation ties a depth range to a carbon dioxide range, and several competing primary-melt ranges for the studied segment come back side by side, from the abstract, from the two trace-element proxies and as a minimum bound, with nothing distinguishing which the question's central association refers to. Southern-segment values, pre-eruptive values and unrelated lengths and temperatures are returned at the same level.",
      "source_locators": [
        "page:2:block:004",
        "page:8:block:007",
        "page:1:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004",
            "page:1:block:005"
          ],
          "rationale": "The key-observations paragraph places the deep microseismicity between ten and twenty kilometres beneath the axis of the named segment, and the introduction names that segment. Bounds, unit, measured status and subject hold; the row drops the approximation marker the prose puts on the range."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:1:block:005"
          ],
          "rationale": "The results state that a body of earthquakes was located around the named ridge-transform intersection, and the introduction names that intersection. The subject of the quantity and its attachment hold; the projection carries no value, so there is nothing further to check."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "The introduction gives the ridge segment between the two named transform faults a length of about two hundred kilometres, which is the value and unit the row records."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "The discussion states that no earthquakes appear below twenty kilometres beneath that segment's axis. Negated modality, bound, unit and subject all match."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004",
            "page:1:block:005"
          ],
          "rationale": "The key-observations paragraph puts earthquakes of ordinary depth, four to ten kilometres, beneath the southern part of the second non-transform discontinuity, which the introduction names. Depths, unit and subject hold."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:1:block:005"
          ],
          "rationale": "The morphology paragraph gives the first non-transform discontinuity a length of about thirty-five kilometres, and the introduction names it. Value, unit and subject hold."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "The discussion states that microseismicity reaching ten kilometres beneath that discontinuity puts the brittle-ductile boundary at about that depth. Quantity, subject and unit match."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "The results state that earthquakes beneath that discontinuity reach down to about ten kilometres. The upper bound and unit match and no lower bound is claimed."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "The same paragraph gives the depth range beneath that discontinuity as under ten kilometres, which is the single upper bound the row records. It restates the preceding row's fact from the same block."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "The morphology paragraph gives that discontinuity a ridge offset of about thirty-three kilometres. Value, unit and subject match."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "The results state that earthquakes sixteen to nineteen kilometres deep were observed beneath the axis of the named segment. Bounds, unit and measured status follow the prose."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "The discussion concludes these earthquakes occur in mantle above eleven hundred degrees. The row records that as a lower bound with no upper bound, which preserves the claim; subject and unit match."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "The morphology paragraph gives the segment a length of about twenty-two kilometres, matching the row's value, unit and subject."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "The discussion attributes eleven hundred to twelve hundred degrees at ten to twenty kilometres depth to thermal modelling. Bounds, unit, calculated modality and modelled determination all follow."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "The morphology paragraph gives the southern segment a length of fifty kilometres. Value, unit and subject match."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004",
            "page:1:block:005"
          ],
          "rationale": "The key-observations paragraph puts most shallow earthquakes, zero to six kilometres, on the outside corner of the intersection, and the introduction identifies the intersection segment under the name the target carries. Depths, unit and subject hold."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:8:block:007",
            "page:5:block:005"
          ],
          "rationale": "The abstract reports an abnormally high carbon dioxide content of roughly zero point four to three weight per cent in the primary melts, and the methods and results tie exactly that range to the primary melts of the studied segment. Value, unit and calculated status hold. The abstract block the derivation reaches does not itself name the segment; that attribution comes from the other two blocks."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "The discussion reports a melt fraction of about one point one per cent required at the base of the lithosphere-asthenosphere boundary. Value, unit, subject and modelled status hold. The prose credits the figure to a cited study rather than to this work, which the row does not record."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "The methods give the barium-based estimate for primary melts of the studied segment as zero point four to three weight per cent. Bounds, unit, subject, melt stage and calculated status all match."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "The methods give the barium-based pre-eruptive estimate for the studied segment as zero point seven to four point six weight per cent. Bounds, unit, subject and melt stage all match."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005",
            "page:8:block:007",
            "page:5:block:004"
          ],
          "rationale": "The results give the calculated carbon dioxide content of melts generated along the studied segment as zero point four to three weight per cent. The identification of those melts as the primary, mantle-source-equilibrium melts comes from the neighbouring results paragraph and the methods, not from the block the derivation reaches."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "The methods conclude that the primary-melt carbon dioxide concentration along the studied segment is at least zero point four weight per cent. The row's single lower bound, unit and subject match."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "The results give estimated pre-eruptive concentrations of zero point seven to four point six weight per cent for the studied segment. Bounds, unit, subject, melt stage and estimated determination all match."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "The methods give the rubidium-based primary-melt estimate for the studied segment as zero point five to two point eight weight per cent. Bounds, unit, subject and melt stage match."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "The methods give the rubidium-based pre-eruptive estimate for the studied segment as zero point nine to four point three weight per cent. Bounds, unit, subject and melt stage match."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "The methods give the barium-based primary-melt estimate for the southern segment as zero point zero four to zero point five weight per cent. Bounds, unit, subject and melt stage match."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "The methods give the barium-based pre-eruptive estimate for the southern segment as zero point zero six to zero point eight weight per cent. Bounds, unit, subject and melt stage match."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005",
            "page:8:block:007"
          ],
          "rationale": "The results give the calculated content for melts generated along the southern segment as zero point zero four to zero point seven weight per cent. As with the corresponding row for the studied segment, the identification of those melts as primary comes from the methods rather than from the block the derivation reaches."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "The methods give the rubidium-based primary-melt estimate for the southern segment as zero point zero five to zero point seven weight per cent. Bounds, unit, subject and melt stage match."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "The methods give the rubidium-based pre-eruptive estimate for the southern segment as zero point zero seven to one weight per cent. Bounds, unit, subject and melt stage match."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:002",
            "page:5:block:003"
          ],
          "rationale": "The discussion puts ascending melt beneath the named segment and ties its degassing to the earthquakes recorded under that segment's axis. The melt population, its ascending stage and its position beneath the subsection all hold."
        },
        {
          "row_index": 31,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:5:block:005",
            "page:8:block:007"
          ],
          "rationale": "The prose supports the existence of primary melts belonging to the named segment and their equilibrium with the mantle source, so the melt population and its stage hold. It says those melts were generated along the segment; it does not state that they lie beneath it, which is what the row's spatial relation asserts."
        },
        {
          "row_index": 32,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "The methods support pre-eruptive melts for the southern segment and their distinction from primary melts, so the population and its stage hold. No block states that this population lies beneath that segment, which is the relation the row asserts."
        },
        {
          "row_index": 33,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:5:block:005",
            "page:8:block:007"
          ],
          "rationale": "The results and methods support primary melts belonging to the southern segment, so the population and its stage hold. The prose has them generated along the segment rather than beneath it, so the row's spatial relation goes past what the reading states."
        }
      ]
    },
    {
      "question_id": "CQ-04",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The preferred mechanism comes back explicitly as a hypothesis: two rows carry the degassing account with a hypothesised modality and a preferred appraisal, one row carries the volume change, the extensional stresses and the triggering of deep mantle earthquakes, and a rejected rival is returned with an unsupported appraisal, which sharpens the contrast. The ascending melt the question's required semantics ask for does not appear in any returned row; the hypothesis statement returned is the abstract's short form, which omits it, and no row connects the hypothesis to a melt population.",
      "source_locators": [
        "page:5:block:002",
        "page:5:block:003",
        "page:1:block:001"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002",
            "page:4:block:003",
            "page:5:block:001"
          ],
          "rationale": "The discussion sets out the magmatic-tectonic possibility in the terms the target statement records, the following paragraph objects that the Icelandic and Mayotte settings differ from a mid-ocean ridge, and the next page rejects the melt-movement mechanism outright. The hypothesis, its hypothesised modality, its unsupported appraisal and the challenging relation all hold."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003",
            "page:5:block:002",
            "page:1:block:001"
          ],
          "rationale": "The discussion states the volume change from degassing, the extensional stresses, the resulting high strain rates and the triggering of deep mantle earthquakes, and names the degassing account as the authors' preferred possibility; the abstract carries the hypothesis statement in the recorded form. The claim, the hypothesis, both epistemic markers and the supporting relation all hold."
        },
        {
          "row_index": 2,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:8:block:001",
            "page:5:block:002"
          ],
          "rationale": "The methods do state, in the recorded words and with the recorded modality, that the deep events beneath the segment axis are well constrained and not artefacts, and the discussion marks the degassing account as preferred, so both endpoints hold. The reading does not connect that robustness conclusion to the degassing hypothesis; the supporting relation is an inference the prose does not make."
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
  "rationale": "one or two sentences in your own words"
}
```
