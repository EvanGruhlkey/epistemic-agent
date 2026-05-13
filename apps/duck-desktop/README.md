# Rubber Duck (desktop)

Tauri 2 + React **frameless** window: transparent background, **pixel duck** only. Drag the duck (or the margin) to move the window; chat / pop-over text can be wired in later.

Repo **pedagogy** (Socratic rules for AI in Cursor/Claude) lives in the root [`AGENTS.md`](../../AGENTS.md). This folder is only the **desktop app**, not a website.

## App / taskbar icon

Icons are generated from the pixel duck SVG (`public/duck.svg`). To refresh after changing the artwork:

```bash
npm run icons
```

Then rebuild (`npm run tauri build`) or run dev again so Windows picks up the new `icon.ico` embedded in the executable. If the taskbar still shows an old image, unpin the app or clear the icon cache once.

The repo only keeps the five paths listed in `src-tauri/tauri.conf.json` (`32x32.png`, `128x128.png`, `128x128@2x.png`, `icon.icns`, `icon.ico`). `npm run icons` will recreate extra Android/iOS/Appx PNGs—remove those again if you only ship desktop.

## Prerequisites

- [Node.js](https://nodejs.org/) (Vite 7 wants a recent LTS; upgrade if `npm` warns about the engine)
- [Rust + Cargo](https://www.rust-lang.org/tools/install) and the [Tauri prerequisites](https://v2.tauri.app/start/prerequisites/) for your OS

## Development

```bash
cd apps/duck-desktop
npm install
npm run tauri dev
```

## Production build

```bash
cd apps/duck-desktop
npm run tauri build
```

The window is **fully transparent** (no panel frame): you only see the **pixel duck**. It is **not user-resizable**—only **moved** by dragging the duck or the empty margin (Tauri `startDragging()`). Close the app from the taskbar when running the desktop build (`npm run tauri dev` needs Rust installed).

## Recommended IDE setup

- [VS Code](https://code.visualstudio.com/) + [Tauri](https://marketplace.visualstudio.com/items?itemName=tauri-apps.tauri-vscode) + [rust-analyzer](https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer)
