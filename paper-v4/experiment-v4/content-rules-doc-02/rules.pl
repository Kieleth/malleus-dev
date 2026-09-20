% =====================================================================
% Four adopter rules over run-23's document population, fact contract 3.
%
% Luis chose these four from rule-census-01's measured table: the conflict
% rule with assertion_modality among the qualifiers, interval sanity, numbers
% in the cited text over the numeric slots, and formulas in the cited text
% over the formula slots. The unit rule is dropped. README.md states each
% definition; this file is the only place any of them is implemented.
%
% The normalisation and the number grammar are here rather than in Python
% because Core's check contract admits a pinned Prolog program and nothing
% else: LogicContract closes its fields, its only implementation field is
% rules_file, and PrologVerifier is the one verifier Core ships.
% equivalence.py proves these bytes agree with rule-census-01/normalise.py on
% a shared fixture table and over run-23's own sentences and slot values.
% =====================================================================

:- discontiguous malleus_violation/3.

malleus_rule('NO_CONFLICTING_QUANTITY').
malleus_rule('INTERVAL_SANITY').
malleus_rule('NUMBER_IN_CITED_TEXT').
malleus_rule('FORMULA_IN_SOURCE').

% ---------------------------------------------------------------------
% Declarations derived from the compiled ontology
%
% Every fact in this block is read off run-23's compiled contract, which
% logic.yaml pins by hash. test_content_rules_doc_02.py recomputes both sets
% from that contract and fails if this block differs by one slot.
%
%   numeric_slot/1  every slot the contract declares with range Float or
%                   Integer, on any declared type.
%   subject_slot/1  every slot declared with range Entity on a type that is
%                   not a Relation subtype. source_id and target_id are also
%                   Entity-ranged and are excluded because a relation's
%                   endpoints are emitted as m_relation/4, never as property
%                   facts.
% ---------------------------------------------------------------------

numeric_slot('assertion_confidence').
numeric_slot('count').
numeric_slot('publication_year').
numeric_slot('ratio_value').
numeric_slot('strength').
numeric_slot('uncertainty').
numeric_slot('value').
numeric_slot('value_lower').
numeric_slot('value_upper').

subject_slot('subject').

% ---------------------------------------------------------------------
% Adopter declarations
%
% These are the distinctions the compiled ontology does not carry, declared
% here because this file is the one place the check contract pins by digest.
% Core closes logic.yaml's fields (malleus.logic.CONTRACT_FIELDS), so the
% declaration Luis asked for in that file lives here instead; logic.yaml
% carries the pointer.
%
% The Core requirement that would let the ontology supply them is the
% per-slot source relation recorded at ledger entry E-0430 and carried as
% items E2 and E3 in ROADMAP.md: the contract declares analyte,
% numerator_kind, denominator_kind, quantity_kind, count_scope, name and
% description all as String and says nothing about which of them is copied
% from the source, tallied from it, or authored by the producer. Until it
% does, the three formula slots and the qualifier list are an adopter's
% assertion about its own ontology, and a test holds each one to the range
% the contract declares for it.
% ---------------------------------------------------------------------

formula_slot('analyte').
formula_slot('numerator_kind').
formula_slot('denominator_kind').

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
qualifier('assertion_modality').

quantity_family('QUANTITY').
quantity_family('COUNT').
quantity_family('RATIO').

quantity_identity('QUANTITY', 'quantity_kind').
quantity_identity('COUNT', 'count_scope').
quantity_identity('RATIO', 'numerator_kind').
quantity_identity('RATIO', 'denominator_kind').

quantity_value('QUANTITY', 'value_lower').
quantity_value('QUANTITY', 'value_upper').
quantity_value('COUNT', 'count').
quantity_value('RATIO', 'ratio_value').

bound_pair('value_lower', 'value_upper').

non_negative_slot('count').
non_negative_slot('ratio_value').
non_negative_slot('uncertainty').

% ---------------------------------------------------------------------
% Character classes
% ---------------------------------------------------------------------

ws_code(32).
ws_code(9).
ws_code(10).
ws_code(13).
ws_code(11).
ws_code(12).
ws_code(160).

ascii_letter(C) :- integer(C), C >= 0'a, C =< 0'z.
ascii_letter(C) :- integer(C), C >= 0'A, C =< 0'Z.
ascii_lower(C) :- integer(C), C >= 0'a, C =< 0'z.
digit_code(C) :- integer(C), C >= 0'0, C =< 0'9.
point_code(C) :- integer(C), ( C =:= 46 ; C =:= 44 ).
decimal_point(C) :- integer(C), C =:= 46.
sign_code(C) :- integer(C), ( C =:= 0'- ; C =:= 8722 ).
plus_minus_code(C) :- integer(C), C =:= 177.
digit_or_point(C) :- digit_code(C), !.
digit_or_point(C) :- decimal_point(C).

ligature(64256, [0'f, 0'f]).
ligature(64257, [0'f, 0'i]).
ligature(64258, [0'f, 0'l]).
ligature(64259, [0'f, 0'f, 0'i]).
ligature(64260, [0'f, 0'f, 0'l]).
ligature(64261, [0's, 0't]).
ligature(64262, [0's, 0't]).

% ---------------------------------------------------------------------
% The declared normalisation, once, applied to every string compared here
%
% Ligatures, hyphen-space breaks inside a word, spaced digit sequences,
% letter-to-digit gluing, whitespace collapse and case folding, in that
% order. Each rewrite runs to a fixed point over non-overlapping matches,
% which is what the Python it mirrors does.
% ---------------------------------------------------------------------

normalised(Raw, Normal) :-
    atom_codes(Raw, Codes0),
    expand_ligatures(Codes0, Codes1),
    fixpoint(hyphen_break, Codes1, Codes2),
    fixpoint(spaced_point, Codes2, Codes3),
    fixpoint(spaced_digits, Codes3, Codes4),
    fixpoint(letter_digit, Codes4, Codes5),
    collapse_whitespace(Codes5, Codes6),
    trim_whitespace(Codes6, Codes7),
    atom_codes(Cased, Codes7),
    downcase_atom(Cased, Normal).

expand_ligatures([], []).
expand_ligatures([C|T], Out) :-
    (   ligature(C, Expanded)
    ->  append(Expanded, Tail, Out)
    ;   Out = [C|Tail]
    ),
    expand_ligatures(T, Tail).

fixpoint(Rule, In, Out) :-
    one_pass(Rule, In, Mid),
    (   Mid == In
    ->  Out = In
    ;   fixpoint(Rule, Mid, Out)
    ).

one_pass(_, [], []) :- !.
one_pass(Rule, In, Out) :-
    rewrite(Rule, In, Emitted, Rest),
    !,
    append(Emitted, Tail, Out),
    one_pass(Rule, Rest, Tail).
one_pass(Rule, [C|In], [C|Out]) :-
    one_pass(Rule, In, Out).

% A letter, a hyphen, one or more whitespace characters and a letter lose the
% hyphen and the whitespace.
rewrite(hyphen_break, [A, 0'-|T0], [A, B], T) :-
    ascii_letter(A),
    skip_whitespace(T0, T1),
    T1 \== T0,
    T1 = [B|T],
    ascii_letter(B).
% One whitespace character on either side of a point or comma between digits.
rewrite(spaced_point, [D1|T0], [D1, P, D2], T) :-
    digit_code(D1),
    optional_whitespace(T0, T1),
    T1 = [P|T2],
    point_code(P),
    optional_whitespace(T2, T3),
    T3 = [D2|T],
    digit_code(D2).
% One whitespace character directly between two digits.
rewrite(spaced_digits, [D1, W, D2|T], [D1, D2], T) :-
    digit_code(D1),
    ws_code(W),
    digit_code(D2).
% One whitespace character between a letter and the digit after it. Never the
% other way, so H 2 O becomes H2 O.
rewrite(letter_digit, [L, W, D|T], [L, D], T) :-
    ascii_letter(L),
    ws_code(W),
    digit_code(D).

skip_whitespace([C|T0], T) :- ws_code(C), !, skip_whitespace(T0, T).
skip_whitespace(L, L).

optional_whitespace([C|T], T) :- ws_code(C), !.
optional_whitespace(L, L).

collapse_whitespace([], []).
collapse_whitespace([C|T], Out) :-
    (   ws_code(C)
    ->  skip_whitespace(T, Rest),
        Out = [32|Tail],
        collapse_whitespace(Rest, Tail)
    ;   Out = [C|Tail],
        collapse_whitespace(T, Tail)
    ).

trim_whitespace(In, Out) :-
    drop_leading_space(In, Left),
    reverse(Left, Reversed),
    drop_leading_space(Reversed, Trimmed),
    reverse(Trimmed, Out).

drop_leading_space([C|T], Out) :- code_type(C, space), !, drop_leading_space(T, Out).
drop_leading_space(L, L).

% Substring containment after normalising both sides. A value that normalises
% to nothing is contained in every text.
contains_normalised(Value, NormalText) :-
    normalised(Value, NormalValue),
    (   NormalValue == ''
    ->  true
    ;   sub_atom(NormalText, _, _, _, NormalValue)
    ).

% ---------------------------------------------------------------------
% Exact decimals
%
% A number is n(Mantissa, Scale), worth Mantissa times ten to the minus
% Scale, so every comparison and every plus-or-minus is exact integer
% arithmetic and no float ever decides a refusal.
% ---------------------------------------------------------------------

aligned(n(M1, S1), n(M2, S2), A1, A2, S) :-
    S is max(S1, S2),
    A1 is M1 * 10 ^ (S - S1),
    A2 is M2 * 10 ^ (S - S2).

equal_number(A, B) :- aligned(A, B, X, Y, _), X =:= Y.
greater_number(A, B) :- aligned(A, B, X, Y, _), X > Y.
negative_number(n(M, _)) :- M < 0.
add_number(A, B, n(M, S)) :- aligned(A, B, X, Y, S), M is X + Y.
subtract_number(A, B, n(M, S)) :- aligned(A, B, X, Y, S), M is X - Y.
negate_number(n(M, S), n(N, S)) :- N is -M.

% A slot value as an exact decimal. An integer is itself; a float is read
% from its own shortest round-trip printing, which is the spelling the fact
% was written with.
slot_number(Value, n(Value, 0)) :- integer(Value), !.
slot_number(Value, Number) :-
    float(Value),
    format(atom(Printed), '~w', [Value]),
    atom_codes(Printed, Codes),
    printed_decimal(Codes, Number).

printed_decimal(Codes, Number) :-
    (   Codes = [0'-|Body]
    ->  Negative = true
    ;   Body = Codes,
        Negative = false
    ),
    take_number(Body, Digits, After),
    decimal_of(Digits, n(M0, S0)),
    (   After = [E|Exponent],
        integer(E),
        ( E =:= 0'e ; E =:= 0'E )
    ->  (   Exponent = [0'-|ExponentDigits]
        ->  ExponentSign = -1
        ;   ( Exponent = [0'+|ExponentDigits] -> true ; ExponentDigits = Exponent ),
            ExponentSign = 1
        ),
        number_codes(Power, ExponentDigits),
        S1 is S0 - ExponentSign * Power
    ;   S1 = S0
    ),
    (   Negative == true
    ->  M1 is -M0
    ;   M1 = M0
    ),
    (   S1 < 0
    ->  M is M1 * 10 ^ (-S1), S = 0
    ;   M = M1, S = S1
    ),
    Number = n(M, S).

% A run of digits with an optional single point and one group of digits after
% it. No exponent and no thousands separator, so 1,234 is 1 and 234.
take_number(In, Digits, Rest) :-
    take_digits(In, Whole, After),
    Whole \== [],
    (   After = [P|AfterPoint],
        decimal_point(P),
        take_digits(AfterPoint, Fraction, Tail),
        Fraction \== []
    ->  append(Whole, [46|Fraction], Digits),
        Rest = Tail
    ;   Digits = Whole,
        Rest = After
    ).

take_digits([C|T], [C|Digits], Rest) :- digit_code(C), !, take_digits(T, Digits, Rest).
take_digits(L, [], L).

decimal_of(Digits, n(M, S)) :-
    (   append(Whole, [46|Fraction], Digits)
    ->  append(Whole, Fraction, All),
        length(Fraction, S)
    ;   All = Digits,
        S = 0
    ),
    number_codes(M, All).

% ---------------------------------------------------------------------
% The declared number grammar
%
% Every digit run is a number wherever it sits (the ATTACHED reading), the
% twenty-eight number words are read whole, a ± b yields a, b, a-b and a+b,
% and a bare ± b with no left operand yields the interval from minus b to
% plus b. That last production is the one thing this grammar adds to
% rule-census-01/normalise.py, and equivalence.py names every fixture where
% the two therefore differ.
% ---------------------------------------------------------------------

numbers_of(Raw, Numbers) :-
    normalised(Raw, Normal),
    atom_codes(Normal, Codes),
    token_numbers(Codes, Tokens),
    word_numbers(Codes, Words),
    plus_minus_numbers(Codes, Spreads),
    append([Tokens, Words, Spreads], All),
    sort(All, Numbers).

token_numbers(Codes, Numbers) :- scan_tokens(Codes, none, none, Numbers).

scan_tokens([], _, _, []).
scan_tokens([C|T], Previous, Before, Out) :-
    (   digit_code(C),
        \+ digit_or_point(Previous),
        take_number([C|T], Digits, Rest)
    ->  decimal_of(Digits, Magnitude),
        signed(Previous, Before, Magnitude, Number),
        Out = [Number|Tail],
        last(Digits, LastCode),
        scan_tokens(Rest, LastCode, none, Tail)
    ;   scan_tokens(T, C, Previous, Out)
    ).

% A leading minus is a sign only where it cannot be a range or a hyphen: the
% character before it is neither a digit nor a point.
signed(Previous, Before, n(M, S), Number) :-
    (   sign_code(Previous),
        \+ digit_or_point(Before)
    ->  N is -M,
        Number = n(N, S)
    ;   Number = n(M, S)
    ).

number_word(zero, 0).
number_word(one, 1).
number_word(two, 2).
number_word(three, 3).
number_word(four, 4).
number_word(five, 5).
number_word(six, 6).
number_word(seven, 7).
number_word(eight, 8).
number_word(nine, 9).
number_word(ten, 10).
number_word(eleven, 11).
number_word(twelve, 12).
number_word(thirteen, 13).
number_word(fourteen, 14).
number_word(fifteen, 15).
number_word(sixteen, 16).
number_word(seventeen, 17).
number_word(eighteen, 18).
number_word(nineteen, 19).
number_word(twenty, 20).
number_word(thirty, 30).
number_word(forty, 40).
number_word(fifty, 50).
number_word(sixty, 60).
number_word(seventy, 70).
number_word(eighty, 80).
number_word(ninety, 90).

word_numbers(Codes, Numbers) :- scan_words(Codes, none, Numbers).

scan_words([], _, []).
scan_words([C|T], Previous, Out) :-
    (   number_word(Word, Value),
        atom_codes(Word, WordCodes),
        append(WordCodes, Rest, [C|T]),
        \+ ascii_lower(Previous),
        (   Rest = [Next|_]
        ->  \+ ascii_lower(Next)
        ;   true
        )
    ->  Out = [n(Value, 0)|Tail],
        last(WordCodes, LastCode),
        scan_words(Rest, LastCode, Tail)
    ;   scan_words(T, C, Out)
    ).

plus_minus_numbers(Codes, Numbers) :- scan_plus_minus(Codes, none, none, Numbers).

scan_plus_minus([], _, _, []).
scan_plus_minus(L, Previous, Before, Out) :-
    (   plus_minus_pair(L, Left, Right, Rest, LastCode)
    ->  subtract_number(Left, Right, Low),
        add_number(Left, Right, High),
        Out = [Left, Right, Low, High|Tail],
        scan_plus_minus(Rest, LastCode, none, Tail)
    ;   L = [C|T],
        (   plus_minus_code(C),
            \+ digit_immediately_before(Previous, Before),
            bare_operand(T, Operand)
        ->  negate_number(Operand, Negative),
            Out = [Negative|Tail]
        ;   Out = Tail
        ),
        scan_plus_minus(T, C, Previous, Tail)
    ).

plus_minus_pair(L, Left, Right, Rest, LastCode) :-
    take_number(L, LeftDigits, AfterLeft),
    skip_whitespace(AfterLeft, BeforeSign),
    BeforeSign = [Sign|AfterSign],
    plus_minus_code(Sign),
    skip_whitespace(AfterSign, BeforeRight),
    take_number(BeforeRight, RightDigits, Rest),
    decimal_of(LeftDigits, Left),
    decimal_of(RightDigits, Right),
    last(RightDigits, LastCode).

digit_immediately_before(Previous, _) :- digit_code(Previous), !.
digit_immediately_before(Previous, Before) :- ws_code(Previous), digit_code(Before).

bare_operand(After, Operand) :-
    skip_whitespace(After, Start),
    take_number(Start, Digits, _),
    decimal_of(Digits, Operand).

% ---------------------------------------------------------------------
% Rule (a): two current records state a different value for the same
% quantity of the same subject.
% ---------------------------------------------------------------------

malleus_violation('NO_CONFLICTING_QUANTITY', Code, [A, B]) :-
    subject_pair(A, B),
    quantity_family(Family),
    identity_agrees(Family, A, B),
    value_differs(Family, A, B),
    qualifiers_agree(A, B),
    atom_concat(Family, '_DISAGREEMENT', Code).

subject_pair(A, B) :-
    subject_slot(Slot),
    m_property(A, Slot, Kind, Subject),
    m_property(B, Slot, Kind, Subject),
    A @< B.

identity_agrees(Family, A, B) :-
    forall(
        quantity_identity(Family, Slot),
        (   m_property(A, Slot, Kind, Value),
            m_property(B, Slot, Kind, Value)
        )
    ).

value_differs(Family, A, B) :-
    findall(V, (quantity_value(Family, Slot), stated(A, Slot, V)), Left),
    findall(V, (quantity_value(Family, Slot), stated(B, Slot, V)), Right),
    Left \== Right.

stated(Record, Slot, Value) :-
    (   m_property(Record, Slot, _, Found)
    ->  Value = Found
    ;   Value = absent
    ).

qualifiers_agree(A, B) :-
    forall(
        qualifier(Slot),
        (   findall(V, m_property(A, Slot, _, V), Left),
            findall(V, m_property(B, Slot, _, V), Right),
            Left == Right
        )
    ).

% ---------------------------------------------------------------------
% Rule (b): interval sanity, typed, internal to one record, no text read.
% ---------------------------------------------------------------------

malleus_violation('INTERVAL_SANITY', 'BOUNDS_INVERTED', [Record]) :-
    bound_pair(LowerSlot, UpperSlot),
    numeric_slot(LowerSlot),
    numeric_slot(UpperSlot),
    m_property(Record, LowerSlot, LowerKind, Lower),
    numeric_kind(LowerKind),
    m_property(Record, UpperSlot, UpperKind, Upper),
    numeric_kind(UpperKind),
    slot_number(Lower, LowerNumber),
    slot_number(Upper, UpperNumber),
    greater_number(LowerNumber, UpperNumber).

malleus_violation('INTERVAL_SANITY', Code, [Record]) :-
    non_negative_slot(Slot),
    numeric_slot(Slot),
    m_property(Record, Slot, Kind, Value),
    numeric_kind(Kind),
    slot_number(Value, Number),
    negative_number(Number),
    atomic_list_concat(['NEGATIVE_VALUE', Slot], '/', Code).

numeric_kind(integer).
numeric_kind(float).

% ---------------------------------------------------------------------
% Rule (c): every numeric slot of a citing record carries a number the
% cited sentence states.
% ---------------------------------------------------------------------

cited_text(Record, Text) :-
    m_property(Record, 'assertion_locator', string, Locator),
    Locator \== '',
    m_source_text(_, Locator, Text).

malleus_violation('NUMBER_IN_CITED_TEXT', Code, [Record]) :-
    cited_text(Record, Text),
    numbers_of(Text, Numbers),
    m_property(Record, Slot, Kind, Value),
    numeric_kind(Kind),
    numeric_slot(Slot),
    \+ number_stated(Value, Numbers),
    atomic_list_concat(['NUMBER_NOT_IN_CITED_TEXT', Slot], '/', Code).

number_stated(Value, Numbers) :-
    slot_number(Value, Number),
    member(Stated, Numbers),
    equal_number(Number, Stated),
    !.

% ---------------------------------------------------------------------
% Rule (e): every formula slot of a citing record occurs in the cited
% sentence after the declared normalisation.
% ---------------------------------------------------------------------

malleus_violation('FORMULA_IN_SOURCE', Code, [Record]) :-
    cited_text(Record, Text),
    normalised(Text, NormalText),
    m_property(Record, Slot, string, Value),
    formula_slot(Slot),
    \+ contains_normalised(Value, NormalText),
    atomic_list_concat(['FORMULA_NOT_IN_CITED_TEXT', Slot], '/', Code).
