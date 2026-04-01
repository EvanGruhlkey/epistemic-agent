from __future__ import annotations

from typing import Any

from epistemic.models import Claim, EpistemicType, SourceKind, utc_now


PREMISE_MODEL_TRANSCRIPT_ID = "premise-llm-output"


class ClaimExtractor:
    """
    Turn raw model text into provisional claims (one pass, heuristic split).

    By default, adds a single **retrieved** premise claim for the full transcript and
    links each segment to it so :class:`~epistemic.rules.RuleEngine` can enforce
    ``inferred_requires_premises`` without silently waving inference roots.
    """

    def __init__(
        self,
        *,
        source: SourceKind = SourceKind.MODEL,
        default_confidence: float = 0.55,
        base_metadata: dict[str, Any] | None = None,
        link_segments_to_transcript_premise: bool = True,
    ) -> None:
        self._source = source
        self._default_confidence = default_confidence
        self._base_metadata = dict(base_metadata) if base_metadata else {}
        self._link_transcript = link_segments_to_transcript_premise

    def extract(self, raw: str) -> list[Claim]:
        segments = _split_segments(raw)
        if not segments:
            return []

        premise_id: str | None = PREMISE_MODEL_TRANSCRIPT_ID
        out: list[Claim] = []

        if self._link_transcript:
            snippet = raw.strip()
            if len(snippet) > 400:
                snippet = snippet[:400] + "..."
            out.append(
                Claim(
                    id=premise_id,
                    text=f"(verbatim model output) {snippet}",
                    epistemic_type=EpistemicType.RETRIEVED,
                    source=SourceKind.DOCUMENT,
                    confidence=1.0,
                    created_at=utc_now(),
                    metadata={**self._base_metadata, "epistemic_hint": "retrieved"},
                )
            )
        else:
            premise_id = None

        deps: tuple[str, ...] = (premise_id,) if premise_id else ()

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
                    dependencies=deps,
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
