# Shop evidence after the revision policy declared a fifth change kind

Captured from five fresh histories at `5cc211a6`, with the correction,
object-event, public-population, showcase and fresh-import runners unchanged.
The revision policy declared a fifth change kind, `REBIND_CHECK_CONTRACT`, at
`bb3dd754`, so its content address moved, and every recompiled revision binds
the new one.

The revision policy identity before and after that commit:

    sha256:05b6880517ae8287333973e421248e2eb803c2f50569adcea26ca114d154ce8e
    sha256:e129b6e87bd06abc8d23b22bdefee2142c07574237b273a068040fc14d09db59

A compiled revision records `policy_identity`, the policy it was compiled
under, which is how a recorded revision resolves back to an executable policy
on replay. The first field that moved is therefore
`/contract_revision/revision_identity` in `public_population/evidence.json`:

    sha256:8c05740fc38088b38241c2af4588848c465e39f42304e3c62d44e49581c32ef4
    sha256:7a85748a0d9ca11ac317c4082f9cc96e2dc8ee5313837f69df9bf56e02aa9203

Nothing else inside that record moved. Substituting the superseded policy
identity back into the produced revision bytes reproduces the frozen identity
exactly. The ledger head, ledger digest, acceptance head, materialization head
and receipt identity follow from it, here and in `fresh_import`, which admits
onto the same history.

Only the two scenarios that record a contract revision changed. Correction,
object-event and showcase regenerate byte-identical to the preceding
generation, and the validated compiler artifacts and their producer are
unchanged in all five, so the compiler's implementation bytes did not move.
The Shop revision declares no re-binding and carries no `check_rebinding`
field at all. The policy digest moved because the policy is content-addressed
over its declared change kinds, not because this fixture used the new
capability.

`binding.json` retains the exact compiler artifacts, producer identity and
complete outputs, and pins all thirty output files from the three preceding
generations, which remain untouched. The recorded `changed_paths` describe this
transition only: six SHA-256 fingerprints in public population, three in fresh
import, none elsewhere. No domain value, record, source, count, operation or
time coordinate changed. This is test evidence, not a new wire format or an
automatically selected producer. Tests only compare frozen bytes; they never
regenerate expectations.

## The connected-story chain

The same moved policy digest moved a second family of frozen coordinates. The
warehouse history records the revision as its first appended event, sequence
122 of 193, so 72 events differ from there by the hash chain and the warehouse
history digest moved:

    sha256:ae9bbf870fd928e96de9f62c54a43d05575929b2546bb1e4376ecc9b8191cc06
    sha256:32798a67f4b2d5b6fab2de102ae6c4b41087f04ae794547517497232256ac333

Its length is unchanged at 1,646,996 bytes. The connected-story history that
precedes the warehouse append is unchanged too, 121 events and
`sha256:1c989c55…`, so `run_receipt.json`, `timeline_receipt.json`,
`shipment_explanation_receipt.json` and `warehouse/source_boundary.json` still
hold. Four files carried the moved values and were re-frozen at `5cc211a6`:
`connected_story/partial_shipments/input_boundary.json`,
`connected_story/warehouse/receipt.json`,
`connected_story/warehouse/ordering_receipt.json` and
`connected_story/partial_shipments/receipt.json`. Twelve values in total, every
one a ledger head, ledger digest, replay receipt or a report digest that embeds
one. `binding.json` records each superseded and current pair under
`connected_story_chain`, because those files carry only the current value and
the boundary declares the one exact prefix it accepts.

Before the re-freeze, `partial_shipments/run.py` refused the chain at its input
check with `Synthetic extension requires the exact warehouse history`. The
Appendix B digests and the exhibits in `paper-v4` that compare against a fresh
chain are the paper front's and are not re-cut here.
