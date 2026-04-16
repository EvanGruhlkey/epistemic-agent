# Rubber Duck Learning

<a href="https://github.com/EvanGruhlkey/rubber-duck-learning/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License" /></a> <a href="https://github.com/EvanGruhlkey/rubber-duck-learning/stargazers"><img src="https://img.shields.io/github/stars/EvanGruhlkey/rubber-duck-learning?style=flat" alt="Stars" /></a>

A reusable template for **Socratic pair programming** with AI coding agents. The model asks sharp questions and points you to **files, symbols, and checks**. It does **not** write your code for you.

**Recommended: [Claude Code](https://docs.anthropic.com/en/docs/claude-code) with a strong reasoning model for best results**, but it works fine with other AI coding agents too.

Open this repo in your agent, run **`/rubber-duck-learning`** in Claude Code (or use the **Cursor** rule), and you get **one clarifying question** plus **at most three look-here hints** per turn while you stay on the keyboard.

## Quick Start

1. **Clone this repository**
   ```bash
   git clone https://github.com/EvanGruhlkey/rubber-duck-learning.git
   cd rubber-duck-learning
   ```
2. **Start your AI agent** (Claude Code recommended):
   ```bash
   claude --chrome
   ```
3. **Run the skill**:
   ```
   /rubber-duck-learning
   ```
   Then say what you are stuck on. In **Cursor**, just open the folder: the **`rubber-duck-learning`** rule is already there (see `.cursor/rules/rubber-duck-learning.mdc`).
4. **Customize** (optional): copy `AGENTS.md`, `.cursor/rules/`, and `.claude/skills/rubber-duck-learning/` into your own repo and tweak the wording.

> Using a different agent? Open **`AGENTS.md`**. Most agents pick it up automatically.

## Supported Platforms

| Agent                                                         | Status                     |
| ------------------------------------------------------------- | -------------------------- |
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | **Recommended** |
| [Codex CLI](https://github.com/openai/codex)                  | Supported                  |
| [OpenCode](https://opencode.ai/)                              | Supported                  |
| [GitHub Copilot](https://github.com/features/copilot)         | Supported                  |
| [Cursor](https://cursor.com/)                                 | Supported                  |
| [Windsurf](https://codeium.com/windsurf)                      | Supported                  |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli)     | Supported                  |
| [Cline](https://github.com/cline/cline)                       | Supported                  |
| [Roo Code](https://github.com/RooCodeInc/Roo-Code)            | Supported                  |
| [Continue](https://continue.dev/)                             | Supported                  |
| [Amazon Q](https://aws.amazon.com/q/developer/)               | Supported                  |
| [Augment Code](https://www.augmentcode.com/)                  | Supported                  |
| [Aider](https://aider.chat/)                                  | Supported                  |

## Prerequisites

- An AI coding agent (see [Supported Platforms](#supported-platforms))
- [Node.js](https://nodejs.org/) 18+ **only if** you want to run **`npm run check`** (validates the template layout)

## Tech Stack

- **`AGENTS.md`**: single source of truth (no codegen for the user’s repo, questions and pointers only)
- **`.cursor/rules/rubber-duck-learning.mdc`**: Cursor always-on rule
- **`.claude/skills/rubber-duck-learning/`**: Claude Code **`/rubber-duck-learning`** skill
- **`CLAUDE.md` / `GEMINI.md`**: short entrypoints that point at `AGENTS.md`

## How It Works

1. **Grounding**: the agent reads **`AGENTS.md`** and uses repo tools in a read-only way. Hints should point at real paths or search patterns.
2. **One turn, one focus**: each reply is **one** clarifying question and **up to three** look-here bullets (`path`, optional line range, or a symbol / `rg` pattern).
3. **Hypotheses, not authority**: “what would falsify this?” beats sounding sure about files it never opened.
4. **You keep the keyboard**: no big pasted-in “here is the fix” blocks. You apply the changes.

## Use Cases

- **Debugging without handing off the editor**: questions and pointers instead of silent bulk edits.
- **Onboarding**: learn a codebase from grounded hints instead of auto-generated rewrites.
- **Rubber ducking with structure**: when a one-shot answer is not enough.

## Not Intended For

- **Full auto-implementation**: if you want the agent to write large patches for you, use a different ruleset. This one is **navigator-only**.
- **Made-up paths**: agents following `AGENTS.md` should not invent file paths they have not checked.
- **Bypassing policy**: your team’s license, security, and acceptable-use rules still apply.

## Project Structure

```
.
├── AGENTS.md                              # Agent instructions (single source of truth)
├── CLAUDE.md                              # Claude Code pointer + skill name
├── GEMINI.md                              # Gemini CLI pointer
├── LICENSE
├── package.json                           # npm script: check (optional)
├── .cursor/rules/rubber-duck-learning.mdc
├── .claude/skills/rubber-duck-learning/SKILL.md
└── scripts/
    ├── check-setup.mjs                    # Validates files + skill slug consistency
    └── sync-agent-rules.sh                # Sanity check; reminds you to keep entrypoints in sync
```

## Commands

```bash
npm run check # optional: verify template layout (needs Node 18+)
node scripts/check-setup.mjs       # same, without npm
bash scripts/sync-agent-rules.sh   # verify AGENTS.md exists; sync reminder
```

### If using docker

This template does not ship Docker or Compose. Run everything from your IDE or agent CLI on your machine.

## Updating for Other Platforms

| What                 | Source of truth | Sync command                       |
| -------------------- | --------------- | ---------------------------------- |
| Project instructions | `AGENTS.md`     | `bash scripts/sync-agent-rules.sh` |

After you edit **`AGENTS.md`**, update **`CLAUDE.md`**, **`GEMINI.md`**, **`.cursor/rules/`**, and **`.claude/skills/`** so they stay aligned. The shell script does not regenerate those files for you. It only checks that `AGENTS.md` is there.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=EvanGruhlkey/rubber-duck-learning&type=Date)](https://star-history.com/#EvanGruhlkey/rubber-duck-learning&Date)

## License

MIT
