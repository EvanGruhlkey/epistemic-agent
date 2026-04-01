from __future__ import annotations

from collections.abc import Iterable
from dataclasses import replace
from datetime import datetime, timezone
from typing import Any

from epistemic.models import Claim, EpistemicType, utc_now


def apply_staleness(claim: Claim, *, now: datetime | None = None) -> Claim:
    """
    Return a copy with ``EpistemicType.STALE`` if TTL or ``expires_at`` has passed.
    Does not downgrade an already-stale claim or mutate storage.
    """
    at = now if now is not None else utc_now()
    if claim.epistemic_type is EpistemicType.STALE:
        return claim
    if not _is_expired(claim, at):
        return claim
    meta = {**claim.metadata, "stale_reason": "ttl_or_expires_at"}
    return replace(claim, epistemic_type=EpistemicType.STALE, metadata=meta)


def _is_expired(claim: Claim, now: datetime) -> bool:
    if _past_expires_at(claim.metadata.get("expires_at"), now):
        return True
    ttl = claim.metadata.get("ttl_seconds")
    if ttl is None:
        return False
    try:
        limit = float(ttl)
    except (TypeError, ValueError):
        return False
    age = (now - claim.created_at).total_seconds()
    return age > limit


def _past_expires_at(raw: Any, now: datetime) -> bool:
    dt = _parse_expires_at(raw)
    if dt is None:
        return False
    return now > dt


def _parse_expires_at(raw: Any) -> datetime | None:
    if raw is None:
        return None
    if isinstance(raw, datetime):
        return raw if raw.tzinfo else raw.replace(tzinfo=timezone.utc)
    if isinstance(raw, str):
        s = raw.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(s)
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    return None


class InMemoryClaimStore:
    """Process-local claim registry with optional staleness on read."""

    def __init__(self) -> None:
        self._claims: dict[str, Claim] = {}

    def put(self, claim: Claim) -> None:
        self._claims[claim.id] = claim

    def put_all(self, claims: Iterable[Claim]) -> None:
        for c in claims:
            self.put(c)

    def get(self, claim_id: str) -> Claim | None:
        return self._claims.get(claim_id)

    def get_effective(self, claim_id: str, *, now: datetime | None = None) -> Claim | None:
        c = self.get(claim_id)
        if c is None:
            return None
        return apply_staleness(c, now=now)

    def __contains__(self, claim_id: str) -> bool:
        return claim_id in self._claims

    def discard(self, claim_id: str) -> None:
        self._claims.pop(claim_id, None)

    def clear(self) -> None:
        self._claims.clear()


def merge_dependency_closure(
    batch: Iterable[Claim],
    store: InMemoryClaimStore,
    *,
    now: datetime | None = None,
) -> list[Claim]:
    """
    Union of ``batch`` plus any transitive dependencies found in ``store`` (effective/stale-aware).

    IDs present in ``batch`` win over store rows with the same id.
    """
    indexed: dict[str, Claim] = {c.id: c for c in batch}
    pending = list(indexed.keys())
    at = now if now is not None else utc_now()
    i = 0
    while i < len(pending):
        cid = pending[i]
        i += 1
        c = indexed[cid]
        for dep_id in c.dependencies:
            if dep_id in indexed:
                continue
            ext = store.get_effective(dep_id, now=at)
            if ext is None:
                continue
            indexed[dep_id] = ext
            pending.append(dep_id)
    return list(indexed.values())
