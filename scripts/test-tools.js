#!/usr/bin/env node
/*
  Test the maths of every tool against its check cases. Node built-ins only.

      node scripts/test-tools.js                       every tool on the map
      node scripts/test-tools.js signals/some-tool.html   one tool

  A tool keeps its maths in   <script id="maths">var MATHS = { ... };</script>
  and its check cases in      <script type="application/json" id="check-cases">[ ... ]</script>

  The maths block is run on its own, with no page behind it, so a function that touches the DOM fails here.
  A check case is  { "fn": "name", "args": [...], "expect": value, "tol": 1e-9, "pick": "a.b", "note": "..." }
    expect   a number, string, boolean, null, list or object. In an object, only the keys named are compared.
    tol      how far a number may be off, as an absolute error or relative to its size (default 1e-9)
    pick     optional: compare this dotted path inside the result instead of the whole result
    "Infinity", "-Infinity" and "NaN" stand for those numbers, in args and in expect.
  The format is documented in docs/tools.md.
*/
"use strict";

const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const ROOT = path.resolve(__dirname, "..");

function block(html, id) {
  const hit = new RegExp('<script\\b[^>]*\\bid="' + id + '"[^>]*>([\\s\\S]*?)</script>').exec(html);
  return hit ? hit[1] : null;
}

function toolsOnTheMap() {
  const found = new Set();
  (function walk(dir) {
    if (!fs.existsSync(dir)) return;
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) walk(full);
      else if (entry.name.endsWith(".json") && entry.name !== "renames.json") {
        const data = JSON.parse(fs.readFileSync(full, "utf8"));
        for (const topic of data.topics || []) for (const tool of topic.tools || []) if (tool.endsWith(".html")) found.add(tool);
      }
    }
  })(path.join(ROOT, "map"));
  return Array.from(found).sort();
}

const SPECIAL = { Infinity: Infinity, "-Infinity": -Infinity, NaN: NaN };
function revive(v) {
  if (typeof v === "string" && Object.prototype.hasOwnProperty.call(SPECIAL, v)) return SPECIAL[v];
  if (Array.isArray(v)) return v.map(revive);
  if (v && typeof v === "object") { const o = {}; for (const k of Object.keys(v)) o[k] = revive(v[k]); return o; }
  return v;
}

// Does `got` match `want`? Returns "" when it does, otherwise a short reason.
function differ(got, want, tol, where) {
  if (typeof want === "number") {
    if (typeof got !== "number") return where + ": expected a number, got " + JSON.stringify(got);
    if (Number.isNaN(want)) return Number.isNaN(got) ? "" : where + ": expected NaN, got " + got;
    if (!Number.isFinite(want)) return got === want ? "" : where + ": expected " + want + ", got " + got;
    return Math.abs(got - want) <= tol * Math.max(1, Math.abs(want), Math.abs(got)) ? "" : where + ": expected " + want + ", got " + got;
  }
  if (Array.isArray(want)) {
    if (!Array.isArray(got) && !(got && typeof got.length === "number")) return where + ": expected a list";
    if (got.length !== want.length) return where + ": expected " + want.length + " items, got " + got.length;
    for (let i = 0; i < want.length; i++) { const d = differ(got[i], want[i], tol, where + "[" + i + "]"); if (d) return d; }
    return "";
  }
  if (want && typeof want === "object") {
    if (!got || typeof got !== "object") return where + ": expected an object, got " + JSON.stringify(got);
    for (const k of Object.keys(want)) { const d = differ(got[k], want[k], tol, where + "." + k); if (d) return d; }
    return "";
  }
  return got === want ? "" : where + ": expected " + JSON.stringify(want) + ", got " + JSON.stringify(got);
}

function testTool(tool) {
  const failures = [];
  const file = path.join(ROOT, tool);
  if (!fs.existsSync(file)) return { cases: 0, failures: [tool + ": the file does not exist"] };
  const html = fs.readFileSync(file, "utf8");
  const maths = block(html, "maths"), casesText = block(html, "check-cases");
  if (maths === null) return { cases: 0, failures: [tool + ': no <script id="maths"> block'] };
  if (casesText === null) return { cases: 0, failures: [tool + ': no <script type="application/json" id="check-cases"> block'] };
  let cases;
  try { cases = JSON.parse(casesText); } catch (err) { return { cases: 0, failures: [tool + ": the check cases are not valid JSON: " + err.message] }; }
  const sandbox = {};
  try {
    vm.runInNewContext(maths, sandbox, { filename: tool + "#maths", timeout: 5000 });
  } catch (err) {
    return { cases: 0, failures: [tool + ": the maths block does not run on its own: " + err.message] };
  }
  const M = sandbox.MATHS;
  if (!M || typeof M !== "object") return { cases: 0, failures: [tool + ": the maths block must define `var MATHS = { ... }`"] };
  cases.forEach((c, i) => {
    const label = tool + " case " + (i + 1) + " (" + c.fn + ")";
    if (typeof M[c.fn] !== "function") { failures.push(label + ": MATHS." + c.fn + " is not a function"); return; }
    let got;
    try { got = M[c.fn].apply(null, revive(c.args || [])); } catch (err) { failures.push(label + ": threw " + err.message); return; }
    if (c.pick) for (const key of String(c.pick).split(".")) got = got == null ? undefined : got[key];
    const d = differ(got, revive(c.expect), typeof c.tol === "number" ? c.tol : 1e-9, "result");
    if (d) failures.push(label + ": " + d + (c.note ? "   [" + c.note + "]" : ""));
  });
  return { cases: cases.length, failures };
}

const asked = process.argv.slice(2);
const tools = asked.length ? asked : toolsOnTheMap();
let total = 0, failed = 0;
for (const tool of tools) {
  const result = testTool(tool);
  total += result.cases;
  failed += result.failures.length;
  for (const line of result.failures) console.log("FAIL  " + line);
}
console.log(failed ? failed + " failure(s) in " + tools.length + " tool(s)." : total + " check cases pass in " + tools.length + " tool(s).");
process.exit(failed ? 1 : 0);
