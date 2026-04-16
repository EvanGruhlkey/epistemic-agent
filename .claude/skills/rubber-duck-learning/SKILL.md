---
name: rubber-duck-learning
description: Rubber Duck Learning. Socratic debugging and navigation only; no code generation for the user's repo.
---

# /rubber-duck-learning

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

No install or server is required. Everything runs inside your agent and IDE.
