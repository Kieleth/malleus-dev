# Real check execution, before ledger submission

The TYPE and direct-grant reference producers now execute finite predicates.
`check-rules.json` names the predicates and contains their existing instruction
sequences. Python binds exact inputs, executes those instructions and assembles
the existing output records using the previously defined field-origin census.
No goal, supplier rule, robotics rule or final policy verdict is introduced.

`load_check_executor()` reads the local implementation resources once. The
result's `execute` method receives only explicit invocation metadata, supplied
full records, supplied retained bytes and the compiled record contract. It has
no clock, writer, source store, callback or external capability. Its source
capsule contains the actual producer, instruction executor, definition checker
and control adapter code. The monitor must bind this capsule and the complete
definition bytes as real SourceArtifacts. A specification or arbitrary byte
string cannot stand in for the implementation. Core and Python dependencies
remain separately identified runtime dependencies, not embedded in the capsule.

Input and provenance closure order is invocation role order, then monitor ID,
then the monitor's canonical static-input order, retaining the first occurrence
of an ID. Scalars are not disguised as artifact IDs. Failure output comes first;
the unavailable assessment additionally cites that failure. Output metadata and
IDs are explicit, distinct and unused. Source byte, source semantic and record
hashes remain separate.

The producer instantiates closed operand shapes from this invocation solely for
the finite path checker. These generated shapes do not infer domain validity
from an example. TYPE executes VALIDATE_RECORD against the complete separately
compiled ontology, including additional fields on concrete action subclasses.
A known type violation yields VIOLATED. Wrong identities, absent bytes,
malformed invocation or an unsupported instruction refuse instead of becoming
a scientific or permission judgment. A genuine engine exception produces the
existing paired MonitorFailure and unavailable assessment with UNKNOWN.

Direct-grant predicates check grantee, permitted action type, grant-to-scope
association, exact scope ID/hash equality, no subdelegation and requested
interval containment. Known mismatches produce VIOLATED and retain the exact
grant actually checked. Grantor legitimacy and scope hierarchy are not proved.

The owning-history work must preserve the accepted external-design contract:
monitor invocation is explicit and outside append/replay. Replay verifies the
recorded closure and recomputes control from recorded outcomes. It does not
invoke these producers again. This distinction also permits a retained genuine
unavailability record to replay after a checker recovers. Tests that inject an
engine failure exercise this branch, not physical checker unavailability.

These are pure computation results over supplied inputs. They explicitly say
`history_authenticated: false`. They are not admitted records, permission,
dispatch, world-state observations, portable execution or an E2E handoff. The
next integration owns authenticated prefix resolution, registration, complete
event programs and failure-atomic persistence in KnowledgeChangeHistory.
