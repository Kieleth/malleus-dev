malleus_rule('NO_CONFLICTING_QUANTITY').
malleus_rule('NO_EMPTY_RECORD').

% Two current records state a different quantity for the same order and product.
% The subject is the order reference, the quantity is named by product_code, and
% the value kind is shared so a representation difference is never a conflict.
malleus_violation('NO_CONFLICTING_QUANTITY', 'QUANTITY_DISAGREEMENT', [A, B]) :-
    m_property(A, 'order_id', SubjectKind, Subject),
    m_property(B, 'order_id', SubjectKind, Subject),
    A @< B,
    m_property(A, 'product_code', ProductKind, Product),
    m_property(B, 'product_code', ProductKind, Product),
    m_property(A, 'ordered_quantity', QuantityKind, QuantityA),
    m_property(B, 'ordered_quantity', QuantityKind, QuantityB),
    QuantityA \== QuantityB.

% A record of any kind carries no property at all.
malleus_violation('NO_EMPTY_RECORD', 'RECORD_WITHOUT_PROPERTIES', [Record]) :-
    m_record(Record, _, _),
    \+ m_property(Record, _, _, _).
