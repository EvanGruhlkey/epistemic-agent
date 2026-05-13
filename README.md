# Rubber Duck Learning

<a href="https://github.com/EvanGruhlkey/rubber-duck-learning/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License" /></a> <a href="https://github.com/EvanGruhlkey/rubber-duck-learning/stargazers"><img src="https://img.shields.io/github/stars/EvanGruhlkey/rubber-duck-learning?style=flat" alt="Stars" /></a>

<p align="center">
  <img src="apps/duck-desktop/public/duck.svg" width="112" height="112" alt="Pixel art rubber duck" />
</p>

Hi. This repo is a small **desktop duck** you can keep on screen while you work, plus a set of **rules and habits** (`AGENTS.md`) for working with AI in a slower, more “explain it to the duck” style. There’s no website or hosted app here, just the Tauri build and the pedagogy files.

**Desktop duck:** [`apps/duck-desktop/`](./apps/duck-desktop/README.md) (Tauri: floating, draggable pixel duck).

**Pedagogy:** [`AGENTS.md`](./AGENTS.md) (how assistants should ask questions and point you to your own code, not take it over). Hooks for [**Cursor**](.cursor/rules/rubber-duck-learning.mdc) and [**Claude Code**](.claude/skills/rubber-duck-learning/SKILL.md) (`/rubber-duck-learning`).

**Duck art (SVG):** [`apps/duck-desktop/public/duck.svg`](./apps/duck-desktop/public/duck.svg) (what the app shows; also used when you run `npm run icons` in the app folder).

## Why this exists

A lot of coding AI is built to ship code fast. Rubber Duck Learning is biased toward **understanding**: short questions, small hints, and you stay in charge. That applies whether you’re staring at the desktop duck or using an assistant that follows `AGENTS.md`.

## Run the desktop duck

```bash
cd apps/duck-desktop
npm install
npm run tauri dev
```

You’ll need [Rust](https://www.rust-lang.org/tools/install) and the [Tauri prerequisites](https://v2.tauri.app/start/prerequisites/). More detail in [`apps/duck-desktop/README.md`](./apps/duck-desktop/README.md).
