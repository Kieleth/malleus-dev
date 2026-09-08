malleus_rule('ONE_SHIPMENT_PER_UNIT').
malleus_violation('ONE_SHIPMENT_PER_UNIT', 'UNIT_ASSIGNED_TWICE', [A, B, Unit]) :-
    m_relation(A, 'ShipmentContainsUnit', First, Unit),
    m_relation(B, 'ShipmentContainsUnit', Second, Unit),
    First @< Second.
