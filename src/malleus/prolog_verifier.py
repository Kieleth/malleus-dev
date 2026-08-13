"""Process-isolated SWI-Prolog execution for generic Malleus graph facts."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from malleus.kg import KnowledgeGraph
from malleus.logic import (
    GraphFactCompiler,
    LogicContract,
    LogicError,
    LogicExecutionError,
    LogicCheckResult,
    Violation,
    fact_declarations,
)
from malleus.staging import CandidateSubgraph


RESULT_FIELDS = {"rules", "violations", "version"}
VIOLATION_FIELDS = {"rule_id", "violation_code", "witnesses"}
RUNNER = r"""
:- use_module(library(http/json)).
:- initialization(malleus_main).
malleus_main :-
    findall(RuleId, malleus_rule(RuleId), Rules),
    findall(
        _{rule_id:RuleId, violation_code:ViolationCode, witnesses:WitnessRecordIds},
        malleus_violation(RuleId, ViolationCode, WitnessRecordIds),
        Violations
    ),
    current_prolog_flag(version, Version),
    json_write_dict(
        current_output,
        _{rules:Rules, violations:Violations, version:Version},
        [width(0)]
    ),
    nl,
    halt.
"""


class PrologVerifier:
    """Evaluate a trusted pinned rule set in one fresh process per check."""

    def __init__(self, contract: LogicContract):
        if not isinstance(contract, LogicContract):
            raise TypeError("PrologVerifier requires a LogicContract")
        contract.validate_integrity()
        self.contract = contract
        self._compiler = GraphFactCompiler()

    @classmethod
    def from_contract(cls, path: str) -> "PrologVerifier":
        return cls(LogicContract.load(path))

    def verify_candidate_subgraph(
        self,
        candidate: CandidateSubgraph,
        *context: KnowledgeGraph,
    ) -> LogicCheckResult:
        """Enumerate all declared violations over context plus the candidate."""
        self.contract.validate_integrity()
        if not isinstance(candidate, CandidateSubgraph):
            raise TypeError("candidate must be a CandidateSubgraph")
        overlay = candidate.overlay()
        compiled = self._compiler.compile(*context, overlay)
        if compiled.ontology_hash != candidate.ontology_hash:
            raise LogicError("Compiled facts and candidate use different ontologies")
        if compiled.ontology_hash != self.contract.ontology_hash:
            raise LogicError("Logic contract and compiled facts use different ontologies")

        execution = self._execute(compiled.facts)
        declared = {
            _ground_string(value, "declared rule ID")
            for value in execution["rules"]
        }
        if declared != set(self.contract.rule_ids):
            raise LogicExecutionError(
                "Rules file declaration differs from the pinned logic contract"
            )
        violations = self._violations(
            execution["violations"],
            declared,
            set(compiled.record_ids),
        )
        context_count = len(context)
        return LogicCheckResult(
            candidate_digest=candidate.candidate_digest,
            base_state_digest=candidate.base_state_digest,
            candidate_state_digest=candidate.candidate_state_digest,
            context_state_digests=tuple(sorted(set(compiled.state_digests[:context_count]))),
            ontology_hash=compiled.ontology_hash,
            fact_contract_version=self.contract.fact_contract_version,
            contract_id=self.contract.contract_id,
            contract_version=self.contract.contract_version,
            contract_hash=self.contract.contract_hash,
            ruleset_id=self.contract.ruleset_id,
            ruleset_version=self.contract.ruleset_version,
            ruleset_hash=self.contract.ruleset_hash,
            engine_name="SWI-Prolog",
            engine_version=_engine_version(execution["version"]),
            timeout_seconds=self.contract.timeout_seconds,
            facts_hash=compiled.facts_hash,
            fact_count=len(compiled.facts),
            translated_record_ids=compiled.record_ids,
            checked_rule_ids=tuple(sorted(self.contract.rule_ids)),
            violations=violations,
        )

    def _execute(self, facts: tuple[str, ...]) -> dict:
        executable = shutil.which("swipl")
        if executable is None:
            raise LogicExecutionError("SWI-Prolog executable 'swipl' is not available")
        program = (
            ":- set_prolog_flag(character_escapes, true).\n"
            + fact_declarations()
            + "\n"
            + "\n".join(f"{fact}." for fact in facts)
            + "\n"
            + RUNNER
            + "\n"
            + self.contract.rules_source.rstrip()
            + "\n"
        )
        try:
            with tempfile.TemporaryDirectory(prefix="malleus-logic-") as directory:
                path = Path(directory) / "check.pl"
                path.write_text(program, encoding="utf-8")
                completed = subprocess.run(
                    [executable, "-q", "-f", str(path)],
                    capture_output=True,
                    text=True,
                    timeout=self.contract.timeout_seconds,
                    check=False,
                )
        except subprocess.TimeoutExpired as error:
            raise LogicExecutionError(
                f"Logic check exceeded {self.contract.timeout_seconds} seconds"
            ) from error
        except (OSError, UnicodeError) as error:
            raise LogicExecutionError(f"Logic engine execution failed: {error}") from error
        if completed.returncode != 0:
            detail = completed.stderr.strip() or "no error detail"
            raise LogicExecutionError(
                f"Logic engine exited with status {completed.returncode}: {detail}"
            )
        output = completed.stdout.strip()
        if not output:
            detail = completed.stderr.strip() or "no error detail"
            raise LogicExecutionError(
                f"Logic engine emitted no JSON result: {detail}"
            )
        try:
            result = json.loads(output)
        except json.JSONDecodeError as error:
            raise LogicExecutionError(f"Logic engine emitted invalid JSON: {error}") from error
        _exact_result(result, RESULT_FIELDS, "logic engine result")
        if not isinstance(result["rules"], list) or not isinstance(result["violations"], list):
            raise LogicExecutionError("Logic engine rules and violations must be lists")
        return result

    @staticmethod
    def _violations(
        results: list,
        declared_rules: set[str],
        record_ids: set[str],
    ) -> tuple[Violation, ...]:
        violations = set()
        for index, result in enumerate(results):
            _exact_result(result, VIOLATION_FIELDS, f"violation {index}")
            rule_id = _ground_string(result["rule_id"], "violation rule ID")
            if rule_id not in declared_rules:
                raise LogicExecutionError(f"Violation returned undeclared rule ID '{rule_id}'")
            code = _ground_string(result["violation_code"], "violation code")
            witness_values = result["witnesses"]
            if not isinstance(witness_values, list) or not witness_values:
                raise LogicExecutionError("Violation witnesses must be a nonempty proper list")
            witnesses = tuple(
                _ground_string(value, "violation witness record ID")
                for value in witness_values
            )
            if len(witnesses) != len(set(witnesses)):
                raise LogicExecutionError("Violation witness record IDs must be unique")
            unknown = sorted(set(witnesses) - record_ids)
            if unknown:
                raise LogicExecutionError(
                    f"Violation returned unknown witness record ID '{unknown[0]}'"
                )
            violations.add(Violation(rule_id, code, tuple(sorted(witnesses))))
        return tuple(sorted(violations))


def _exact_result(value, expected: set[str], context: str) -> None:
    if not isinstance(value, dict):
        raise LogicExecutionError(f"{context} must be an object")
    missing = sorted(expected - set(value))
    unknown = sorted(set(value) - expected)
    if missing or unknown:
        raise LogicExecutionError(
            f"{context} fields differ, missing={missing}, unknown={unknown}"
        )


def _ground_string(value, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LogicExecutionError(f"{context} must be a nonblank ground string")
    return value


def _engine_version(value) -> str:
    if not isinstance(value, (str, int)) or isinstance(value, bool):
        raise LogicExecutionError("engine version must be a string or integer")
    text = str(value)
    if not text.strip():
        raise LogicExecutionError("engine version must be nonblank")
    return text
