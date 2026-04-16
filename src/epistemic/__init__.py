"""Epistemic type system for agent outputs."""

from epistemic.classifier import EpistemicClassifier
from epistemic.extractor import PREMISE_MODEL_TRANSCRIPT_ID, ClaimExtractor
from epistemic.llm_client import generate_model_answer, run_llm_pipeline
from epistemic.formatter import OutputFormatter
from epistemic.memory import InMemoryClaimStore, apply_staleness, merge_dependency_closure
from epistemic.models import Claim, EpistemicType, SourceKind, Violation
from epistemic.pipeline import PipelineResult, run_pipeline
from epistemic.rules import RuleEngine
from epistemic.serde import (
    claim_from_jsonable,
    claim_to_jsonable,
    dumps_pipeline_result,
    loads_pipeline_result,
    pipeline_result_from_jsonable,
    pipeline_result_to_jsonable,
    violation_from_jsonable,
    violation_to_jsonable,
)

__all__ = [
    "Claim",
    "ClaimExtractor",
    "claim_from_jsonable",
    "claim_to_jsonable",
    "dumps_pipeline_result",
    "EpistemicClassifier",
    "generate_model_answer",
    "EpistemicType",
    "InMemoryClaimStore",
    "loads_pipeline_result",
    "merge_dependency_closure",
    "OutputFormatter",
    "pipeline_result_from_jsonable",
    "pipeline_result_to_jsonable",
    "PipelineResult",
    "PREMISE_MODEL_TRANSCRIPT_ID",
    "RuleEngine",
    "SourceKind",
    "Violation",
    "violation_from_jsonable",
    "violation_to_jsonable",
    "apply_staleness",
    "run_llm_pipeline",
    "run_pipeline",
]
