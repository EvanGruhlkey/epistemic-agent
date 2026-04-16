#!/usr/bin/env node
/**
 * Verifies required files exist and the Claude skill slug matches AGENTS.md / SKILL.md.
 * No dependencies; requires Node 18+.
 *
 * When you rename the skill, update SKILL_SLUG below and the paths under .cursor/ and .claude/.
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const SKILL_SLUG = "rubber-duck-learning";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, "..");

function die(msg) {
  console.error(`check-setup: ${msg}`);
  process.exit(1);
}

function read(rel) {
  return fs.readFileSync(path.join(root, rel), "utf8");
}

function mustExist(rel) {
  const p = path.join(root, rel);
  if (!fs.existsSync(p)) die(`missing file: ${rel}`);
}

const required = [
  "AGENTS.md",
  "README.md",
  "CLAUDE.md",
  "GEMINI.md",
  "LICENSE",
  "package.json",
  `.cursor/rules/${SKILL_SLUG}.mdc`,
  `.claude/skills/${SKILL_SLUG}/SKILL.md`,
  "scripts/sync-agent-rules.sh",
  "scripts/check-setup.mjs",
];

for (const rel of required) mustExist(rel);

const skillPath = `.claude/skills/${SKILL_SLUG}/SKILL.md`;
const skillRaw = read(skillPath);
const fm = skillRaw.match(/^---\r?\n([\s\S]*?)\r?\n---/);
if (!fm) die(`${skillPath}: expected YAML frontmatter`);

const nameMatch = fm[1].match(/^name:\s*(.+)$/m);
if (!nameMatch) die(`${skillPath}: frontmatter needs name:`);
const skillName = nameMatch[1].trim();
if (!/^[a-z][a-z0-9-]*$/.test(skillName)) {
  die(`${skillPath}: name must be a lowercase slug, got ${JSON.stringify(skillName)}`);
}

if (skillName !== SKILL_SLUG) {
  die(
    `${skillPath}: name is ${JSON.stringify(skillName)} but scripts/check-setup.mjs expects SKILL_SLUG ${JSON.stringify(SKILL_SLUG)}`,
  );
}

const afterFm = skillRaw.slice(fm[0].length).trimStart();
const h1 = afterFm.match(/^#\s+(.+)$/m);
if (!h1 || h1[1].trim() !== `/${skillName}`) {
  die(`${skillPath}: first # heading should be # /${skillName}`);
}

const agents = read("AGENTS.md");
if (!agents.includes(`/${skillName}`)) die("AGENTS.md: should mention the /command");
if (!agents.includes(`.claude/skills/${skillName}/SKILL.md`)) {
  die("AGENTS.md: should reference the skill path");
}
if (!agents.includes(`.cursor/rules/${skillName}.mdc`)) {
  die("AGENTS.md: should reference the Cursor rule path");
}

const claude = read("CLAUDE.md");
if (!claude.includes(`/${skillName}`)) die("CLAUDE.md: should mention the slash command");

console.log("check-setup: OK (layout and skill slug look consistent).");
