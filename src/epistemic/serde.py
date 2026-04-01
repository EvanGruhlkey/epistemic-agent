from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from epistemic.models import Claim, EpistemicType, SourceKind, Violation
from epistemic.pipeline import PipelineResult


def _parse_datetime(raw: str) -> datetime:
    s = raw.replace("Z", "+00:00")
    dt = datetime.fromisoformat(s)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def claim_to_jsonable(claim: Claim) -> dict[str, Any]:
    """dict with JSON-safe values (``metadata`` must itself be JSON-serializable)."""
    return {
        "id": claim.id,
        "text": claim.text,
        "epistemic_type": claim.epistemic_type.value,
        "source": claim.source.value,
        "confidence": claim.confidence,
        "created_at": claim.created_at.isoformat(),
        "dependencies": list(claim.dependencies),
        "metadata": claim.metadata,
    }


def claim_from_jsonable(data: dict[str, Any]) -> Claim:
    """Inverse of :func:`claim_to_jsonable`."""
    try:
        et = EpistemicType(data["epistemic_type"])
        src = SourceKind(data["source"])
    except KeyError as e:
        raise ValueError(f"missing field: {e.args[0]}") from e
    except ValueError as e:
        raise ValueError(f"invalid enum in claim: {e}") from e

    deps = data.get("dependencies", [])
    if not isinstance(deps, list):
        raise ValueError("dependencies must be a list")
    meta = data.get("metadata", {})
    if meta is None:
        meta = {}
    if not isinstance(meta, dict):
        raise ValueError("metadata must be a dict")

    return Claim(
        id=str(data["id"]),
        text=str(data["text"]),
        epistemic_type=et,
        source=src,
        confidence=float(data["confidence"]),
        created_at=_parse_datetime(str(data["created_at"])),
        dependencies=tuple(str(x) for x in deps),
        metadata=dict(meta),
    )


def violation_to_jsonable(v: Violation) -> dict[str, Any]:
    return {
        "rule_id": v.rule_id,
        "claim_id": v.claim_id,
        "message": v.message,
    }


def violation_from_jsonable(data: dict[str, Any]) -> Violation:
    return Violation(
        rule_id=str(data["rule_id"]),
        claim_id=str(data["claim_id"]),
        message=str(data["message"]),
    )


def pipeline_result_to_jsonable(result: PipelineResult) -> dict[str, Any]:
    """Snapshot of a run suitable for ``json.dumps``."""
    return {
        "ok": result.ok,
        "output_text": result.output_text,
        "claims": [claim_to_jsonable(c) for c in result.claims],
        "violations": [violation_to_jsonable(v) for v in result.violations],
    }


def pipeline_result_from_jsonable(data: dict[str, Any]) -> PipelineResult:
    claims = tuple(claim_from_jsonable(x) for x in data["claims"])
    violations = tuple(violation_from_jsonable(x) for x in data["violations"])
    return PipelineResult(
        claims=claims,
        violations=violations,
        output_text=str(data["output_text"]),
        ok=bool(data["ok"]),
    )


def dumps_pipeline_result(result: PipelineResult, **kwargs: Any) -> str:
    """``json.dumps`` of :func:`pipeline_result_to_jsonable`."""
    return json.dumps(pipeline_result_to_jsonable(result), **kwargs)


def loads_pipeline_result(s: str) -> PipelineResult:
    return pipeline_result_from_jsonable(json.loads(s))
