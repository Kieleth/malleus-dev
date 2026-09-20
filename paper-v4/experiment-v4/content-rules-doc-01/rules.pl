% Three adopter rules over run-23's document population, fact contract 3.
% Every slot name below is read from run-23's compiled ontology; the fact
% contract carries no slot range, so the exclusions and the qualifier list are
% stated here and justified in README.md.

malleus_rule('VALUE_IN_CITED_TEXT').
malleus_rule('NO_CONFLICTING_QUANTITY').
malleus_rule('NO_EMPTY_RECORD').

% ---------------------------------------------------------------------------
% Normalisation: whitespace and case, and nothing else.
%
% Case folds with downcase_atom/2. Every maximal run of the listed whitespace
% characters becomes one space and leading and trailing runs are dropped. No
% punctuation stripping, no Unicode normalisation, no unit folding, no number
% reformatting. A number arrives as Prolog prints it, so a float the producer
% wrote as 40.0 is compared as '40.0'.
% ---------------------------------------------------------------------------

whitespace_chars(" \t\n\r\v\f\u00a0").

normalised(Raw, Normal) :-
    downcase_atom(Raw, Lower),
    whitespace_chars(White),
    split_string(Lower, White, White, Pieces),
    nonempty(Pieces, Words),
    atomic_list_concat(Words, ' ', Normal).

nonempty([], []).
nonempty([""|Rest], Words) :-
    !,
    nonempty(Rest, Words).
nonempty([Piece|Rest], [Piece|Words]) :-
    nonempty(Rest, Words).

% ---------------------------------------------------------------------------
% Rule 1: a record's scalar values occur in the text the record cites.
% ---------------------------------------------------------------------------

% Record references: the value names another record, so it resolves through
% the graph and not through a sentence.
excluded_slot('subject').
excluded_slot('caused_by').

% Enumerations: the value is a permissible-value name this contract or an
% imported pack mints, and the source states the concept in its own words.
excluded_slot('agent_type').
excluded_slot('assertion_modality').
excluded_slot('contribution_role').
excluded_slot('depth_reference').
excluded_slot('determination').
excluded_slot('event_type').
excluded_slot('hypothesis_disposition').
excluded_slot('melt_stage').
excluded_slot('quantity_kind_class').
excluded_slot('relation_type').
excluded_slot('source_kind').
excluded_slot('temporal_precision').
excluded_slot('value_qualification').

% Capture coordinates: not statements the source makes. The first is the
% rule's own input and the second is a digest of a sentence, never a phrase
% inside it.
excluded_slot('assertion_locator').
excluded_slot('statement_sha256').

% Record bookkeeping the record carries about itself.
excluded_slot('created_at').
excluded_slot('updated_at').
excluded_slot('order_key').

readable_kind(string).
readable_kind(integer).
readable_kind(float).

malleus_violation('VALUE_IN_CITED_TEXT', Code, [Record]) :-
    m_property(Record, 'assertion_locator', string, Locator),
    m_source_text(_, Locator, Text),
    normalised(Text, NormalText),
    m_property(Record, Name, Kind, Value),
    readable_kind(Kind),
    \+ excluded_slot(Name),
    normalised(Value, NormalValue),
    \+ sub_atom(NormalText, _, _, _, NormalValue),
    atomic_list_concat(['VALUE_NOT_IN_CITED_TEXT', Name], '/', Code).

% ---------------------------------------------------------------------------
% Rule 2: two current records state a different value for the same quantity
% of the same subject.
% ---------------------------------------------------------------------------

% Slots that say which quantity of which subject is reported. They must agree,
% or a different value is two quantities rather than a disagreement.
% uncertainty is not here: it is part of the value, not of what it is about.
qualifier('unit').
qualifier('determination').
qualifier('value_qualification').
qualifier('depth_reference').
qualifier('melt_stage').
qualifier('analyte').
qualifier('estimation_proxy').
qualifier('begins_at').
qualifier('ends_at').
qualifier('temporal_precision').
qualifier('temporal_reference_system').

qualifiers_agree(A, B) :-
    forall(
        qualifier(Slot),
        (   findall(Value, m_property(A, Slot, _, Value), Left),
            findall(Value, m_property(B, Slot, _, Value), Right),
            Left == Right
        )
    ).

subject_pair(A, B) :-
    m_property(A, 'subject', Kind, Subject),
    m_property(B, 'subject', Kind, Subject),
    A @< B.

stated(Record, Slot, Value) :-
    (   m_property(Record, Slot, _, Found)
    ->  Value = Found
    ;   Value = absent
    ).

% metrology Quantified: the quantity kind is quantity_kind and the value is
% the closed (value_lower, value_upper) pair.
malleus_violation('NO_CONFLICTING_QUANTITY', 'QUANTITY_DISAGREEMENT', [A, B]) :-
    subject_pair(A, B),
    m_property(A, 'quantity_kind', KindKind, QuantityKind),
    m_property(B, 'quantity_kind', KindKind, QuantityKind),
    stated(A, 'value_lower', LowerA),
    stated(B, 'value_lower', LowerB),
    stated(A, 'value_upper', UpperA),
    stated(B, 'value_upper', UpperB),
    bounds(LowerA, UpperA) \== bounds(LowerB, UpperB),
    qualifiers_agree(A, B).

% metrology Counted: the quantity kind is count_scope and the value is count.
malleus_violation('NO_CONFLICTING_QUANTITY', 'COUNT_DISAGREEMENT', [A, B]) :-
    subject_pair(A, B),
    m_property(A, 'count_scope', ScopeKind, Scope),
    m_property(B, 'count_scope', ScopeKind, Scope),
    stated(A, 'count', CountA),
    stated(B, 'count', CountB),
    CountA \== CountB,
    qualifiers_agree(A, B).

% metrology Ratio: the quantity kind is the numerator and denominator kinds
% taken together and the value is ratio_value.
malleus_violation('NO_CONFLICTING_QUANTITY', 'RATIO_DISAGREEMENT', [A, B]) :-
    subject_pair(A, B),
    m_property(A, 'numerator_kind', NumeratorKind, Numerator),
    m_property(B, 'numerator_kind', NumeratorKind, Numerator),
    m_property(A, 'denominator_kind', DenominatorKind, Denominator),
    m_property(B, 'denominator_kind', DenominatorKind, Denominator),
    stated(A, 'ratio_value', ValueA),
    stated(B, 'ratio_value', ValueB),
    ValueA \== ValueB,
    qualifiers_agree(A, B).

% ---------------------------------------------------------------------------
% Rule 3: a record of any kind carries no property at all.
% ---------------------------------------------------------------------------

malleus_violation('NO_EMPTY_RECORD', 'RECORD_WITHOUT_PROPERTIES', [Record]) :-
    m_record(Record, _, _),
    \+ m_property(Record, _, _, _),
    \+ m_list(Record, _, _).
