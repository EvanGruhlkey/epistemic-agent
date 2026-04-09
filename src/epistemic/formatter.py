from __future__ import annotations

from collections.abc import Sequence

from epistemic.models import Claim, EpistemicType, Violation


class OutputFormatter:
    """User-facing text with epistemic transparency (no HTML/UI)."""

    def format(self, claims: Sequence[Claim]) -> str:
        blocks = [_format_claim_block(c) for c in claims]
        return "\n\n".join(blocks) if blocks else ""

    def format_blocked(self, violations: Sequence[Violation]) -> str:
        if not violations:
            return "No output was produced: policy checks reported no details."
        body = "\n".join(f"  - {v.rule_id} [{v.claim_id}]: {v.message}" for v in violations)
        return (
            "Output withheld pending policy:\n"
            f"{body}\n"
            "Tune presentation mode, premises, or metadata, then retry."
        )


def _confidence_sentence(c: Claim) -> str:
    if c.confidence >= 1.0:
        return ""
    return f" Stated confidence: {c.confidence:.0%}."


def _format_claim_block(c: Claim) -> str:
    prose = _prose_for_type(c.epistemic_type)
    conf = _confidence_sentence(c)
    return f"{prose}{conf}\n\n{c.text.strip()}"


def _prose_for_type(t: EpistemicType) -> str:
    return {
        EpistemicType.OBSERVED: (
            "This claim reflects a direct tool or API result (as reported to the system)."
        ),
        EpistemicType.RETRIEVED: (
            "This claim was retrieved from a source and is reproduced here as given."
        ),
        EpistemicType.INFERRED: "This claim is inferred and has not been verified.",
        EpistemicType.ASSUMED: (
            "This is a working assumption for the rest of the reasoning; not an established fact."
        ),
        EpistemicType.ESTIMATED: "Estimated from incomplete information.",
        EpistemicType.USER_STATED: (
            "This reflects what the user stated; it has not been independently verified."
        ),
        EpistemicType.STALE: (
            "This information may be outdated; refresh or re-validate before relying on it."
        ),
    }[t]
