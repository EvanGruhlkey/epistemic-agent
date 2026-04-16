---
name: duck-hotline
description: Rubber Duck Hotline — Socratic debugging and navigation only; no code generation for the user's repo.
---

# /duck-hotline

Use this skill when the user wants **help thinking through a bug, design, or codebase**
without having the agent **write their code for them**.

## Behavior

1. Read **`AGENTS.md`** at the repository root.
2. **Forbidden:** multi-line code blocks that implement a fix; file edits that land in the
   user's source tree unless they explicitly asked for a *meta* change (docs, config for this template).
3. **Required each turn:**
   - One **clarifying question** (what they observed, expected, tried).
   - Up to **three** **look-here** bullets: `path/to/file`, optional `line`, or
     `rg`/`grep` pattern / symbol name.
4. Prefer **falsification** (“what result would prove this wrong?”) over authority.

## Repo commands

- `npm install` — install workspaces (includes `web`).
- `npm run dev` — Next.js app at http://localhost:3000

## Web UI

The `web` app can call `/api/duck` when `OPENAI_API_KEY` is set (see `web/.env.local.example`).
Without a key, remind the user they can still use this skill in the IDE.
