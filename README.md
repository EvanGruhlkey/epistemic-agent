# Duck Hotline

Socratic pair programming: questions and pointers only — you keep the keyboard. See **AGENTS.md** for agent rules. **Claude Code:** `/duck-hotline`.

## Quick start

```bash
npm install --prefix web
npm run dev
```

Open http://localhost:3000. Optional: `web/.env.local` with `OPENAI_API_KEY` for browser replies.

### Windows: SWC / “not a valid Win32 application”

If `next dev` fails loading `@next/swc-win32-x64-msvc` or lockfile patch errors with `ENOWORKSPACES`, do a **clean install** in `web` only (this repo does **not** use npm workspaces so Next can manage its own lockfile):

```powershell
Remove-Item -Recurse -Force node_modules, web\node_modules -ErrorAction SilentlyContinue
Remove-Item -Force package-lock.json, web\package-lock.json -ErrorAction SilentlyContinue
npm install --prefix web
npm run dev
```

Repos on **OneDrive** sometimes corrupt native `.node` binaries; moving the project off OneDrive or a clean reinstall usually fixes it. `@next/swc-wasm-nodejs` is listed in `web` as a fallback when native SWC fails.

Layout matches agent-first templates (AGENTS.md, `.cursor/rules`, `.claude/skills`). Legacy Python: `src/epistemic/`, `pip install -e .`.

MIT