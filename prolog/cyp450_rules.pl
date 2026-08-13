%% Trusted local CYP450 rules over the generic Malleus fact vocabulary.
%%
%% The compiler supplies:
%%   m_record(RecordId, ConcreteType, Kind).
%%   m_relation(RecordId, ConcreteType, SourceId, TargetId).
%%   m_property(RecordId, Property, ScalarKind, Value).
%%
%% The verifier requires these fixed entrypoints:
%%   malleus_rule(RuleId).
%%   malleus_violation(RuleId, ViolationCode, WitnessRecordIds).

malleus_rule('CYP450_INHIBITOR_INDUCER_CONFLICT').

malleus_violation(
    'CYP450_INHIBITOR_INDUCER_CONFLICT',
    'INHIBITOR_AND_INDUCER',
    [InhibitsRelationId, InducesRelationId]
) :-
    m_relation(InhibitsRelationId, 'InhibitsRelation', DrugId, EnzymeId),
    m_property(InhibitsRelationId, 'inhibition_strength', 'string', 'STRONG'),
    m_relation(InducesRelationId, 'InducesRelation', DrugId, EnzymeId),
    m_property(InducesRelationId, 'inhibition_strength', 'string', 'STRONG'),
    InhibitsRelationId \= InducesRelationId.
