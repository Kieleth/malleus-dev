# Small Shop object-event fixture

This versioned fixture exercises the shipped `object-event` history profile on
the controlled Small Shop source row for packing event `e27`.

The source states that actor `R4` packed order `O1` with items `X1`, `X2`, and
`Y1`. The fixture therefore proposes one Event, five enduring Entities, and five
qualified Event-to-Entity participation records. Its expected result is kept in
an independently hand-authored fixture oracle and is never compiler input.

This proves governed Event population, qualified participation, one-ledger
admission, reopen, replay, and query for this bounded occurrence. It does not
claim Event-to-Event ordering, derive product codes absent from the source row,
select a universal event-log vocabulary, or make this Small Shop ontology part
of the Malleus protocol.
