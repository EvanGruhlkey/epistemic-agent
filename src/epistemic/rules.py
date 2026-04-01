from __future__ import annotations

"""
Runtime policy for first-class epistemic types (not prompt styling).

Core constraints reflected here:

- **Assumptions / user hearsay / inference** are not promoted to world-factual presentation
  (:func:`_strong_enough_for_factual`, ``presentation == "factual"``).
- **Estimates** must carry uncertainty metadata on every estimate claim.
- **Stale** rows must record a refresh before use (``metadata["refreshed"]``).
- **Inferred** segments must declare premise claim ids (``dependencies``), unless explicitly waived.
"""

from collections.abc import Callable, Iterable

from epistemic.models import Claim, EpistemicType, Violation

PresentationCheck = Callable[[dict[str, Claim]], list[Violation]]

_FACTUAL = "factual"


def _strong_enough_for_factual(c: Claim) -> bool:
    """World-facing factual presentation: not user hearsay, not inference, assumptions, or stale."""
    if c.epistemic_type in (EpistemicType.OBSERVED, EpistemicType.RETRIEVED):
        return True
    if c.epistemic_type is EpistemicType.ESTIMATED:
        return _has_uncertainty_marker(c)
    return False


def _has_uncertainty_marker(c: Claim) -> bool:
    return bool(c.metadata.get("uncertainty_disclosed") or c.metadata.get("uncertainty_marked"))


def _rule_inferred_requires_premises(indexed: dict[str, Claim]) -> list[Violation]:
    """Inferred claims must cite supporting premises (dependency ids), unless explicitly waived."""
    out: list[Violation] = []
    for c in indexed.values():
        if c.epistemic_type is not EpistemicType.INFERRED:
            continue
        if c.metadata.get("inference_without_premises_allowed"):
            continue
        if not c.dependencies:
            out.append(
                Violation(
                    "inferred_requires_premises",
                    c.id,
                    "inferred claims must list premise claim ids in dependencies",
                )
            )
    return out


def _rule_estimated_must_mark_uncertainty(indexed: dict[str, Claim]) -> list[Violation]:
    """Estimates must carry uncertainty disclosure metadata (or text markers via uncertainty_marked)."""
    out: list[Violation] = []
    for c in indexed.values():
        if c.epistemic_type is not EpistemicType.ESTIMATED:
            continue
        if _has_uncertainty_marker(c):
            continue
        out.append(
            Violation(
                "estimated_requires_uncertainty_marker",
                c.id,
                "estimates must set metadata uncertainty_disclosed or uncertainty_marked",
            )
        )
    return out


def _rule_stale_must_be_refreshed(indexed: dict[str, Claim]) -> list[Violation]:
    """Stale rows cannot be used until refresh is recorded (re-fetch or operator ack)."""
    out: list[Violation] = []
    for c in indexed.values():
        if c.epistemic_type is not EpistemicType.STALE:
            continue
        if c.metadata.get("refreshed"):
            continue
        out.append(
            Violation(
                "stale_requires_refresh",
                c.id,
                "stale claims must be refreshed (set metadata refreshed=True after revalidation) before use",
            )
        )
    return out


def _rule_factual_top_claim(indexed: dict[str, Claim]) -> list[Violation]:
    """Claims marked for factual presentation must be epistemically strong enough (see _strong_enough_for_factual)."""
    out: list[Violation] = []
    for c in indexed.values():
        if c.metadata.get("presentation") != _FACTUAL:
            continue
        if not _strong_enough_for_factual(c):
            out.append(
                Violation(
                    "factual_requires_observed_or_retrieved",
                    c.id,
                    f"factual presentation requires observed, retrieved, or disclosed estimate; got {c.epistemic_type.value}",
                )
            )
    return out


def _rule_factual_dependency_chain(indexed: dict[str, Claim]) -> list[Violation]:
    """Factual claims may not depend on weak epistemic types."""
    out: list[Violation] = []
    for c in indexed.values():
        if c.metadata.get("presentation") != _FACTUAL:
            continue
        for dep_id in c.dependencies:
            dep = indexed.get(dep_id)
            if dep is None:
                continue
            if not _strong_enough_for_factual(dep):
                out.append(
                    Violation(
                        "factual_requires_strong_dependencies",
                        c.id,
                        f"factual claim depends on {dep_id!r} ({dep.epistemic_type.value})",
                    )
                )
    return out


def _rule_unresolved_dependencies(indexed: dict[str, Claim]) -> list[Violation]:
    """Every dependency id must refer to a claim in the batch."""
    out: list[Violation] = []
    for c in indexed.values():
        for dep_id in c.dependencies:
            if dep_id not in indexed:
                out.append(
                    Violation(
                        "unresolved_dependency",
                        c.id,
                        f"unknown dependency claim id {dep_id!r}",
                    )
                )
    return out


_DEFAULT_RULES: tuple[PresentationCheck, ...] = (
    _rule_inferred_requires_premises,
    _rule_estimated_must_mark_uncertainty,
    _rule_stale_must_be_refreshed,
    _rule_factual_top_claim,
    _rule_factual_dependency_chain,
    _rule_unresolved_dependencies,
)


class RuleEngine:
    """Runs ordered policy checks over a set of claims."""

    def __init__(self, rules: Iterable[PresentationCheck] | None = None) -> None:
        self._rules: tuple[PresentationCheck, ...] = (
            tuple(rules) if rules is not None else _DEFAULT_RULES
        )

    def evaluate(self, claims: Iterable[Claim]) -> list[Violation]:
        indexed = {c.id: c for c in claims}
        violations: list[Violation] = []
        for rule in self._rules:
            violations.extend(rule(indexed))
        return violations
