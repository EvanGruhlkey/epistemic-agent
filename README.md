# Duck Hotline

**Socratic pair programming in your IDE** — the agent asks sharp questions and points you to files, symbols, and checks. It does **not** write your code for you.

| Where you work | How to use it |
|----------------|---------------|
| **Cursor** | Open this repo; rule **`duck-hotline`** applies (see `.cursor/rules/duck-hotline.mdc`). |
| **Claude Code** | Run **`/duck-hotline`** (skill: `.claude/skills/duck-hotline/SKILL.md`). |
| **Other agents** | Read **`AGENTS.md`** at repo root — single source of truth. |

## Quick start

1. Clone or copy this repo into your project (or use it as a reference and copy `AGENTS.md` + rules/skills into yours).
2. Open the folder in **Cursor** or **Claude Code** (or any agent that reads project instructions).
3. Read **`AGENTS.md`** so expectations match: one question per turn, at most three look-here hints, no solution code dumps.
4. Start a chat and describe the bug or design problem; the agent navigates — you type the fixes.

No install step is required for the hotline behavior itself.

## Prerequisites

- An AI coding assistant that can read project files and follow **`AGENTS.md`** (or your ported copy).

**Optional — Python package** (tests and `src/epistemic/` experiments):

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

## How it works

1. **Product rules** — No codegen for the user’s repo; hypotheses over authority; hints grounded in what was actually read or searched.
2. **One turn, one focus** — One clarifying question plus up to three pointers (`path`, line range, or symbol / `rg` pattern).
3. **Multiple entrypoints** — After editing **`AGENTS.md`**, keep **`CLAUDE.md`**, **`GEMINI.md`**, and Cursor rules in sync manually (or run `scripts/sync-agent-rules.sh` as a quick reminder check).

## Project structure

```
.
├── AGENTS.md                 # Rules for all agents (source of truth)
├── CLAUDE.md                 # Pointer to AGENTS.md + Claude skill
├── GEMINI.md                 # Pointer to AGENTS.md
├── .cursor/rules/            # Cursor rule (duck-hotline)
├── .claude/skills/duck-hotline/
├── scripts/sync-agent-rules.sh
├── src/epistemic/            # Optional Python library / experiments
├── tests/
└── pyproject.toml
```

## Commands

| Command | Purpose |
|---------|---------|
| `pip install -e ".[dev]"` | Editable install + dev deps (pytest, etc.). |
| `pytest` | Run tests under `tests/`. |
| `./scripts/sync-agent-rules.sh` | Sanity check that `AGENTS.md` exists; reminds you to sync other agent files (bash). |

## License

MIT
