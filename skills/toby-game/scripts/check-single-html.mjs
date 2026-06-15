#!/usr/bin/env node
// check-single-html.mjs — the rote pass on a one-file game. it does not judge taste; it catches the
// three bugs that ship a dead screen and waste a playtest: a syntax error, a handler wired to an id
// that never existed, and a stray external <script> that breaks the open-by-double-click promise.
//
//   node check-single-html.mjs path/to/game.html [--emit script.js]
//
// --emit writes the extracted inline script to a file, so you can eval the fenced CORE in a node
// harness and run bots against it headless. the id check is a heuristic (regex, largest-script): treat
// a dead-id warning as a reason to look, and read the matches before trusting one.

import { readFileSync, writeFileSync } from "node:fs";
import vm from "node:vm";

const file = process.argv[2];
if (!file) { console.error("usage: node check-single-html.mjs <file.html> [--emit out.js]"); process.exit(2); }
const emitTo = process.argv.includes("--emit") ? process.argv[process.argv.indexOf("--emit") + 1] : null;

const html = readFileSync(file, "utf8");
const problems = [];

// every <script>; split inline from external by the presence of a src attribute
const tags = [...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)];
const external = tags.filter(m => /\bsrc\s*=/i.test(m[1]));
const inline = tags.filter(m => !/\bsrc\s*=/i.test(m[1])).map(m => m[2]);
const game = inline.slice().sort((a, b) => b.length - a.length)[0] || ""; // largest = the game logic

// the single-file promise: a loaded script must be a pinned https module (three.js and friends), not a local path
for (const m of external) {
  const src = (m[1].match(/\bsrc\s*=\s*["']([^"']+)["']/i) || [])[1] || "";
  if (!/^https:\/\//.test(src)) problems.push(`external script is not a pinned https url: ${src || "(no src)"}`);
}

// syntax: a stray paren ships a blank canvas. vm.Script throws on the same errors `node --check` would.
if (!game) problems.push("no inline <script> found — nothing to check");
else {
  try { new vm.Script(game, { filename: "game-inline.js" }); }
  catch (e) { problems.push(`syntax error in the inline script: ${e.message}`); }
}

// dead handlers: every id the script reaches for must exist somewhere in the html
const ids = new Set([...html.matchAll(/\bid\s*=\s*["']([^"']+)["']/g)].map(m => m[1]));
const reached = new Set();
for (const m of game.matchAll(/getElementById\(\s*["']([^"']+)["']\s*\)/g)) reached.add(m[1]);
for (const m of game.matchAll(/\$\(\s*["']([A-Za-z][\w-]*)["']\s*\)/g)) reached.add(m[1]);   // $("id") shorthand
for (const m of game.matchAll(/(?:\$|querySelector(?:All)?)\(\s*["']#([\w-]+)["']\s*\)/g)) reached.add(m[1]); // "#id" form
const dead = [...reached].filter(id => !ids.has(id));
for (const id of dead) problems.push(`handler reaches #${id}, which is not an id in the html (dead/stale handler)`);

if (emitTo && game) {
  writeFileSync(emitTo, game);
  console.log(`wrote inline script to ${emitTo} (${game.length} bytes) — eval the fenced CORE for headless bots`);
}

console.log(`inline scripts: ${inline.length}  external: ${external.length}  ids: ${ids.size}  handler ids: ${reached.size}`);
if (problems.length) { console.error("\nFAIL:\n  " + problems.join("\n  ")); process.exit(1); }
console.log("\nok — syntax parses, every handler id exists, one file holds it");
