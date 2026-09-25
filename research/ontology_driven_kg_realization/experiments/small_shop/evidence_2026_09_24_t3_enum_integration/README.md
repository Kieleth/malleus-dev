# Shop evidence after the T3 and ADD_ENUM integration

Captured from five fresh histories on branch `core/t3-enum-integration`, which
lands the temporal T3 cut under route C with route D together with the
`ADD_ENUM` revision candidate (`design/temporal/g4/RULINGS.md` R-07).

## What moved, and what did not

Two of the five scenarios moved. Every changed leaf is a sha256 value; no
count, record, source, graph or field name changed, and `binding.json` declares
no `changed_values` or `changed_keys`.

| scenario | changed leaves | why |
|---|---|---|
| public population | 46 | the five plans name the successor state-version profile (route D), and the contract revision identity moves with the `ADD_ENUM` successor revision policy it now names |
| fresh import | 3 | `ledger_head`, `ledger_sha256`, `receipt_identity`: the contract revision names the `ADD_ENUM` successor revision policy |
| object event, correction, showcase | 0 | byte-identical to the preceding generation |

`public_population/evidence.json` carries the same `graph` object and the same
`graph_state_digest` as the preceding generation. The Shop histories use their
own policies, which name the research structural check at builtin version 1, so
route C (the shipped structural default moving to version 2) moves none of
these five.

The identities behind the move: state-version profile
`sha256:b18f3129…` to `sha256:5f6bd9eb…`; contract revision policy
`sha256:e129b6e8…` to `sha256:a2580f91…`.

## The connected story

`connected_story_chain` records the connected story's re-cut: 30 values across
8 files, each a ledger digest, head, replay receipt, partial contract identity
or a report digest embedding one. The connected story's Table 1 baseline is a
structural history, so route C moved it from the first stage. The re-cut ran
the stages' own producers (`run_story`, `read_timelines`, `explain_shipments`,
`append_warehouse`, `receipt`, `read_ordering`, the partial-shipments `start`,
`prepare`, `admit` and `receipt`) and replaced only the values that moved.
`run_receipt.json` `contract_facts` did not move and was not changed.

Measured against a `git archive` of `ebff70f7`: the exported graph and the
complete record history are equal at all three stages, and so are the timeline
and shipment-explanation reports except for their history coordinates. The three
graph state digests are unchanged: `sha256:4a890bb0…`, `sha256:e5f36981…` and
`sha256:57e3839c…`.

## What this generation pins

`binding.json` retains the exact compiler artifacts and producer commit of all
five scenarios, the complete outputs, and all fifty output files from the five
preceding generations, which remain untouched.
