%% Toy 2, provenance pattern, over Malleus fact contract version 2.
%%
%% Transcribed from research/domain_reasoning_controls_recon/GEDANKEN.md:210-232.
%% One repair against the sketch: MISSING_RISK_STAGE reads `entity` where the
%% sketch wrote `signal`. The sketch typed RiskAssessment as a Signal; a
%% concrete relation's endpoint ranges must be Entity subtypes and
%% RiskAssessment is a DerivedFrom endpoint, so it is an Entity and the
%% compiler emits `entity` as its kind.
%%
%% SUPPORT_POSTDATES_CONCLUSION compares two writer-supplied strings. That is
%% the whole point of the toy: it checks the analyst's honesty about order,
%% not the order.

malleus_rule('PROVENANCE_PATTERN').

malleus_violation('PROVENANCE_PATTERN', 'MISSING_RISK_STAGE', [Rec]) :-
    m_record(Rec, 'Recommendation', entity),
    \+ ( m_relation(_, 'DerivedFromRelation', Rec, K),
         m_record(K, 'RiskAssessment', entity) ).

malleus_violation('PROVENANCE_PATTERN', 'SUPPORT_POSTDATES_CONCLUSION', [Rec, K]) :-
    m_record(Rec, 'Recommendation', entity),
    m_relation(_, 'DerivedFromRelation', Rec, K),
    m_property(Rec, asserted_at, string, RT),
    m_property(K,   asserted_at, string, KT),
    KT @> RT.
