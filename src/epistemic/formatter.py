from __future__ import annotations

from collections.abc import Sequence

from epistemic.models import Claim, EpistemicType, Violation


class OutputFormatter:
    """User-facing text with epistemic transparency (no HTML/UI)."""

    def format(self, claims: Sequence[Claim]) -> str:
        lines = [_format_claim_line(c) for c in claims]
        return "\n\n".join(lines) if lines else ""

    def format_blocked(self, violations: Sequence[Violation]) -> str:
        if not violations:
            return "[epistemic policy] Output blocked (no details)."
        body = "\n".join(f"  - {v.rule_id} [{v.claim_id}]: {v.message}" for v in violations)
        return "[epistemic policy] Output blocked:\n" + body


def _format_claim_line(c: Claim) -> str:
    label = _label_for(c.epistemic_type)
    conf = f" (confidence {c.confidence:.0%})" if c.confidence < 1.0 else ""
    return f"{label}{conf}\n{c.text.strip()}"


def _label_for(t: EpistemicType) -> str:
    return {
        EpistemicType.OBSERVED: "[observed]",
        EpistemicType.RETRIEVED: "[retrieved]",
        EpistemicType.INFERRED: "[inferred - not verified]",
        EpistemicType.ASSUMED: "[assumption]",
        EpistemicType.ESTIMATED: "[estimate]",
        EpistemicType.USER_STATED: "[user stated - not verified]",
        EpistemicType.STALE: "[may be outdated - refresh before relying]",
    }[t]
