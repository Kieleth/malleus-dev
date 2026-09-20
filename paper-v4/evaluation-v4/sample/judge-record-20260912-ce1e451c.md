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
  "sample_sha256": "sha256:ce1e451cc0c8059e25207ab2c3a4ac661a98eddc55761158274002da89fec518",
  "judge": {
    "evaluator_kind": "INDEPENDENT_MODEL_JUDGE",
    "model_id": "claude-fable-5-1",
    "actor_id": "actor:fable-judge-20260912-ce1e451c",
    "reasoning_effort": "harness default, not pinned or observed"
  },
  "judgements": [
    {
      "cell": "run-23",
      "witness_key": "claim:acknowledgement-discussions",
      "source_support": "PARTIAL",
      "rationale": "The block shows the authors thanking named people, so the thanks-to-colleagues part holds, but it ends before saying what they are thanked for, so the useful-discussions purpose has no support here."
    },
    {
      "cell": "run-23",
      "witness_key": "claim:fixed-depth-rms-worse",
      "source_support": "PARTIAL",
      "rationale": "The slower decrease and the higher final residuals relative to the free-depth case are in the block, but the block opens mid-sentence, so the opening claim that the initial residuals were much higher under fixed depths is not itself present."
    },
    {
      "cell": "run-23",
      "witness_key": "claim:max-depth-not-following-relationship",
      "source_support": "PARTIAL",
      "rationale": "The negation and the MAR subject are in the block (the caption expands the abbreviation), and the link to BDB depth versus spreading is stated, but the sentence is cut by the intruding caption before the rate-observed-elsewhere tail, which therefore lacks support."
    },
    {
      "cell": "run-23",
      "witness_key": "claim:occ-exhumed-mantle",
      "source_support": "PARTIAL",
      "rationale": "The exhumed-mantle inference and the tectonic-origin conclusion open the block, but the block begins mid-sentence with its subject missing, so the claim that peridotite observation is the evidence is not supported by this fragment."
    },
    {
      "cell": "run-23",
      "witness_key": "claim:volatiles-reduce-solidus",
      "source_support": "PARTIAL",
      "rationale": "The consequence clause (lower solidus of dry peridotite, melt below its solidus at the LAB) is in the block, but the block starts mid-sentence so volatiles as the agent lowering the solidus is not stated; later text ties melt at the LAB to CO2 and water without the solidus mechanism, and the LAB abbreviation is never spelled out as the subject name has it."
    },
    {
      "cell": "run-23",
      "witness_key": "obs:depth-uncertainty-bound",
      "source_support": "PARTIAL",
      "rationale": "A 10 km inclusive ceiling in kilometres is present, but the block starts mid-list and never names the quantity it caps; that it is depth uncertainty of the located events is not stated in the block itself."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:askja",
      "source_support": "PARTIAL",
      "rationale": "Askja is named as a volcano in Iceland where magmatic-tectonic deep seismicity was seen, under a possibility the authors raise, so the name and hypothesised framing hold; nothing in the block describes it as a cone, so the structure kind is not supported."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:fagradalsfjall",
      "source_support": "PARTIAL",
      "rationale": "The block names Fagradalsfjall as a peninsula in Iceland with deep magmatic-tectonic earthquakes, supporting the name and the hypothesised framing; it says nothing that would make it a volcanic cone."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:mayotte",
      "source_support": "PARTIAL",
      "rationale": "Mayotte Island is named, with deep events offshore, so the name is supported; the block calls it an island and gives no basis for typing it as a seamount."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:ntd1-faults",
      "source_support": "PARTIAL",
      "rationale": "The two strike directions for the NTD1 faults are stated exactly as recorded; the block calls them faults only, reserving the word normal for the OCC and NTD2 faults, so the normal-fault typing is not supported for these."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:occ-termination",
      "source_support": "PARTIAL",
      "rationale": "The OCC termination is named in the block, placed in the axial valley and tied to an inactive detachment; there is no mention of corrugations, so the corrugated-surface typing is unsupported."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:expected-max-depth",
      "source_support": "SUPPORTED",
      "rationale": "The block states that for the local spreading rate prior microseismicity work implies a maximum earthquake depth under 10 km, which matches the quantity, the strict upper bound, the unit and the expected rather than observed character of the value."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:mar-events",
      "source_support": "SUPPORTED",
      "rationale": "The Fig. 2 panel text puts a total of 317 events directly under the MAR label, and the caption frames the figure as seismicity along the ridge study region, matching the count and its scope."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:q:romanche-events",
      "source_support": "SUPPORTED",
      "rationale": "The panel text gives a total of 197 events under the TF label alongside depth-versus-distance axes and the Romanche transform legend, matching the count and the profile scope."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:rainbow",
      "source_support": "PARTIAL",
      "rationale": "The Rainbow massif is named and placed at a non-transform discontinuity, so the name holds; the paragraph lists core complexes only as a category of compiled information and never calls Rainbow one, so the OCC typing lacks support."
    },
    {
      "cell": "run-24",
      "witness_key": "entity:rc2-bounding-faults",
      "source_support": "PARTIAL",
      "rationale": "Orientation, high angle and inward dip of the faults bounding RC2 are all stated, so the name and geometry fields hold; the block calls them faults without a slip sense, so the normal-fault typing is inferred rather than stated."
    },
    {
      "cell": "run-24",
      "witness_key": "event:romanche-2016",
      "source_support": "PARTIAL",
      "rationale": "The caption names a 2016 Mw 7.1 Romanche earthquake, supporting the name, type, scale and magnitude; it gives only the year, so the recorded 1 January midnight timestamp carries a precision the block does not provide."
    },
    {
      "cell": "run-25",
      "witness_key": "agent:geli",
      "source_support": "PARTIAL",
      "rationale": "A person surnamed Geli appears among those thanked for discussions, which supports the person type and surname; the initial L. is not in this block."
    },
    {
      "cell": "run-25",
      "witness_key": "obs:depth-uncertainty-cap",
      "source_support": "PARTIAL",
      "rationale": "The 10 km upper limit and unit are there, but the block begins with the value and no noun, so the identification of the capped quantity as depth uncertainty of the located earthquakes is not in the cited text."
    },
    {
      "cell": "run-25",
      "witness_key": "obs:fig3e-elevation-scale",
      "source_support": "SUPPORTED",
      "rationale": "The panel text for the NTD2 map (panel e) carries an elevation legend in metres with endpoints at minus 6000 and minus 3000, matching the range, unit and map association recorded."
    },
    {
      "cell": "run-25",
      "witness_key": "sample:basalt",
      "source_support": "PARTIAL",
      "rationale": "Basalt appears as a legend entry in the Fig. 2 map text, supporting the name and material; the block does not say these are rock samples or that they are drawn as coloured hexagons."
    },
    {
      "cell": "run-25",
      "witness_key": "sample:peridotite",
      "source_support": "PARTIAL",
      "rationale": "Peridotite is listed in the map legend of the block, which supports the name and material; nothing in the block describes the symbol as coloured hexagons or labels the entries as rock samples."
    }
  ]
}
```
