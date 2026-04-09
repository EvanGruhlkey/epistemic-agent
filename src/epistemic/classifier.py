from __future__ import annotations

import re
from dataclasses import replace
from typing import Any

from epistemic.models import Claim, EpistemicType, SourceKind


class EpistemicClassifier:
    """
    Assigns ``epistemic_type`` from :class:`SourceKind`, metadata, and light heuristics.

    Intended mapping:

    - **TOOL** — direct tool/API payload → :attr:`~EpistemicType.OBSERVED`
    - **DOCUMENT** — text from corpus / cited doc → :attr:`~EpistemicType.RETRIEVED`
    - **MODEL** / **INFERENCE** — model or deduction step (often with ``dependencies``) → :attr:`~EpistemicType.INFERRED`
    - **USER** — user-supplied assertion (e.g. budget) → :attr:`~EpistemicType.USER_STATED`
    - **SYSTEM** — orchestration default → :attr:`~EpistemicType.ASSUMED`

    **STALE** / **ESTIMATED** are usually set via metadata or upstream extractors; heuristics below are opt-in.
    """

    def classify(self, claim: Claim) -> Claim:
        hinted = _coerce_epistemic_hint(claim.metadata.get("epistemic_hint"))
        if hinted is not None:
            return replace(claim, epistemic_type=hinted)

        if claim.metadata.get("classify_as_stale") or claim.metadata.get("timestamp_stale"):
            return replace(claim, epistemic_type=EpistemicType.STALE)

        if _should_classify_as_estimated(claim):
            return replace(claim, epistemic_type=EpistemicType.ESTIMATED)

        et = _type_from_source(claim.source)
        return replace(claim, epistemic_type=et)


def _should_classify_as_estimated(claim: Claim) -> bool:
    if claim.metadata.get("classify_as_estimated"):
        return True
    if claim.metadata.get("incomplete_underlying_data") or claim.metadata.get(
        "estimate_from_incomplete_data"
    ):
        return True
    # Channel-first: tool/doc/user types come from source, not numeric hunches.
    if claim.source in (
        SourceKind.TOOL,
        SourceKind.DOCUMENT,
        SourceKind.USER,
    ):
        return False
    if claim.metadata.get("missing_data_for_quantity") and re.search(r"\d", claim.text):
        return True
    return False


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


def _type_from_source(source: SourceKind) -> EpistemicType:
    if source is SourceKind.TOOL:
        return EpistemicType.OBSERVED
    if source is SourceKind.DOCUMENT:
        return EpistemicType.RETRIEVED
    if source is SourceKind.USER:
        return EpistemicType.USER_STATED
    if source in (SourceKind.MODEL, SourceKind.INFERENCE, SourceKind.UNKNOWN):
        return EpistemicType.INFERRED
    if source is SourceKind.SYSTEM:
        return EpistemicType.ASSUMED
    return EpistemicType.INFERRED
