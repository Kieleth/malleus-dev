# Shop evidence after compiled-view rule checking

Captured from five fresh histories at `a342c72c`, after the seven-line
`ContractView.verifies` repair at `8d315fbd`. The compiler's exact producer
identity changes when its implementation bytes change, even when its compiled
domain facts do not. The old generation remains untouched.

The existing correction, object-event, public-population, showcase and
fresh-import runners produced these bytes. `binding.json` retains their exact
compiler artifacts, producer identity and complete outputs. It also binds all
twenty historical output files from the two preceding generations. This is
test evidence, not a new wire format or an automatically selected producer.

Before capture, a recursive comparison checked identical structure and scalar
types. Every difference was a SHA-256 fingerprint, with the complete differing
paths recorded in the binding. Domain values, records, sources, counts,
operations and time semantics did not change. Both graph outputs are
byte-identical to the preceding generation. The ordinary tests repeat that
check and retain their independent source, graph, correction and trace checks.

The new shipment-rule episode has its own fresh selected-policy history. These
five older episodes are not silently migrated to that policy. No previous
receipt, source, ontology, runner policy, package or downstream evidence is
rewritten. Tests only compare frozen bytes; they never regenerate expectations.
