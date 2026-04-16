#!/usr/bin/env bash
# Regenerate or verify agent-facing files from the single source of truth: AGENTS.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [[ ! -f "$ROOT/AGENTS.md" ]]; then
  echo "Missing AGENTS.md at $ROOT" >&2
  exit 1
fi
echo "OK: AGENTS.md is the source of truth."
echo "Edit AGENTS.md, then update CLAUDE.md / GEMINI.md / .cursor/rules if needed."
