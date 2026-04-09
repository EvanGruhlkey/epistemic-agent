from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

from epistemic.classifier import EpistemicClassifier
from epistemic.extractor import ClaimExtractor
from epistemic.formatter import OutputFormatter
from epistemic.memory import InMemoryClaimStore, merge_dependency_closure
from epistemic.models import Claim, Violation, utc_now
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
    store: InMemoryClaimStore | None = None,
    persist_on_ok: bool = False,
    resolve_dependencies_from_store: bool = False,
) -> PipelineResult:
    """
    raw LLM (or tool) text -> structured claims -> classify -> optional factual gate -> rules -> text.

    If ``store`` is set and ``persist_on_ok`` is True, successful runs are written to the store.

    If ``resolve_dependencies_from_store`` is True, the rule engine also sees dependency claims
    loaded from ``store`` (staleness applied); formatted output still uses only the extracted batch.
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

    evaluation_claims: list[Claim] = claims_list
    if store is not None and resolve_dependencies_from_store:
        evaluation_claims = merge_dependency_closure(claims_list, store, now=utc_now())

    claims = tuple(claims_list)
    violations_list = eng.evaluate(evaluation_claims)
    violations = tuple(violations_list)

    if violations_list:
        withheld_ids = {v.claim_id for v in violations_list}
        shown_list = [c for c in claims_list if c.id not in withheld_ids]
        if (
            presentation_mode == "factual"
            and shown_list
            and len(shown_list) < len(claims_list)
        ):
            body = fmt.format(shown_list)
            footer_lines = "\n".join(
                f"  - [{v.claim_id}] ({v.rule_id}) {v.message}" for v in violations_list
            )
            text = (
                f"{body}\n\n---\n"
                "The following were not asserted as fact under factual mode:\n"
                f"{footer_lines}"
            )
            return PipelineResult(claims, violations, text, False)

        return PipelineResult(claims, violations, fmt.format_blocked(violations_list), False)

    if store is not None and persist_on_ok:
        store.put_all(claims_list)

    return PipelineResult(claims, violations, fmt.format(claims_list), True)
