from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class EpistemicType(str, Enum):
    """How the system should treat the truth status of the proposition."""

    OBSERVED = "observed"  # direct sensory / instrument / API read with provenance
    RETRIEVED = "retrieved"  # fetched from corpus, DB, tool result as given
    INFERRED = "inferred"  # derived by reasoning; not directly asserted by source
    ASSUMED = "assumed"  # explicit hypothesis for continuation
    ESTIMATED = "estimated"  # numeric or qualitative unknown with model/interval
    USER_STATED = "user_stated"  # attributed to the end user (distinct from observed world state)
    STALE = "stale"  # was valid; validity timebounded or invalidated


class SourceKind(str, Enum):
    """Where the raw proposition entered the system."""

    USER = "user"
    TOOL = "tool"
    DOCUMENT = "document"
    MODEL = "model"  # raw LLM / policy output before epistemic tagging
    INFERENCE = "inference"  # produced by a dedicated inference step
    SYSTEM = "system"  # orchestration / hard-coded defaults
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class Claim:
    """A single asserted proposition with epistemic metadata."""

    id: str
    text: str
    epistemic_type: EpistemicType
    source: SourceKind
    confidence: float
    created_at: datetime
    dependencies: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Claim.id must be non-empty")
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError("confidence must be in [0, 1]")


@dataclass(frozen=True, slots=True)
class Violation:
    """Single failed policy check against a claim."""

    rule_id: str
    claim_id: str
    message: str
