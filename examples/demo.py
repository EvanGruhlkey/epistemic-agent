from __future__ import annotations
import sys
from pathlib import Path
from epistemic import run_pipeline

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

_FAKE_LLM = """The capital of France is Paris.
The population of Mars is 2.5 billion people."""

if __name__ == "__main__":
    transparent = run_pipeline(_FAKE_LLM, presentation_mode="transparent")
    print("=== transparent mode (rules pass, labels shown) ===")
    print(transparent.output_text)
    print("ok:", transparent.ok)

    print()
    factual = run_pipeline(_FAKE_LLM, presentation_mode="factual")
    print("=== factual mode (model-inferred claims -> policy block) ===")
    print(factual.output_text)
    print("ok:", factual.ok)
