from __future__ import annotations

from collections.abc import Callable, Iterable

from epistemic.models import Claim, EpistemicType, Violation

PresentationCheck = Callable[[dict[str, Claim]], list[Violation]]

_FACTUAL = "factual"
_ALLOWED_FOR_FACTUAL = frozenset({EpistemicType.OBSERVED, EpistemicType.RETRIEVED})


def _rule_factual_top_claim(indexed: dict[str, Claim]) -> list[Violation]:
    """Claims marked for factual presentation must be observed or retrieved only."""
    out: list[Violation] = []
    for c in indexed.values():
        if c.metadata.get("presentation") != _FACTUAL:
            continue
        if c.epistemic_type not in _ALLOWED_FOR_FACTUAL:
            out.append(
                Violation(
                    "factual_requires_observed_or_retrieved",
                    c.id,
                    f"factual presentation requires observed or retrieved type; got {c.epistemic_type.value}",
                )
            )
    return out


def _rule_factual_dependency_chain(indexed: dict[str, Claim]) -> list[Violation]:
    """Factual claims may not depend on non-factual epistemic types."""
    out: list[Violation] = []
    for c in indexed.values():
        if c.metadata.get("presentation") != _FACTUAL:
            continue
        for dep_id in c.dependencies:
            dep = indexed.get(dep_id)
            if dep is None:
                continue
            if dep.epistemic_type not in _ALLOWED_FOR_FACTUAL:
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
