# What the first connected source pack contains

Scope: all 21 rows of the retained Table 1 image plus four named context
excerpts. No other chapter view is silently merged into this denominator.
The source inventory counts 123 populated fields. Every field has a retained
locator and a planned disposition. This is source accounting, not semantic
completeness. Human source ratification is pending.

| Source row | What is present | Representation to build |
|---|---|---|
| e1 | O1, requested 2 X and 1 Y, R1 | Order, requested quantities, creation occurrence |
| e2 | O2, requested 1 X and 1 Y, R1 | Second order and its own quantities/occurrence |
| e3 | Supplier order A, 3 X, R1 | Supplier-order identity and initial state |
| e4 | Supplier order B, 1 Y, R3 | Identity, state and occurrence, covered by the probe |
| e5 | O2, I2, R3 | Invoice identity, order association, creation occurrence |
| e6 | A, X1/X2/X3, R2 | Receipt occurrence and distinct units; date stays unresolved |
| e7 | O2, B, 2 Y, R1 | Update occurrence and explicit B state replacement; probe covers B only |
| e8 | A, X3, R2 | Unpacking occurrence; date stays unresolved |
| e9 | I2, R2 | Invoice-update occurrence; unknown new value remains a gap |
| e10 | A, X1, R2 | Unpacking occurrence |
| e11 | A, X2, R2 | Unpacking occurrence |
| e18 | O1, I1, R3 | Invoice identity, order association, creation occurrence |
| e19 | B, Y1/Y2, R2 | Receipt occurrence and two distinct units |
| e20 | B, Y1, R2 | First unit's unpacking occurrence |
| e21 | B, Y2, R2 | Second unit's unpacking occurrence |
| e27 | O1, X1/X2/Y1, R4 | Packing occurrence and qualified object participation |
| e28 | O1, R4 | Recorded shipping occurrence, not an authorization receipt |
| e29 | P1, R5 | Payment identity and receipt occurrence; amount unstated |
| e30 | I1/I2, P1, R5 | Clearing occurrence and payment-to-invoice associations |
| e33 | O2, X3/Y2, R4 | Second packing occurrence, no renumbering |
| e34 | O2, R4 | Second recorded shipping occurrence |

Every row also retains its activity label and printed time. The inventory
separates five actors, two orders, two supplier orders, five units, two invoices
and one payment. Product kinds X/Y are not physical-unit identities. Table
identifiers A/B denote supplier orders, not automatically supplier parties.

The context excerpts add four declared inputs: shared-customer scope, the
reason B's quantity changed, the invoice-count shipment policy, and the source's
qualitative explanation of the payment delay. They supply neither a customer ID
nor invoice amounts. They are retained context and rule inputs, not automatically
accepted facts or execution authority.

The compatibility probe is deliberately smaller than this inventory. It covers
B's two quantity states, two occurrences and their participation in B. It does
not yet cover e7's O2 participation or either row's actor. Its GREEN result must
not be called completion of these source rows, let alone the connected story.
