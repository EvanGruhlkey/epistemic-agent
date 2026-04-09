from __future__ import annotations

from epistemic import run_pipeline
from epistemic.extractor import ClaimExtractor
from epistemic.models import Claim, EpistemicType, SourceKind, utc_now


class _ContrastExtractor(ClaimExtractor):
    """Same scenario as examples/demo.py (France retrieved, Mars inferred)."""

    def __init__(self) -> None:
        super().__init__(link_segments_to_transcript_premise=False)

    def extract(self, raw: str) -> list[Claim]:
        del raw
        t = utc_now()
        return [
            Claim(
                id="claim-france",
                text="The capital of France is Paris.",
                epistemic_type=EpistemicType.RETRIEVED,
                source=SourceKind.DOCUMENT,
                confidence=0.95,
                created_at=t,
                dependencies=(),
                metadata={},
            ),
            Claim(
                id="claim-mars",
                text="Mars has a population of 2.5 billion.",
                epistemic_type=EpistemicType.INFERRED,
                source=SourceKind.MODEL,
                confidence=0.45,
                created_at=t,
                dependencies=("claim-france",),
                metadata={},
            ),
        ]


def test_factual_mode_emits_partial_output_when_some_claims_fail() -> None:
    r = run_pipeline("", presentation_mode="factual", extractor=_ContrastExtractor())
    assert not r.ok
    assert "Paris" in r.output_text
    assert "2.5 billion" not in r.output_text.split("---")[0]
    assert "claim-mars" in r.output_text
