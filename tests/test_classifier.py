from __future__ import annotations

from datetime import datetime, timezone

from epistemic.classifier import EpistemicClassifier
from epistemic.models import Claim, EpistemicType, SourceKind


def _claim(
    source: SourceKind,
    *,
    text: str = "test",
    metadata: dict | None = None,
) -> Claim:
    return Claim(
        id="x",
        text=text,
        epistemic_type=EpistemicType.INFERRED,
        source=source,
        confidence=0.9,
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        metadata=dict(metadata or {}),
    )


def test_tool_maps_to_observed() -> None:
    c = EpistemicClassifier().classify(_claim(SourceKind.TOOL))
    assert c.epistemic_type is EpistemicType.OBSERVED


def test_document_maps_to_retrieved() -> None:
    c = EpistemicClassifier().classify(_claim(SourceKind.DOCUMENT))
    assert c.epistemic_type is EpistemicType.RETRIEVED


def test_user_maps_to_user_stated() -> None:
    c = EpistemicClassifier().classify(_claim(SourceKind.USER))
    assert c.epistemic_type is EpistemicType.USER_STATED


def test_metadata_stale_flag() -> None:
    c = EpistemicClassifier().classify(
        _claim(SourceKind.DOCUMENT, metadata={"classify_as_stale": True})
    )
    assert c.epistemic_type is EpistemicType.STALE


def test_metadata_heuristic_estimated_with_digit() -> None:
    c = EpistemicClassifier().classify(
        _claim(
            SourceKind.MODEL,
            text="roughly 2.5 billion",
            metadata={"missing_data_for_quantity": True},
        )
    )
    assert c.epistemic_type is EpistemicType.ESTIMATED


def test_user_numeric_budget_stays_user_stated() -> None:
    c = EpistemicClassifier().classify(
        _claim(
            SourceKind.USER,
            text="my budget is $500",
            metadata={"missing_data_for_quantity": True},
        )
    )
    assert c.epistemic_type is EpistemicType.USER_STATED
