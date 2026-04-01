from __future__ import annotations

from typing import Any

from epistemic.models import Claim, EpistemicType, SourceKind, utc_now


class ClaimExtractor:
    """Turn raw model text into provisional claims (one pass, heuristic split)."""

    def __init__(
        self,
        *,
        source: SourceKind = SourceKind.MODEL,
        default_confidence: float = 0.55,
        base_metadata: dict[str, Any] | None = None,
    ) -> None:
        self._source = source
        self._default_confidence = default_confidence
        self._base_metadata = dict(base_metadata) if base_metadata else {}

    def extract(self, raw: str) -> list[Claim]:
        segments = _split_segments(raw)
        out: list[Claim] = []
        for i, text in enumerate(segments, start=1):
            meta = {**self._base_metadata}
            out.append(
                Claim(
                    id=f"claim-{i}",
                    text=text,
                    epistemic_type=EpistemicType.INFERRED,
                    source=self._source,
                    confidence=self._default_confidence,
                    created_at=utc_now(),
                    metadata=meta,
                )
            )
        return out


def _split_segments(raw: str) -> list[str]:
    t = raw.strip()
    if not t:
        return []
    for sep in ("\n\n", "\n"):
        parts = [p.strip() for p in t.split(sep) if p.strip()]
        if len(parts) > 1:
            return parts
    return [t]
