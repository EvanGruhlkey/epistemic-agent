"""Contrast demo: run from repo root with ``python examples/demo.py``."""

from __future__ import annotations

import sys
from pathlib import Path

_sys_src = str(Path(__file__).resolve().parents[1] / "src")
if _sys_src not in sys.path:
    sys.path.insert(0, _sys_src)

from epistemic import run_pipeline
from epistemic.extractor import ClaimExtractor
from epistemic.models import Claim, EpistemicType, SourceKind, utc_now


class ContrastDemoExtractor(ClaimExtractor):
    """
    Two hand-authored claims with opposite epistemic status (no transcript premise).

    - France → document / :class:`~epistemic.models.EpistemicType.RETRIEVED`
    - Mars → model / :class:`~epistemic.models.EpistemicType.INFERRED` (linked to France as premise id)
    """

    def __init__(self) -> None:
        super().__init__(link_segments_to_transcript_premise=False)

    def extract(self, raw: str) -> list[Claim]:
        del raw  # fixed scenario
        t = utc_now()
        france = Claim(
            id="claim-france",
            text="The capital of France is Paris.",
            epistemic_type=EpistemicType.RETRIEVED,
            source=SourceKind.DOCUMENT,
            confidence=0.95,
            created_at=t,
            dependencies=(),
            metadata={},
        )
        mars = Claim(
            id="claim-mars",
            text="Mars has a population of 2.5 billion.",
            epistemic_type=EpistemicType.INFERRED,
            source=SourceKind.MODEL,
            confidence=0.45,
            created_at=t,
            dependencies=("claim-france",),
            metadata={},
        )
        return [france, mars]


if __name__ == "__main__":
    extractor = ContrastDemoExtractor()

    print(
        "Same two sentences, different epistemic typing:\n"
        "  - France: retrieved from a source\n"
        "  - Mars: model-inferred (explicit premise link for policy)\n"
    )

    transparent = run_pipeline(
        "", presentation_mode="transparent", extractor=extractor
    )
    print("=== Transparent mode ===")
    print("(France reads as a normal retrieved claim; Mars is explicitly qualified.)\n")
    print(transparent.output_text)
    print("ok:", transparent.ok)

    print()
    factual = run_pipeline(
        "", presentation_mode="factual", extractor=extractor
    )
    print("=== Factual mode ===")
    print("(France may be asserted; inferred Mars is withheld.)\n")
    print(factual.output_text)
    print("ok:", factual.ok)
