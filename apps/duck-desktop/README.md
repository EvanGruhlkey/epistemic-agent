# Rubber Duck (desktop)

Tauri 2 + React **frameless** window: fixed **280×460** panel, **pixel duck**, optional hint + input. **Ask the duck** shells out to **Claude Code** or **Cursor** CLI (no HTTP APIs in this app). Drag the duck or empty margin to move.

Repo **pedagogy** for IDE assistants lives in the root [`AGENTS.md`](../../AGENTS.md). The duck app only uses that file to **find the project root** (same folder check); your question is sent to the CLI **as-is**—no `AGENTS.md` is injected into the model prompt.

## Local AI (Claude Code or Cursor)

The app runs **`claude -p …`** from your project root when `claude` is on `PATH` (user message only; no appended system file). If that fails or returns nothing, it tries **`agent --trust -p …`** (Cursor headless CLI) with the same plain prompt, then **`cursor agent --trust -p …`**.

1. **Project root**: The process must see **`AGENTS.md`**. From `apps/duck-desktop` (`npm run tauri:dev`), walking parents finds the repo root. For a packaged `.exe`, set **`RUBBER_DUCK_PROJECT_ROOT`** to your clone (folder that contains `AGENTS.md`).
2. **Claude Code**: Install the [Claude Code CLI](https://docs.claude.com/en/docs/claude-code/cli-usage), run `claude auth login`, ensure `claude` is on `PATH` when you launch the duck.
3. **Cursor**: Install the [Cursor CLI](https://cursor.com/docs/cli/headless) (Windows: `irm 'https://cursor.com/install?win32=true' | iex`). That installs **`agent`** under `%LOCALAPPDATA%\cursor-agent\` (the duck prepends that folder to `PATH` on Windows). Then sign in with [CLI authentication](https://cursor.com/docs/cli/reference/authentication) (same account as the editor—no API key field in this app). The duck calls **`agent --trust -p`** or **`cursor agent --trust -p`** (via the `cursor` shim under `resources\app\bin`, not the `Cursor.exe` GUI) with **Ask** mode and plain **text** output. **`--trust`** matches approving the workspace once when you run `agent` in a terminal.
4. **Cursor CLI login (once)**: In any terminal, run **`agent login`** and finish sign-in in the browser. Until you do, `agent -p` returns “Authentication required” (not an API key in this app).  
   **PowerShell:** if `agent` is not on `PATH`, use: `& "$env:LOCALAPPDATA\cursor-agent\agent.cmd" login`  
   **cmd.exe:** `"%LOCALAPPDATA%\cursor-agent\agent.cmd" login`

The CLIs use their own subscriptions or auth (not configured inside this repo). This app does not add API keys or fetch models over HTTP itself.

**`.env` (optional):** The Rust side loads the first `.env` found walking up from the process current directory (so a repo-root `.env` works when you run `npm run tauri:dev` from `apps/duck-desktop`). Example lines, no spaces around `=`:

`RUBBER_DUCK_CURSOR=C:\Path\To\cursor.cmd` (the CLI shim under `%LOCALAPPDATA%\Programs\cursor\resources\app\bin\`, not `Cursor.exe`)  
`RUBBER_DUCK_AGENT=C:\Path\To\cursor-agent\agent.cmd` (optional if `PATH` already includes `%LOCALAPPDATA%\cursor-agent`)

You can still use Windows **user** environment variables instead; restart the app after changes.

## App / taskbar icon

Icons are generated from the pixel duck SVG (`public/duck.svg`):

```bash
npm run icons
```

Then rebuild. The repo only keeps the five paths listed in `src-tauri/tauri.conf.json`. `npm run icons` may recreate extra platform assets; remove those again if you only ship desktop.

## Prerequisites

- [Node.js](https://nodejs.org/) (Vite 7 wants a recent LTS)
- [Rust + Cargo](https://www.rust-lang.org/tools/install) and [Tauri prerequisites](https://v2.tauri.app/start/prerequisites/)

## Development

```bash
cd apps/duck-desktop
npm install
npm run tauri:dev
```

The `tauri` npm scripts run through `scripts/tauri-env.mjs`, which sets **`CARGO_TARGET_DIR`** to `%LOCALAPPDATA%\RubberDuckDesktop\cargo-target` on Windows (or `~/.cache/rubber-duck-desktop/cargo-target` elsewhere) when unset. That avoids **MSVC LNK1318** (“Unexpected PDB error”) when the repo lives under **OneDrive**, which can lock or corrupt PDBs under `src-tauri/target`. Override by exporting **`CARGO_TARGET_DIR`** yourself if you prefer another location.

## Production build

```bash
cd apps/duck-desktop
npm run tauri:build
```

**Tap** the duck for the panel; **Ask the duck** sends your text to a local CLI. **Drag** to move the window. Close from the taskbar.

## Recommended IDE setup

- [VS Code](https://code.visualstudio.com/) + [Tauri](https://marketplace.visualstudio.com/items?itemName=tauri-apps.tauri-vscode) + [rust-analyzer](https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer)
