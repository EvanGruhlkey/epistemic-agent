from __future__ import annotations

import argparse
import json
import sys

from epistemic.llm_client import DEFAULT_MODEL, generate_model_answer
from epistemic.pipeline import run_pipeline
from epistemic.serde import pipeline_result_to_jsonable


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Query an LLM, then tag and gate the answer with the epistemic pipeline "
            "(transparent or factual presentation)."
        )
    )
    parser.add_argument(
        "-m",
        "--message",
        required=True,
        help="User message / question sent to the model.",
    )
    parser.add_argument(
        "--mode",
        choices=["transparent", "factual"],
        default="transparent",
        help="Pipeline presentation mode (default: transparent).",
    )
    parser.add_argument(
        "--model",
        default=None,
        help=f"Chat model id (default: env OPENAI_MODEL or {DEFAULT_MODEL}).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not call the API; use canned text (no API key).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_out",
        help="Print PipelineResult as JSON (claims, violations, ok).",
    )
    parser.add_argument(
        "--show-raw",
        action="store_true",
        help="Print the model's raw text before the epistemic section.",
    )
    args = parser.parse_args(argv)

    try:
        raw = generate_model_answer(
            args.message,
            model=args.model,
            dry_run=args.dry_run,
        )
        result = run_pipeline(raw, presentation_mode=args.mode)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 1

    if args.show_raw and not args.json_out:
        print("=== Raw model output ===\n")
        print(raw)
        print("\n=== Epistemic output ===\n")

    if args.json_out:
        print(json.dumps(pipeline_result_to_jsonable(result), indent=2))
    else:
        print(result.output_text)
        print(f"\nok (no violations): {result.ok}")

    return 0 if result.ok else 2
