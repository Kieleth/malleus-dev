%% Toy 3, differential required, over Malleus fact contract version 2.
%%
%% Transcribed from research/domain_reasoning_controls_recon/GEDANKEN.md:318-335.
%% One repair against the sketch: COMPETITOR_NOT_REFUTED reads `entity` where
%% the sketch wrote `event` for TestResult. The sketch typed TestResult as an
%% Event; it is a BearsOn source, and a concrete relation's endpoint ranges
%% must be Entity subtypes, so it is an Entity.
%%
%% Neither rule reads `entered_at`. That is the sketch's own shape, kept, and
%% it is the finding: these rules test provenance shape, never order.

malleus_rule('DIFFERENTIAL_REQUIRED').

malleus_violation('DIFFERENTIAL_REQUIRED', 'SINGLE_HYPOTHESIS', [Dx]) :-
    m_record(Dx, 'Diagnosis', entity),
    m_relation(_, 'ConcludesRelation', Dx, H),
    m_relation(_, 'ExplainsRelation', H, F),
    \+ ( m_record(Other, 'Hypothesis', entity), Other \= H,
         m_relation(_, 'ExplainsRelation', Other, F) ).

malleus_violation('DIFFERENTIAL_REQUIRED', 'COMPETITOR_NOT_REFUTED', [Dx, Other]) :-
    m_record(Dx, 'Diagnosis', entity),
    m_relation(_, 'ConcludesRelation', Dx, H),
    m_relation(_, 'ExplainsRelation', H, F),
    m_record(Other, 'Hypothesis', entity), Other \= H,
    m_relation(_, 'ExplainsRelation', Other, F),
    \+ ( m_record(R, 'TestResult', entity),
         m_relation(_, 'BearsOnRelation', R, Other),
         m_property(R, verdict, string, 'REFUTES') ).
