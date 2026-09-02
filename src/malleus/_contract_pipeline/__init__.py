"""Private binding-to-validated-fact compiler boundary."""

from .model import (
    ArtifactRefusal,
    ArtifactRefusalReason,
    EffectiveConstraints,
    ElaboratedAlternative,
    ElaboratedClass,
    ElaboratedCondition,
    ElaboratedContract,
    ElaboratedEnum,
    ElaboratedExpressionGroup,
    ElaboratedScalar,
    ElaboratedSlot,
    ElaboratedSlotUse,
    ElaborationRefusal,
    ElaborationRefusalReason,
    ValidatedContractArtifact,
    ValidatedContractCompilation,
)
from .view import ContractView, load_validated_contract_artifact


def compile_binding(binding):
    """Elaboration is supplied by the adjacent implementation module."""

    from .elaborate import compile_binding as implementation

    return implementation(binding)


__all__ = [
    "ArtifactRefusal",
    "ArtifactRefusalReason",
    "ContractView",
    "EffectiveConstraints",
    "ElaboratedAlternative",
    "ElaboratedClass",
    "ElaboratedCondition",
    "ElaboratedContract",
    "ElaboratedEnum",
    "ElaboratedExpressionGroup",
    "ElaboratedScalar",
    "ElaboratedSlot",
    "ElaboratedSlotUse",
    "ElaborationRefusal",
    "ElaborationRefusalReason",
    "ValidatedContractArtifact",
    "ValidatedContractCompilation",
    "compile_binding",
    "load_validated_contract_artifact",
]
