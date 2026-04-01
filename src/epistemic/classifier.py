from __future__ import annotations

from dataclasses import replace
from typing import Any

from epistemic.models import Claim, EpistemicType, SourceKind


class EpistemicClassifier:
    """
    Assigns or refines epistemic_type from source and optional extractor hints.

    Explicit ``metadata["epistemic_hint"]`` (a member name or value of
    :class:`EpistemicType`) wins over heuristics.
    """

    def classify(self, claim: Claim) -> Claim:
        hinted = _coerce_epistemic_hint(claim.metadata.get("epistemic_hint"))
        if hinted is not None:
            return replace(claim, epistemic_type=hinted)

        et = _default_type_for_source(claim.source)
        return replace(claim, epistemic_type=et)


def _coerce_epistemic_hint(raw: Any) -> EpistemicType | None:
    if raw is None:
        return None
    if isinstance(raw, EpistemicType):
        return raw
    if isinstance(raw, str):
        try:
            return EpistemicType(raw.lower())
        except ValueError:
            pass
        try:
            return EpistemicType[raw.upper()]
        except KeyError:
            return None
    return None


def _default_type_for_source(source: SourceKind) -> EpistemicType:
    if source in (SourceKind.TOOL, SourceKind.DOCUMENT):
        return EpistemicType.RETRIEVED
    if source is SourceKind.USER:
        return EpistemicType.OBSERVED
    if source in (SourceKind.MODEL, SourceKind.INFERENCE, SourceKind.UNKNOWN):
        return EpistemicType.INFERRED
    if source is SourceKind.SYSTEM:
        return EpistemicType.ASSUMED
    return EpistemicType.INFERRED
