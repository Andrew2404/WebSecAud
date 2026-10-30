#!/usr/bin/env node
"use strict";

/**
 * Reproduce the offline workbook's import and release-gate unit checks.
 *
 * Usage:
 *   node scripts/test_workbook.cjs
 *   node scripts/test_workbook.cjs assets/security-audit.html
 *
 * Requires Node.js with structuredClone and TextEncoder (Node 18+).
 * Uses only built-in modules; no packages, server, network, or live tests.
 * The built HTML is the code under test. DOM initialization is omitted in this
 * harness so the pure import/gate functions can be exercised. Browser rendering,
 * actual downloads, storage, accessibility, and print remain separate checks.
 */

const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const crypto = require("node:crypto");
const assert = require("node:assert/strict");

const candidates = [
  path.resolve(__dirname, "../website-security-audit/assets/security-audit.html"),
  path.resolve(__dirname, "../assets/security-audit.html")
];
const htmlPath = process.argv[2] ? path.resolve(process.argv[2]) : candidates.find(file => fs.existsSync(file));
if (!htmlPath || !fs.existsSync(htmlPath)) {
  process.stderr.write("Usage: node scripts/test_workbook.cjs PATH/TO/security-audit.html\nBuild the HTML before running these tests.\n");
  process.exit(2);
}
const html = fs.readFileSync(htmlPath, "utf8");
const catalogMatch = html.match(/<script type="application\/json" id="catalog-data">([\s\S]*?)<\/script>/);
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
assert.ok(catalogMatch, "Embedded catalog script was found");
assert.ok(scriptMatch, "Workbook executable script was found");
const catalog = JSON.parse(catalogMatch[1]);
const executable = scriptMatch[1];
const logic = executable.replace(/\n  initialize\(\);\s*(\}\)\(\);)\s*$/, "\n$1");
assert.notEqual(logic, executable, "Only the final DOM initialization call was omitted");
const sandbox = {
  document: {getElementById(id) {
    assert.equal(id, "catalog-data", "Pure harness must not access rendered UI");
    return {textContent: catalogMatch[1]};
  }},
  window: {},
  TextEncoder
};
vm.createContext(sandbox);
vm.runInContext(logic, sandbox, {filename: path.basename(htmlPath), timeout: 5000});
const api = sandbox.window.AuditWorkbook;
let assertions = 0;
function ok(value, message) {
  assert.ok(value, message);
  assertions++;
}
function rejected(value, message) {
  assert.throws(() => api.parseImport(typeof value === "string" ? value : JSON.stringify(value)), undefined, message);
  assertions++;
}

const digest = crypto.createHash("sha256").update(executable).digest("base64");
ok(html.includes("script-src 'sha256-" + digest + "'"), "CSP authorizes exactly the embedded executable script");
ok(!/<script\s+[^>]*\bsrc\s*=|<link\s+[^>]*\bhref\s*=/i.test(html), "Workbook has no external script or stylesheet dependencies");
const criticalIndex = catalog.controls.findIndex(control => ["Critical", "High"].includes(control.priority));
const mediumIndex = catalog.controls.findIndex(control => control.priority === "Medium");
assert.ok(criticalIndex >= 0 && mediumIndex >= 0 && catalog.controls.length >= 2, "Fixture catalog needs a Critical/High and a Medium control");
const count = catalog.controls.length;
const base = JSON.parse(JSON.stringify(api.snapshot()));
const unchangedRecords = JSON.stringify(base.controls);
let imported = api.parseImport(JSON.stringify(base));
let gate = api.evaluate(imported.audit, imported.records, "2026-10-29");
ok(gate.blocked && gate.unresolved.length === count && gate.passed === 0, "Fresh audit is blocked and entirely untested");
ok(base.controls.every(record => record.status === "Untested" && record.applicability === "Unreviewed" && record.findingSeverity === "Unassessed"), "Fresh statuses and severity never imply a pass");

function ready() {
  const value = structuredClone(base);
  for (const key of Object.keys(value.audit)) value.audit[key] = "synthetic scope fixture";
  value.audit.date = "2026-10-29";
  for (const record of value.controls) {
    record.applicability = "Applicable";
    record.status = "Pass";
    record.evidence = "Synthetic fixture result reference; not real audit evidence";
  }
  return value;
}
function evaluate(value) {
  const parsed = api.parseImport(JSON.stringify(value));
  return api.evaluate(parsed.audit, parsed.records, "2026-10-29");
}
function mediumFinding(value, severity = "Unassessed", status = "Fail") {
  const record = value.controls[mediumIndex];
  record.status = status;
  record.findingSeverity = severity;
  record.notes = "Synthetic impact and remediation; retest pending or residual risk recorded";
  return record;
}

let value = ready();
ok(!evaluate(value).blocked && evaluate(value).passed === count, "Evidence-supported passes clear only automatic blockers");
value = ready();
value.controls[criticalIndex].evidence = " ";
ok(evaluate(value).blocked, "Pass without evidence blocks");
value = ready();
value.audit.authorization = "";
ok(evaluate(value).blocked, "Missing scope authorization blocks");
value = ready();
mediumFinding(value);
ok(evaluate(value).blocked, "A Medium-priority finding with unassessed severity blocks");
for (const severity of ["High", "Critical"]) {
  value = ready();
  mediumFinding(value, severity);
  ok(evaluate(value).blocked, severity + " finding blocks independently of control priority");
}
value = ready();
mediumFinding(value, "Low");
ok(!evaluate(value).blocked && evaluate(value).lowerGaps.length === 1, "Low finding remains listed for human review");
value.controls[mediumIndex].notes = "";
ok(evaluate(value).blocked, "A finding without impact/remediation notes remains incomplete");
value = ready();
let risk = mediumFinding(value, "Medium", "Accepted risk");
risk.riskOwner = "Synthetic accountable role";
risk.riskRationale = "Synthetic acceptance rationale";
risk.riskExpiry = "2026-10-28";
ok(evaluate(value).blocked, "Expired acceptance blocks");
risk.riskExpiry = "2026-12-01";
ok(!evaluate(value).blocked && evaluate(value).accepted.length === 1 && evaluate(value).passed === count - 1, "Valid Medium acceptance remains a risk, never a pass");
risk.findingSeverity = "Critical";
ok(evaluate(value).blocked, "Critical accepted risk blocks");
risk.findingSeverity = "Medium";
risk.riskOwner = "";
ok(evaluate(value).blocked, "Acceptance without a named owner blocks");
value = ready();
value.controls[criticalIndex].status = "Untested";
ok(evaluate(value).blocked, "Applicable untested Critical/High control blocks");
value.controls[criticalIndex].status = "Blocked";
ok(evaluate(value).blocked, "A blocked Critical/High test blocks a release recommendation");
value = ready();
value.controls[criticalIndex].applicability = "Not applicable";
value.controls[criticalIndex].status = "Untested";
value.controls[criticalIndex].notes = "";
ok(evaluate(value).blocked, "Not applicable without rationale blocks");
value.controls[criticalIndex].notes = "No applicable feature exists in this synthetic scoped build";
ok(!evaluate(value).blocked, "A reasoned not-applicable exclusion is permitted");
value.controls[criticalIndex].status = "Pass";
ok(evaluate(value).blocked, "Inconsistent not-applicable/pass record blocks");

value = ready();
value.controls[0].evidence = '<svg onload="globalThis.XSS=true"></svg><script>alert(1)</script>';
value.audit.project = '</script><img src=x onerror=alert(1)>';
imported = api.parseImport(JSON.stringify(value));
ok(imported.records.get(value.controls[0].id).evidence === value.controls[0].evidence && imported.audit.project === value.audit.project, "Markup is retained as plain string data");
value = ready(); value.controls[1] = structuredClone(value.controls[0]); rejected(value, "Duplicate IDs rejected");
value = ready(); value.controls[0].id = "UNKNOWN-CONTROL"; rejected(value, "Unknown IDs rejected");
value = ready(); value.controls.pop(); rejected(value, "Missing controls rejected");
value = ready(); value.extra = "x"; rejected(value, "Unknown fields rejected");
value = ready(); value.controls[0].status = "Secure"; rejected(value, "Unknown status rejected");
value = ready(); value.controls[0].findingSeverity = "P0"; rejected(value, "Unknown severity rejected");
value = ready(); value.controls[0].notes = {html: "x"}; rejected(value, "Object-valued text rejected");
value = ready(); value.controls[0].notes = "a".repeat(20001); rejected(value, "Oversized text rejected");
value = ready(); value.controls[0].notes = "a\u0000b"; rejected(value, "NUL characters rejected");
value = ready(); value.schemaVersion = base.schemaVersion + 1; rejected(value, "Unsupported schema version rejected");
value = ready(); value.catalogVersion += "-incompatible"; rejected(value, "Catalog mismatch rejected");
value = ready(); value.audit.date = "2026-02-31"; rejected(value, "Invalid calendar date rejected");
value = ready(); value.exportedAt = "2026-02-31T00:00:00.000Z"; rejected(value, "Invalid timestamp rejected");
value = ready(); value.controls[0].riskExpiry = "2026-13-01"; rejected(value, "Invalid risk expiry rejected");
value = ready(); rejected(JSON.stringify(value).replace('"project":', '"__proto__":{},"project":'), "Prototype pollution key rejected");
value = ready(); rejected(JSON.stringify(value).replace('"project":', '"constructor":{},"project":'), "Constructor key rejected");
rejected(" ".repeat(2 * 1024 * 1024 + 1), "2 MiB import cap enforced");
ok(JSON.stringify(api.snapshot().controls) === unchangedRecords, "Valid and invalid import validation does not mutate the current audit");

process.stdout.write(JSON.stringify({
  passed: assertions,
  controls: count,
  file: path.basename(htmlPath),
  scope: "Offline import-schema and release-gate unit checks; DOM/print tests remain separate; no live security testing"
}) + "\n");
