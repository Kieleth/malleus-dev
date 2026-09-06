# Malleus paper v4 shop-01 source-grounded review record

Template. The row counts are substituted at freeze, from the frozen cell's own
query result, at the same time as `paper-v4/evaluation-v4/shop-01/review-task.md`.
No placeholder may survive instantiation.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

`inputs.review_protocol_sha256` is empty and stays empty until a frozen protocol
binds this cell. The v2 protocol does not: its validator pins the evidence
surface to the selected reading and its question ids to `CQ-01` to `CQ-04`. The
open decision is recorded in the run contract under `evaluation.review_protocol`
and at the top of the review task.

Fill one `rows` entry per returned row, in order, zero-based: 5 for
CQ-S1, 1 for CQ-S2, 2 for CQ-S3, 9 for
CQ-S4, 17 in all. Cite row locators of the form `row:N:field` only,
naming the source file. Write the reasons in your own words and copy no source
row into this record beyond the locator.

Each `rationale` opens with the fixed tokens the task defines: `VALUE_MATCHES_ROW`,
`VALUE_DIFFERS_FROM_ROW` or `LOCATOR_NOT_RESOLVABLE`, then, on a `RELATION` row
only, `DERIVATION_LOCAL` or `DERIVATION_NON_LOCAL`, and on a `SUBJECT` or an
`ENTITY` row only, one of `SUBJECT_IN_ROW`, `SUBJECT_NOT_IN_ROW` or
`NO_SUBJECT_IN_ROW`; then the reason in your own words. The `rows` grammar is
closed at four keys, which is why every finding lives at the head of the text
field.

```json
{
  "schema": "malleus.paper-v4.source-grounded-review/v2",
  "status": "PRELIMINARY_COMPLETE",
  "inputs": {
    "review_protocol_sha256": "",
    "review_input_manifest_sha256": "sha256:8345df5f8bd77d28a2abe7e68620d6fce2c467fa48de7474f88bff4aa7b9236e"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-preliminary-shop-01",
    "completed_at": "2026-09-06T20:47:54Z"
  },
  "questions": [
    {
      "question_id": "CQ-S1",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The five rows name payment P1, the two invoices, and two relations running from P1 to each invoice, so the which-invoices part of the question is answered directly and nothing extraneous is returned. What the rows carry between the payment and the invoices is a reference relation, which is what the payments source states by listing invoice identifiers on the payment; the source states no settlement, and the question asks which invoices the payment settled, so that part is addressed only as far as the source reaches. Separately, every one of the five rows cites a row index past the end of the file it names, so no returned row's evidence pointer opens.",
      "source_locators": [
        "payments.jsonl row:0:payment_id",
        "payments.jsonl row:0:invoice_ids[0]",
        "payments.jsonl row:0:invoice_ids[1]",
        "invoices.csv row:0:invoice_id",
        "invoices.csv row:1:invoice_id"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "PARTIAL",
          "source_locators": [
            "invoices.csv row:2:invoice_id",
            "invoices.csv row:0:invoice_id"
          ],
          "rationale": "LOCATOR_NOT_RESOLVABLE NO_SUBJECT_IN_ROW invoices.csv carries a header line and two data rows, so on this task's convention its only rows are 0 and 1 and there is no row 2 to open. The invoice identifier the record holds on properties.name does sit in this file under the named field, two rows below the index the derivation gives, so the source surface backs the value while the pointer misses it. The projection is a name only and declares no subject."
        },
        {
          "row_index": 1,
          "source_support": "PARTIAL",
          "source_locators": [
            "invoices.csv row:3:invoice_id",
            "invoices.csv row:1:invoice_id"
          ],
          "rationale": "LOCATOR_NOT_RESOLVABLE NO_SUBJECT_IN_ROW Row 3 is past the end of invoices.csv, whose last data row is 1. The identifier the record holds on properties.name occurs at row 1 under the named field, the same two-row offset as the preceding record, so the file supports the value and the derivation does not reach it. Nothing in the projection names a subject."
        },
        {
          "row_index": 2,
          "source_support": "PARTIAL",
          "source_locators": [
            "payments.jsonl row:1:payment_id",
            "payments.jsonl row:0:payment_id"
          ],
          "rationale": "LOCATOR_NOT_RESOLVABLE NO_SUBJECT_IN_ROW payments.jsonl is one line long, so its only row is 0 and row 1 does not exist. That single line does carry the payment identifier the record holds on properties.name under the named field, one row below the named index. The projection carries the name alone and no subject."
        },
        {
          "row_index": 3,
          "source_support": "PARTIAL",
          "source_locators": [
            "payments.jsonl row:1:payment_id",
            "payments.jsonl row:1:invoice_ids[0]",
            "payments.jsonl row:0:payment_id",
            "payments.jsonl row:0:invoice_ids[0]"
          ],
          "rationale": "LOCATOR_NOT_RESOLVABLE DERIVATION_LOCAL All three derivations of this relation name row 1 of payments.jsonl, a one-line file whose only row is 0, so none of them opens. Reading that one line instead, it carries the payment identifier under payment_id and the target invoice identifier as the first element of invoice_ids, so both endpoints are backed by the file; the field the derivation names for properties.relation_type holds an invoice identifier there and not the relation constant the record carries on that path, which is a second and separate mismatch. The row named as formalising the relation and the row named as deriving its source endpoint are the same payments row, so the derivation is local."
        },
        {
          "row_index": 4,
          "source_support": "PARTIAL",
          "source_locators": [
            "payments.jsonl row:1:payment_id",
            "payments.jsonl row:1:invoice_ids[1]",
            "payments.jsonl row:0:payment_id",
            "payments.jsonl row:0:invoice_ids[1]"
          ],
          "rationale": "LOCATOR_NOT_RESOLVABLE DERIVATION_LOCAL This relation's three derivations also point at row 1 of a single-line payments.jsonl, so none can be opened. The file's one line does carry the payment identifier under payment_id and the second element of invoice_ids is the target invoice identifier, so the endpoints are backed; as with the sibling relation, the field named for properties.relation_type holds an invoice identifier rather than the constant the record carries there. Formalising row and source-endpoint row are the same payments row, so the derivation is local."
        }
      ]
    },
    {
      "question_id": "CQ-S2",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "Two halves, judged from two places as the task directs. The current half comes from the one returned row: it names supplier order B and its product code, which identifies the order, but it carries no quantity, and the question's current state is asked for with the ordered quantity. The superseded half comes from trace-summary.json, where the entry for supplier-order:B carries supersedes_record_id, superseded_by and valid_to all null, so the history holds no earlier state and that half of the question goes unanswered. The supplier order source does hold a second line for the same order under a different quantity, so the earlier state exists on the evidence surface and is absent from the answer.",
      "source_locators": [
        "supplier-order-history.jsonl row:1:supplier_order_id",
        "supplier-order-history.jsonl row:1:product_code",
        "supplier-order-history.jsonl row:1:quantity",
        "supplier-order-history.jsonl row:0:supplier_order_id",
        "supplier-order-history.jsonl row:0:quantity"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "supplier-order-history.jsonl row:1:supplier_order_id",
            "supplier-order-history.jsonl row:1:product_code"
          ],
          "rationale": "VALUE_MATCHES_ROW NO_SUBJECT_IN_ROW supplier-order-history.jsonl has two lines, so row 1 exists on this task's convention and both named fields open. The order identifier and the product code in that row are the values the record carries on properties.name and properties.product_code. The file's other row repeats those same two values, so the row-index offset that makes every other derivation in this block unopenable does not change the comparison here. The projection names no subject."
        }
      ]
    },
    {
      "question_id": "CQ-S3",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The question has two parts. Which inventory unit order O1 contains is not answered: the returned rows are ENTITY rows only, one of the Order type and one of the InventoryUnit type, and no row asserts any link between them. The binding's relation cases for this question all carry PaymentInvoiceRelation as the relation record type, so no containment relation between an Order and an InventoryUnit could be returned by these cases, and the graph holds a single record of each of the two types, so their appearing side by side follows from a type-only case rather than from a statement that one contains the other. The allowed source surface does carry an items field on warehouse.jsonl row:0 beside the order field; whether those identifiers denote inventory units is not stated by the rows and is not something this review decides. What product the returned inventory unit is is addressed on the face of the rows, through the product_code projection, although that projection's derivation locator does not resolve, as row 0 records. Part of the question is addressed and part is not.",
      "source_locators": [
        "warehouse.jsonl row:1:order",
        "warehouse.jsonl row:0:order",
        "warehouse.jsonl row:0:items[0]",
        "inventory-units.csv row:2:inventory_unit_id",
        "inventory-units.csv row:0:product_code"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "UNSUPPORTED",
          "source_locators": [
            "inventory-units.csv row:2:inventory_unit_id",
            "inventory-units.csv row:2:product_code",
            "inventory-units.csv row:0:inventory_unit_id",
            "inventory-units.csv row:0:product_code"
          ],
          "rationale": "LOCATOR_NOT_RESOLVABLE NO_SUBJECT_IN_ROW Both derivations of this witness name row:2 of inventory-units.csv, but under the convention this task fixes, where row:0 is the first row after the header, that file's last row is row:0, so there is no row at the named index to open and the cited rows supply nothing. Both named fields are in the header, and row:0 carries under each of them the value the record projects on the matching path, so what fails is the index rather than the field. The record's projection carries no subject and the binding declares no subject-bearing record type."
        },
        {
          "row_index": 1,
          "source_support": "UNSUPPORTED",
          "source_locators": [
            "warehouse.jsonl row:1:order",
            "warehouse.jsonl row:0:order"
          ],
          "rationale": "LOCATOR_NOT_RESOLVABLE NO_SUBJECT_IN_ROW This witness derives properties.name from row:1:order of warehouse.jsonl, and that file's last row is row:0, so the named row is not there to open. The order field of row:0 does carry the value the record projects. The retained warehouse plan indexes this same single-line file as row:1 throughout its gap entries, so the producer counted physical lines from one while this task counts from zero; the value is present in the file either way, but the locator as written reaches no row. The projection carries no subject."
        }
      ]
    },
    {
      "question_id": "CQ-S4",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The records half, judged from the rows as the task directs: the rows return every current record and relation the graph holds, spanning each entity type in the question's type set and the one relation type on the surface, with no filter on source, because the binding is type-only and no case names a source. The warehouse-derived records are therefore present among the rows, but the rows do not identify which of them those are. The derivation half, judged from trace-summary.json as the task directs: the trace does carry a source_id and a locator for every record, and the records whose source is source:small-shop:warehouse are actor:R4 at row:1:actor and order:O1 at row:1:order. Both locators name a row past warehouse.jsonl's only row, so the locators the question asks for are supplied but do not resolve against the file; the same fields at row:0 carry the values those two records project. One half is answered outside the rows and the other is not isolated by them.",
      "source_locators": [
        "warehouse.jsonl row:1:actor",
        "warehouse.jsonl row:1:order",
        "warehouse.jsonl row:0:actor",
        "warehouse.jsonl row:0:order"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "UNSUPPORTED",
          "source_locators": [
            "warehouse.jsonl row:1:actor",
            "warehouse.jsonl row:0:actor"
          ],
          "rationale": "LOCATOR_NOT_RESOLVABLE NO_SUBJECT_IN_ROW The witness derives properties.name from row:1:actor of warehouse.jsonl, whose last row is row:0 under this task's convention, so the cited row does not exist and supports nothing. The actor field of row:0 carries the value the record projects, so the miss is one row of index, not a missing field. The projection carries no subject."
        },
        {
          "row_index": 1,
          "source_support": "UNSUPPORTED",
          "source_locators": [
            "inventory-units.csv row:2:inventory_unit_id",
            "inventory-units.csv row:2:product_code",
            "inventory-units.csv row:0:inventory_unit_id",
            "inventory-units.csv row:0:product_code"
          ],
          "rationale": "LOCATOR_NOT_RESOLVABLE NO_SUBJECT_IN_ROW Same witness and same two derivations as CQ-S3 row 0, judged again here as its own row: row:2 of inventory-units.csv is past that file's last row, which is row:0 once the header is excluded as the task directs. Row:0 carries both named fields with the values the record projects, so the file supports the projection and the pointer does not reach it. No subject appears in the projection."
        },
        {
          "row_index": 2,
          "source_support": "UNSUPPORTED",
          "source_locators": [
            "invoices.csv row:2:invoice_id",
            "invoices.csv row:0:invoice_id"
          ],
          "rationale": "LOCATOR_NOT_RESOLVABLE NO_SUBJECT_IN_ROW The name derives from row:2:invoice_id of invoices.csv, whose last data row is row:1 once the header is excluded, so the named row is past the end of the file. The invoice_id field of row:0 carries the value this record projects. The retained invoices-payments plan numbers the same file's data rows as row:2 and row:3, which is a header-inclusive count from one and not the count this task sets. The projection carries no subject."
        },
        {
          "row_index": 3,
          "source_support": "UNSUPPORTED",
          "source_locators": [
            "invoices.csv row:3:invoice_id",
            "invoices.csv row:1:invoice_id"
          ],
          "rationale": "LOCATOR_NOT_RESOLVABLE NO_SUBJECT_IN_ROW row:3:invoice_id names a row two past the last data row of invoices.csv, so nothing opens there. The value this record projects on properties.name is present in the file, in the invoice_id field of row:1, under the same one-off-by-the-header shift that the sibling invoice row shows. No subject in the projection."
        },
        {
          "row_index": 4,
          "source_support": "UNSUPPORTED",
          "source_locators": [
            "warehouse.jsonl row:1:order",
            "warehouse.jsonl row:0:order"
          ],
          "rationale": "LOCATOR_NOT_RESOLVABLE NO_SUBJECT_IN_ROW Same witness and derivation as CQ-S3 row 1, judged again here: warehouse.jsonl holds one row, row:0, and the derivation names row:1, so the cited row is absent. The order field of row:0 carries the projected value. The projection carries no subject."
        },
        {
          "row_index": 5,
          "source_support": "UNSUPPORTED",
          "source_locators": [
            "payments.jsonl row:1:payment_id",
            "payments.jsonl row:0:payment_id"
          ],
          "rationale": "LOCATOR_NOT_RESOLVABLE NO_SUBJECT_IN_ROW payments.jsonl holds a single line, so its only row is row:0 and the derivation's row:1:payment_id opens nothing. The payment_id field of row:0 carries the value the record projects on properties.name. The projection carries no subject."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "supplier-order-history.jsonl row:1:supplier_order_id",
            "supplier-order-history.jsonl row:1:product_code"
          ],
          "rationale": "VALUE_MATCHES_ROW NO_SUBJECT_IN_ROW Both derivations name row:1 of supplier-order-history.jsonl, which under this task's zero-based convention is the file's second line and does exist. Its supplier_order_id and product_code fields carry exactly the values the record projects on properties.name and properties.product_code, so the cited row supports both projected claims. One qualifier: the retained supplier-orders plan indexes this file's two lines as row:1 and row:2, so the line this review opened is not the line the producer counted, and because both lines repeat the same identifier and the same product code, this match cannot discriminate between the two conventions. The projection carries no subject."
        },
        {
          "row_index": 7,
          "source_support": "UNSUPPORTED",
          "source_locators": [
            "payments.jsonl row:1:payment_id",
            "payments.jsonl row:1:invoice_ids[0]",
            "payments.jsonl row:0:payment_id",
            "payments.jsonl row:0:invoice_ids[0]"
          ],
          "rationale": "LOCATOR_NOT_RESOLVABLE DERIVATION_LOCAL All three derivations of this relation name row:1 of payments.jsonl, and that file's only row is row:0, so none of them opens and the cited rows support neither endpoint nor the relation property. Locality holds as declared: the row named for the relation's own source_id and target_id paths is the same file and index the source endpoint payment:P1 derives from, so the row that formalizes the relation is among the rows that derive an endpoint. A separate fact, not part of the judgment above: at the resolvable row:0 the invoice_ids[0] element carries an invoice identifier while the path it feeds, properties.relation_type, carries the relation type constant, so correcting the index alone would not turn that one derivation into a value match."
        },
        {
          "row_index": 8,
          "source_support": "UNSUPPORTED",
          "source_locators": [
            "payments.jsonl row:1:payment_id",
            "payments.jsonl row:1:invoice_ids[1]",
            "payments.jsonl row:0:payment_id",
            "payments.jsonl row:0:invoice_ids[1]"
          ],
          "rationale": "LOCATOR_NOT_RESOLVABLE DERIVATION_LOCAL The second relation's derivations name the same absent row:1 of payments.jsonl, on the second element of invoice_ids for the relation property and the target endpoint and on payment_id for the source endpoint, so nothing opens at the cited index. Locality is as declared, for the same reason as the sibling relation row: the relation's own row is the row its source endpoint derives from. The second element of invoice_ids does exist at row:0, and the note made on the sibling row about that element feeding properties.relation_type applies here too."
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
  "source_locators": ["warehouse.jsonl row:0:order"],
  "rationale": "VALUE_MATCHES_ROW NO_SUBJECT_IN_ROW one or two sentences in your own words"
}
```
