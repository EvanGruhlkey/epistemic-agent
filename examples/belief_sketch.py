"""
Sketch: perception -> belief state -> safe output (for LLM agent builders).

Run from repo root: python examples/belief_sketch.py

This does NOT implement Bayes math. It shows where that math would live:
``confidence`` and ``metadata`` on :class:`~epistemic.models.Claim`` are the
hooks for priors, likelihoods, and decay; :class:`~epistemic.memory.InMemoryClaimStore`
is where beliefs persist across turns; :class:`~epistemic.rules.RuleEngine`
is where “don’t act on speculation as if it were fact” becomes executable.
"""

from __future__ import annotations

import sys
from pathlib import Path

_sys_src = str(Path(__file__).resolve().parents[1] / "src")
if _sys_src not in sys.path:
    sys.path.insert(0, _sys_src)

from epistemic.classifier import EpistemicClassifier
from epistemic.extractor import ClaimExtractor
from epistemic.formatter import OutputFormatter
from epistemic.memory import InMemoryClaimStore
from epistemic.models import Claim, EpistemicType, SourceKind, utc_now
from epistemic.pipeline import run_pipeline
from epistemic.rules import RuleEngine


class GiftScenarioExtractor(ClaimExtractor):
    """Synthetic multi-source batch: clicks (tool), user words, model belief."""

    def __init__(self) -> None:
        super().__init__(link_segments_to_transcript_premise=False)

    def extract(self, raw: str) -> list[Claim]:
        del raw
        t = utc_now()
        obs_clicks = Claim(
            id="obs-clicks",
            text="User spent 6 minutes on personalized-engraving SKUs; skipped discount bundles.",
            epistemic_type=EpistemicType.OBSERVED,
            source=SourceKind.TOOL,
            confidence=0.9,
            created_at=t,
            metadata={"layer": "perception", "signal": "behavior"},
        )
        obs_user = Claim(
            id="obs-user-said",
            text='User said: "It\'s for someone who has everything."',
            epistemic_type=EpistemicType.USER_STATED,
            source=SourceKind.USER,
            confidence=1.0,
            created_at=t,
            metadata={"layer": "perception", "signal": "utterance"},
        )
        belief = Claim(
            id="belief-intent",
            text="Likely intent: user wants a thoughtful, non-generic gift (not necessarily price-sensitive).",
            epistemic_type=EpistemicType.INFERRED,
            source=SourceKind.MODEL,
            confidence=0.72,
            created_at=t,
            dependencies=("obs-clicks", "obs-user-said"),
            metadata={
                "layer": "belief",
                "belief_kind": "latent_intent",
                # Hooks for fuller Bayesian treatment later, e.g.:
                # "prior": 0.5, "log_bayes_factor": 0.9, "last_observation_ids": [...]
            },
        )
        return [obs_clicks, obs_user, belief]


def main() -> None:
    clf = EpistemicClassifier()
    claims_in = GiftScenarioExtractor().extract("")
    claims = [clf.classify(c) for c in claims_in]

    print("=== 1) Typed claims (after classifier) ===\n")
    for c in claims:
        print(f"  {c.id}: {c.epistemic_type.value} (confidence {c.confidence:.0%})")
        print(f"    deps: {c.dependencies or '()'}")
        print(f"    text: {c.text[:70]}...")

    store = InMemoryClaimStore()
    store.put_all(claims)

    eng = RuleEngine()
    violations = eng.evaluate(claims)
    print(f"\n=== 2) Policy (transparent batch) violations: {len(violations)} ===\n")
    for v in violations:
        print(f"  {v.rule_id}: {v.message}")

    fmt = OutputFormatter()
    print("\n=== 3) Transparent narration (what an assistant may show the user) ===\n")
    print(fmt.format(claims))

    print("\n=== 4) Factual-style assistant reply (partial: beliefs withheld) ===\n")
    result = run_pipeline(
        "",
        presentation_mode="factual",
        extractor=GiftScenarioExtractor(),
    )
    print(result.output_text)
    print("ok (no violations):", result.ok)

    print(
        "\n---\n"
        "Next steps to grow this into real Bayesian beliefs:\n"
        "  - Store Beta/Gaussian params in metadata or a sibling table; update on each observation.\n"
        "  - Use dependencies to force every latent belief to list which observations moved it.\n"
        "  - Let tool results insert OBSERVED rows; let the planner only commit ACTS when factual policy passes.\n"
    )


if __name__ == "__main__":
    main()
