from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

from epistemic.classifier import EpistemicClassifier
from epistemic.extractor import ClaimExtractor
from epistemic.formatter import OutputFormatter
from epistemic.models import Claim, Violation
from epistemic.rules import RuleEngine

PresentationMode = Literal["factual", "transparent"]


@dataclass(frozen=True, slots=True)
class PipelineResult:
    claims: tuple[Claim, ...]
    violations: tuple[Violation, ...]
    output_text: str
    ok: bool


def run_pipeline(
    raw_text: str,
    *,
    presentation_mode: PresentationMode = "transparent",
    extractor: ClaimExtractor | None = None,
    classifier: EpistemicClassifier | None = None,
    rules: RuleEngine | None = None,
    formatter: OutputFormatter | None = None,
) -> PipelineResult:
    """
    raw LLM (or tool) text → structured claims → classify → optional factual gate → rules → text.
    """
    ex = extractor or ClaimExtractor()
    clf = classifier or EpistemicClassifier()
    eng = rules or RuleEngine()
    fmt = formatter or OutputFormatter()

    claims_list = [clf.classify(c) for c in ex.extract(raw_text)]

    if presentation_mode == "factual":
        claims_list = [
            replace(c, metadata={**c.metadata, "presentation": "factual"}) for c in claims_list
        ]

    claims = tuple(claims_list)
    violations_list = eng.evaluate(claims)
    violations = tuple(violations_list)

    if violations_list:
        return PipelineResult(claims, violations, fmt.format_blocked(violations_list), False)

    return PipelineResult(claims, violations, fmt.format(claims_list), True)
