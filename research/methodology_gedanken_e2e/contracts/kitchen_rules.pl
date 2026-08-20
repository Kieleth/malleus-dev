%% Toy 1, mise en place, over Malleus fact contract version 2.
%%
%% Transcribed from research/domain_reasoning_controls_recon/GEDANKEN.md:98-109.
%% One repair against the sketch: the third argument of m_record/3 reads
%% `entity`, not `event`. The sketch typed the steps as Events; a concrete
%% relation's endpoint ranges must be Entity subtypes, so the steps are
%% Entities and the compiler emits `entity` as their kind.

malleus_rule('MISE_EN_PLACE').

malleus_violation('MISE_EN_PLACE', 'UNPREPARED_INGREDIENT', [Combine, Ing]) :-
    m_record(Combine, 'CombineStep', entity),
    m_relation(_, 'UsesRelation', Combine, Ing),
    m_property(Combine, step_index, integer, CIdx),
    \+ ( m_record(Prep, 'PrepStep', entity),
         m_relation(_, 'UsesRelation', Prep, Ing),
         m_property(Prep, step_index, integer, PIdx),
         PIdx < CIdx ).
