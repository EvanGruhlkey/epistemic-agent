from __future__ import annotations

import os
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from epistemic.pipeline import PipelineResult

DEFAULT_MODEL = "gpt-4o-mini"
_ENV_MODEL = "OPENAI_MODEL"
_ENV_KEY = "OPENAI_API_KEY"

# Encourages line-oriented claims for the default :class:`~epistemic.extractor.ClaimExtractor`.
_DEFAULT_SYSTEM = """You are a careful assistant. Answer the user in plain text.
Put each distinct factual claim on its own line (one sentence per line when possible).
If something is uncertain or a guess, say so briefly on that line.
Do not wrap the answer in markdown code fences."""


def generate_model_answer(
    user_prompt: str,
    *,
    model: str | None = None,
    dry_run: bool = False,
    system_prompt: str = _DEFAULT_SYSTEM,
) -> str:
    """
    Return raw model text suitable for :func:`~epistemic.pipeline.run_pipeline`.

    Uses the OpenAI Chat Completions API when ``dry_run`` is False.
    Requires ``OPENAI_API_KEY`` and ``pip install "epistemic-types[llm]"``.
    """
    if dry_run:
        return (
            "[dry-run] The capital of France is Paris.\n"
            "The population of Mars is not well documented in this stub response."
        )

    try:
        from openai import OpenAI
    except ImportError as e:
        raise RuntimeError(
            'OpenAI SDK not installed. Run: pip install "epistemic-types[llm]"'
        ) from e

    api_key = os.environ.get(_ENV_KEY)
    if not api_key:
        raise RuntimeError(
            f"Set {_ENV_KEY} in the environment (or use --dry-run for offline testing)."
        )

    resolved_model = model or os.environ.get(_ENV_MODEL) or DEFAULT_MODEL
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=resolved_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt.strip()},
        ],
    )
    choice = response.choices[0].message.content
    if not choice or not str(choice).strip():
        raise RuntimeError("Model returned an empty response.")
    return str(choice).strip()


def run_llm_pipeline(
    user_prompt: str,
    *,
    presentation_mode: Literal["transparent", "factual"] = "transparent",
    model: str | None = None,
    dry_run: bool = False,
    system_prompt: str = _DEFAULT_SYSTEM,
    **pipeline_kw: object,
) -> PipelineResult:
    """Call the model, then run the epistemic pipeline on its output."""
    from epistemic.pipeline import run_pipeline

    raw = generate_model_answer(
        user_prompt,
        model=model,
        dry_run=dry_run,
        system_prompt=system_prompt,
    )
    return run_pipeline(
        raw,
        presentation_mode=presentation_mode,
        **pipeline_kw,  # type: ignore[arg-type]
    )
