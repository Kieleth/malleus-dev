# Exact Assent compiler compatibility

Operator-approved scope: a REFERENCE_IMPLEMENTATION repair within the optional
compiler-enabled profile. The tests are CONFORMANCE_FIXTURE evidence, not action
execution or base protocol rules. Work is isolated from shared main.

Claim: compile the exact shipped Assent import closure and its neutral
LocalAction import, retain the distinct date range, reload the resulting
artifact, and structurally validate selected action/assessment records.

Observation: positive imports, calendar-date and record negatives, class-level
ValidTime alternatives, source-free artifact reload, and unchanged Shop facts.
Reuse the existing binder, elaborator, identified metamodel, artifact reader,
and structural view. Date keeps its already-bound LinkML type IRI. Its current
string representation is a real YYYY-MM-DD calendar date, as in the pinned
LinkML XSDDate validator and Assent ValidTime's canonical calendar carrier.
No implicit conversion or normalization is introduced.

The previous metamodel explicitly permits five primitive targets. Date support
must therefore identify an exact additive metamodel extension when date is used,
not change the meaning of old identities. Non-date artifacts keep their existing
metamodel. Runtime validation must not require LinkML or a source checkout.

Dependencies: AssentCompatibility consumes ExactAssentClosure; Compiler produces
ValidatedContractArtifact; ContractView consumes ValidatedContractArtifact;
AssentCompatibility conformsTo test_assent_contract_compatibility.py.

Excluded: ontology edits, general scalar expansion, action runtime/interpreter,
policy expansion, executor, observer, substitute records, shared-main
integration, governance append, package/version change, and remote publication.
If another unsupported semantic feature appears on recompiling the complete
closure, report it before broadening this repair.

The predecessor README and snapshot tests describe commit 28cd4b7 only. They
remain historical evidence, not the acceptance suite for this successor.
