-- G2b: a relational projection of one G1 specimen (Construction B of
-- STORAGE-FLOWS-01.md). One database holds one specimen. Research witness only:
-- not a Core schema, not a public format, not a storage decision.
--
-- Conventions
--   * Exact ids are keys. No key contains a value, a time or a basis, so two
--     claims with equal value and equal times stay two rows.
--   * Typed literals keep datatype, lexical form and unit in TEXT columns of
--     STRICT tables. TEXT affinity never turns '0750' or '5.40' into a number.
--   * Times are fixed-width UTC strings, so string order is time order.
--     The GLOB checks below make that assumption mechanical.
--   * Every foreign key is DEFERRABLE INITIALLY DEFERRED. The encoder inserts a
--     whole change, then reads PRAGMA foreign_key_check to name what is missing,
--     then commits or rolls back. foreign_keys must be ON per connection.
--   * Named CHECK constraints whose name starts with a refusal category are read
--     by the encoder to classify an attempt.
--   * NULL in an optional column means the field was absent in the input.

-- The ledger: accepted changes in knowledge order. seq 0 is genesis.
CREATE TABLE change (
    seq       INTEGER PRIMARY KEY,
    position  TEXT NOT NULL UNIQUE,
    kind      TEXT NOT NULL CHECK (kind IN (
        'GENESIS', 'REPORT', 'TRANSITION', 'CORRECTION', 'ASSUMPTION', 'INTERPRETATION',
        'REASSESSMENT', 'ARGUMENT', 'MODEL_DEFINITION', 'CONTEXT_BINDING',
        'EXECUTION_RECORD', 'RULE_DECLARATION', 'PLAN', 'CONTRACT_DECLARATION')),
    base_seq  INTEGER REFERENCES change(seq) DEFERRABLE INITIALLY DEFERRED,
    note      TEXT,
    CHECK ((seq = 0) = (kind = 'GENESIS')),
    CHECK ((seq = 0) = (base_seq IS NULL))
) STRICT;

CREATE TABLE change_target (
    seq        INTEGER NOT NULL REFERENCES change(seq) DEFERRABLE INITIALLY DEFERRED,
    ord        INTEGER NOT NULL,
    target_id  TEXT NOT NULL REFERENCES record(id) DEFERRABLE INITIALLY DEFERRED,
    PRIMARY KEY (seq, ord),
    UNIQUE (seq, target_id)
) STRICT;

-- Records: identity, type, the change that accepted it, governing contract.
CREATE TABLE record (
    id           TEXT PRIMARY KEY,
    type         TEXT NOT NULL CHECK (type IN (
        'SUBJECT', 'ACCOUNT', 'SOURCE', 'CONTRACT', 'ASSERTION', 'RELATION', 'GROUP',
        'ARGUMENT', 'CONTEXT', 'MODEL', 'EXECUTION', 'RESULT', 'RULE', 'PLAN')),
    added_seq    INTEGER NOT NULL REFERENCES change(seq) DEFERRABLE INITIALLY DEFERRED,
    add_ord      INTEGER NOT NULL,
    contract_id  TEXT REFERENCES contract(id) DEFERRABLE INITIALLY DEFERRED,
    note         TEXT,
    UNIQUE (id, type),
    UNIQUE (added_seq, add_ord)
) STRICT;

-- Which optional list or map fields were present in the input (so an explicit
-- empty list, such as C1's evidence_refs, round-trips).
CREATE TABLE list_field (
    owner_id  TEXT NOT NULL REFERENCES record(id) DEFERRABLE INITIALLY DEFERRED,
    field     TEXT NOT NULL,
    PRIMARY KEY (owner_id, field)
) STRICT;

CREATE TABLE named (                      -- SUBJECT and ACCOUNT
    id     TEXT PRIMARY KEY,
    type   TEXT NOT NULL CHECK (type IN ('SUBJECT', 'ACCOUNT')),
    label  TEXT NOT NULL,
    FOREIGN KEY (id, type) REFERENCES record(id, type) DEFERRABLE INITIALLY DEFERRED
) STRICT;

-- Retained artifacts. available = 0 means the ledger names the artifact but its
-- bytes were withheld from this rebuild; payload columns are then NULL.
CREATE TABLE source (
    id           TEXT PRIMARY KEY,
    type         TEXT NOT NULL DEFAULT 'SOURCE' CHECK (type = 'SOURCE'),
    available    INTEGER NOT NULL CHECK (available IN (0, 1)),
    source_kind  TEXT CHECK (source_kind IN ('SYNTHETIC_TEXT', 'RETAINED_DECLARATION', 'REAL_BLOCK_POINTER')),
    text         TEXT,
    locator      TEXT,
    pointer      TEXT,
    CHECK ((available = 1) = (source_kind IS NOT NULL AND text IS NOT NULL)),
    FOREIGN KEY (id, type) REFERENCES record(id, type) DEFERRABLE INITIALLY DEFERRED
) STRICT;

CREATE TABLE contract (
    id         TEXT PRIMARY KEY,
    type       TEXT NOT NULL DEFAULT 'CONTRACT' CHECK (type = 'CONTRACT'),
    available  INTEGER NOT NULL CHECK (available IN (0, 1)),
    version    TEXT,
    identity   TEXT,
    CHECK ((available = 1) = (version IS NOT NULL AND identity IS NOT NULL)),
    FOREIGN KEY (id, type) REFERENCES record(id, type) DEFERRABLE INITIALLY DEFERRED
) STRICT;

CREATE TABLE model (
    id              TEXT PRIMARY KEY,
    type            TEXT NOT NULL DEFAULT 'MODEL' CHECK (type = 'MODEL'),
    available       INTEGER NOT NULL CHECK (available IN (0, 1)),
    version         TEXT,
    implementation  TEXT,
    formula         TEXT,
    CHECK ((available = 1) = (version IS NOT NULL AND implementation IS NOT NULL AND formula IS NOT NULL)),
    FOREIGN KEY (id, type) REFERENCES record(id, type) DEFERRABLE INITIALLY DEFERRED
) STRICT;

CREATE TABLE model_parameter (
    model_id  TEXT NOT NULL REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED,
    ord       INTEGER NOT NULL,
    name      TEXT NOT NULL,
    PRIMARY KEY (model_id, ord),
    UNIQUE (model_id, name)
) STRICT;

-- Assertions: the claim identity is the id alone. Value, basis, account and
-- stated applicability are payload, never key.
CREATE TABLE assertion (
    id           TEXT PRIMARY KEY,
    type         TEXT NOT NULL DEFAULT 'ASSERTION' CHECK (type = 'ASSERTION'),
    subject_id   TEXT NOT NULL REFERENCES record(id) DEFERRABLE INITIALLY DEFERRED,
    property     TEXT NOT NULL,
    v_datatype   TEXT NOT NULL CHECK (v_datatype IN ('xsd:integer', 'xsd:decimal', 'xsd:string', 'xsd:boolean', 'xsd:dateTime', 'enum')),
    v_lexical    TEXT NOT NULL,
    v_unit       TEXT,
    basis        TEXT NOT NULL CHECK (basis IN ('REPORTED', 'ASSUMPTION', 'CORRECTION', 'INTERPRETATION')),
    account_id   TEXT REFERENCES record(id) DEFERRABLE INITIALLY DEFERRED,
    corrects_id  TEXT REFERENCES assertion(id) DEFERRABLE INITIALLY DEFERRED,
    revises_id   TEXT REFERENCES assertion(id) DEFERRABLE INITIALLY DEFERRED,
    app_kind     TEXT NOT NULL,
    app_from     TEXT,
    app_until    TEXT,
    app_instant  TEXT,
    CONSTRAINT UNSUPPORTED_SEMANTICS_applicability_kind
        CHECK (app_kind IN ('INTERVAL', 'INSTANT', 'NONE_STATED')),
    CONSTRAINT MALFORMED_applicability_shape CHECK (
        (app_kind = 'INTERVAL' AND app_from IS NOT NULL AND app_instant IS NULL
            AND (app_until IS NULL OR app_until > app_from))
        OR (app_kind = 'INSTANT' AND app_instant IS NOT NULL AND app_from IS NULL AND app_until IS NULL)
        OR (app_kind = 'NONE_STATED' AND app_from IS NULL AND app_until IS NULL AND app_instant IS NULL)),
    CONSTRAINT MALFORMED_time CHECK (
        (app_from IS NULL OR app_from GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]Z')
        AND (app_until IS NULL OR app_until GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]Z')
        AND (app_instant IS NULL OR app_instant GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]Z')),
    CHECK ((basis = 'CORRECTION') = (corrects_id IS NOT NULL)),
    FOREIGN KEY (id, type) REFERENCES record(id, type) DEFERRABLE INITIALLY DEFERRED
) STRICT;

CREATE TABLE relation (
    id             TEXT PRIMARY KEY,
    type           TEXT NOT NULL DEFAULT 'RELATION' CHECK (type = 'RELATION'),
    relation_type  TEXT NOT NULL,
    from_id        TEXT NOT NULL REFERENCES record(id) DEFERRABLE INITIALLY DEFERRED,
    to_id          TEXT NOT NULL REFERENCES record(id) DEFERRABLE INITIALLY DEFERRED,
    basis          TEXT CHECK (basis IN ('REPORTED', 'ASSUMPTION', 'CORRECTION', 'INTERPRETATION')),
    FOREIGN KEY (id, type) REFERENCES record(id, type) DEFERRABLE INITIALLY DEFERRED
) STRICT;

-- Qualifiers of assertions and relations: typed literals keyed by owner and name.
CREATE TABLE qualifier (
    owner_id  TEXT NOT NULL REFERENCES record(id) DEFERRABLE INITIALLY DEFERRED,
    name      TEXT NOT NULL,
    datatype  TEXT NOT NULL CHECK (datatype IN ('xsd:integer', 'xsd:decimal', 'xsd:string', 'xsd:boolean', 'xsd:dateTime', 'enum')),
    lexical   TEXT NOT NULL,
    unit      TEXT,
    PRIMARY KEY (owner_id, name)
) STRICT;

CREATE TABLE claim_group (
    id          TEXT PRIMARY KEY,
    type        TEXT NOT NULL DEFAULT 'GROUP' CHECK (type = 'GROUP'),
    group_kind  TEXT NOT NULL,
    FOREIGN KEY (id, type) REFERENCES record(id, type) DEFERRABLE INITIALLY DEFERRED
) STRICT;

-- Graph membership: a GROUP's members or a MODEL's member terms. Membership in
-- one graph says nothing about membership in another.
CREATE TABLE membership (
    graph_id   TEXT NOT NULL REFERENCES record(id) DEFERRABLE INITIALLY DEFERRED,
    ord        INTEGER NOT NULL,
    member_id  TEXT NOT NULL REFERENCES record(id) DEFERRABLE INITIALLY DEFERRED,
    PRIMARY KEY (graph_id, member_id),
    UNIQUE (graph_id, ord)
) STRICT;

CREATE TABLE argument (
    id             TEXT PRIMARY KEY,
    type           TEXT NOT NULL DEFAULT 'ARGUMENT' CHECK (type = 'ARGUMENT'),
    conclusion_id  TEXT NOT NULL REFERENCES assertion(id) DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (id, type) REFERENCES record(id, type) DEFERRABLE INITIALLY DEFERRED
) STRICT;

CREATE TABLE premise (
    argument_id  TEXT NOT NULL REFERENCES argument(id) DEFERRABLE INITIALLY DEFERRED,
    ord          INTEGER NOT NULL,
    premise_id   TEXT NOT NULL REFERENCES record(id) DEFERRABLE INITIALLY DEFERRED,
    PRIMARY KEY (argument_id, premise_id),
    UNIQUE (argument_id, ord)
) STRICT;

CREATE TABLE context (
    id            TEXT PRIMARY KEY,
    type          TEXT NOT NULL DEFAULT 'CONTEXT' CHECK (type = 'CONTEXT'),
    context_kind  TEXT NOT NULL,
    model_id      TEXT REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (id, type) REFERENCES record(id, type) DEFERRABLE INITIALLY DEFERRED
) STRICT;

CREATE TABLE context_basis (
    context_id  TEXT NOT NULL REFERENCES context(id) DEFERRABLE INITIALLY DEFERRED,
    ord         INTEGER NOT NULL,
    basis_id    TEXT NOT NULL REFERENCES record(id) DEFERRABLE INITIALLY DEFERRED,
    PRIMARY KEY (context_id, ord)
) STRICT;

CREATE TABLE execution (
    id              TEXT PRIMARY KEY,
    type            TEXT NOT NULL DEFAULT 'EXECUTION' CHECK (type = 'EXECUTION'),
    model_id        TEXT NOT NULL REFERENCES model(id) DEFERRABLE INITIALLY DEFERRED,
    context_id      TEXT REFERENCES context(id) DEFERRABLE INITIALLY DEFERRED,
    implementation  TEXT,
    FOREIGN KEY (id, type) REFERENCES record(id, type) DEFERRABLE INITIALLY DEFERRED
) STRICT;

-- Selection and execution bindings: a context's or an execution's exact premise
-- per parameter, with the coordinates used to choose it when recorded.
CREATE TABLE binding (
    owner_id        TEXT NOT NULL REFERENCES record(id) DEFERRABLE INITIALLY DEFERRED,
    ord             INTEGER NOT NULL,
    parameter       TEXT NOT NULL,
    assertion_id    TEXT NOT NULL REFERENCES assertion(id) DEFERRABLE INITIALLY DEFERRED,
    sel_at          TEXT REFERENCES change(position) DEFERRABLE INITIALLY DEFERRED,
    sel_valid_at    TEXT,
    sel_account_id  TEXT REFERENCES record(id) DEFERRABLE INITIALLY DEFERRED,
    PRIMARY KEY (owner_id, ord),
    UNIQUE (owner_id, parameter),
    CHECK (sel_at IS NOT NULL OR (sel_valid_at IS NULL AND sel_account_id IS NULL))
) STRICT;

CREATE TABLE result (
    id            TEXT PRIMARY KEY,
    type          TEXT NOT NULL DEFAULT 'RESULT' CHECK (type = 'RESULT'),
    execution_id  TEXT NOT NULL REFERENCES execution(id) DEFERRABLE INITIALLY DEFERRED,
    v_datatype    TEXT NOT NULL CHECK (v_datatype IN ('xsd:integer', 'xsd:decimal', 'xsd:string', 'xsd:boolean', 'xsd:dateTime', 'enum')),
    v_lexical     TEXT NOT NULL,
    v_unit        TEXT,
    FOREIGN KEY (id, type) REFERENCES record(id, type) DEFERRABLE INITIALLY DEFERRED
) STRICT;

CREATE TABLE rule (
    id         TEXT PRIMARY KEY,
    type       TEXT NOT NULL DEFAULT 'RULE' CHECK (type = 'RULE'),
    semantics  TEXT NOT NULL,
    FOREIGN KEY (id, type) REFERENCES record(id, type) DEFERRABLE INITIALLY DEFERRED
) STRICT;

CREATE TABLE rule_scope (
    rule_id     TEXT NOT NULL REFERENCES rule(id) DEFERRABLE INITIALLY DEFERRED,
    ord         INTEGER NOT NULL,
    subject_id  TEXT NOT NULL REFERENCES record(id) DEFERRABLE INITIALLY DEFERRED,
    PRIMARY KEY (rule_id, ord)
) STRICT;

CREATE TABLE rule_assumption (
    rule_id  TEXT NOT NULL REFERENCES rule(id) DEFERRABLE INITIALLY DEFERRED,
    ord      INTEGER NOT NULL,
    text     TEXT NOT NULL,
    PRIMARY KEY (rule_id, ord)
) STRICT;

CREATE TABLE plan (
    id           TEXT PRIMARY KEY,
    type         TEXT NOT NULL DEFAULT 'PLAN' CHECK (type = 'PLAN'),
    subject_id   TEXT NOT NULL REFERENCES record(id) DEFERRABLE INITIALLY DEFERRED,
    action       TEXT NOT NULL,
    planned_for  TEXT NOT NULL,
    FOREIGN KEY (id, type) REFERENCES record(id, type) DEFERRABLE INITIALLY DEFERRED
) STRICT;

-- Evidence links: owner record to retained source.
CREATE TABLE evidence (
    owner_id   TEXT NOT NULL REFERENCES record(id) DEFERRABLE INITIALLY DEFERRED,
    ord        INTEGER NOT NULL,
    source_id  TEXT NOT NULL REFERENCES source(id) DEFERRABLE INITIALLY DEFERRED,
    PRIMARY KEY (owner_id, ord),
    UNIQUE (owner_id, source_id)
) STRICT;

-- Temporal effects, derived by the encoder from each change's declared kind and
-- targets, using only the prefix up to that change. Append-only: an OPEN starts
-- a version of an assertion's applicability (a "cell"); an END closes the
-- version open before it. Knowledge ends are never written back into older rows,
-- so a read at an earlier position cannot see a later closure.
CREATE TABLE temporal_effect (
    seq           INTEGER NOT NULL REFERENCES change(seq) DEFERRABLE INITIALLY DEFERRED,
    op            TEXT NOT NULL CHECK (op IN ('OPEN', 'END')),
    assertion_id  TEXT NOT NULL REFERENCES assertion(id) DEFERRABLE INITIALLY DEFERRED,
    app_kind      TEXT CHECK (app_kind IN ('INTERVAL', 'INSTANT', 'NONE_STATED')),
    valid_from    TEXT,
    valid_until   TEXT,
    instant       TEXT,
    PRIMARY KEY (seq, op, assertion_id),
    CHECK ((op = 'END') = (app_kind IS NULL)),
    CHECK (valid_until IS NULL OR valid_until > valid_from)
) STRICT;
