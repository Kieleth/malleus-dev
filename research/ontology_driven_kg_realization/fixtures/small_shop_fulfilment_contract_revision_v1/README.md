# Small Shop additive contract revision fixture

This conformance fixture proves that one Small Shop knowledge history can cross
one recorded ontology revision and still replay from its ledger alone.

The original contract is the frozen
`small_shop_fulfilment/input/tbox/small-shop.yaml`. The target contract in this
directory keeps the same ontology identity and imports, then adds only the
`SupplierOrderState` class and its three new slots. Those additions are the
smallest vocabulary needed by the existing e4 and e7 supplier-order source
rows.

The integration test first admits the existing O1, X1, and
`OrderContainsUnit` records under the original contract. It records the
compiler-derived additive revision, admits B/e4 and B/e7 under the target
contract, closes the history, reopens it, and verifies both the preserved
records and the e4-to-e7 supersession.

This is a Core conformance fixture. It does not claim that version 0.2.0 was a
historical Small Shop release, select a general ontology-migration policy, or
make the Small Shop vocabulary part of the Malleus protocol.
