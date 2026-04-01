"""Examples: run from repo root with ``python examples/demo.py``."""

from __future__ import annotations

import sys
from pathlib import Path

_sys_src = str(Path(__file__).resolve().parents[1] / "src")
if _sys_src not in sys.path:
    sys.path.insert(0, _sys_src)

from epistemic import run_pipeline

# Simulated model output (two lines). The default extractor also adds a retrieved
# "verbatim transcript" premise so every inferred segment has explicit premises.
_FAKE_LLM = """The capital of France is Paris.
The population of Mars is 2.5 billion people."""

if __name__ == "__main__":
    print(
        "This demo encodes: epistemic types, premise links for inference,\n"
        "factual gating, estimates/staleness/user-stated policies in rules.py.\n"
    )

    transparent = run_pipeline(_FAKE_LLM, presentation_mode="transparent")
    print("=== transparent mode ===")
    print(transparent.output_text)
    print("ok:", transparent.ok)

    print()
    factual = run_pipeline(_FAKE_LLM, presentation_mode="factual")
    print("=== factual mode (inferred lines cannot be asserted as bare facts) ===")
    print(factual.output_text)
    print("ok:", factual.ok)
