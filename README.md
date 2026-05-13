# Rubber Duck Learning

<a href="https://github.com/EvanGruhlkey/rubber-duck-learning/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License" /></a> <a href="https://github.com/EvanGruhlkey/rubber-duck-learning/stargazers"><img src="https://img.shields.io/github/stars/EvanGruhlkey/rubber-duck-learning?style=flat" alt="Stars" /></a>

<p align="center">
  <img src="apps/duck-desktop/public/duck.svg" width="112" height="112" alt="Pixel art rubber duck" />
</p>

## What’s in this repo

| | |
| --- | --- |
| **Desktop duck** | [**`apps/duck-desktop/`**](./apps/duck-desktop/README.md). Tauri app: floating pixel duck on your screen (draggable). **No web server, no marketing site.** |
| **Pedagogy** | [**AGENTS.md**](./AGENTS.md). How AI assistants should help: Socratic questions, hints, and *you* stay the author. Wired for [**Cursor**](.cursor/rules/rubber-duck-learning.mdc) and [**Claude Code**](.claude/skills/rubber-duck-learning/SKILL.md) (`/rubber-duck-learning`). |
| **Art** | [`apps/duck-desktop/public/duck.svg`](./apps/duck-desktop/public/duck.svg): pixel duck used in the app; [`npm run icons`](./apps/duck-desktop/README.md) also derives bundle icons from it. |

## Why Rubber Duck Learning?

Most AI coding tools optimize for speed. This project optimizes for **understanding**: productive struggle, short questions, and small nudges, whether you’re using the floating duck or an IDE assistant following **`AGENTS.md`**.

## Run the desktop duck

```bash
cd apps/duck-desktop
npm install
npm run tauri dev
```

Needs [Rust](https://www.rust-lang.org/tools/install) and [Tauri prerequisites](https://v2.tauri.app/start/prerequisites/). Details: [`apps/duck-desktop/README.md`](./apps/duck-desktop/README.md).
