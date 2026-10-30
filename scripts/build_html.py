#!/usr/bin/env python3
"""Build the portable, offline audit workbook from the reviewed control catalog.

Usage: python scripts/build_html.py [catalog.json] [output.html]
Only Python's standard library is required. No requests or tests are performed.
"""

from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path
import sys


PAGE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<meta http-equiv="Content-Security-Policy" content="__CSP__">
<title>Website security audit · Evidence workbook</title>
<style>
:root{--navy:#102d40;--ink:#142f41;--muted:#4d6370;--teal:#006f68;--pale:#e7f3ef;--amber:#755200;--amber-bg:#fff2cc;--red:#a21d27;--red-bg:#fff0f1;--line:#c8d6dc;--paper:#fff;--canvas:#f2f6f6;--focus:#005fcc;--radius:12px}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--ink);background:var(--canvas);font:16px/1.55 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}a{color:#005e7a;text-underline-offset:.18em;overflow-wrap:anywhere}button,input,select,textarea{font:inherit}button,a,input,select,textarea,summary{touch-action:manipulation}button,input,select,textarea{border:1px solid #8a9fa9;border-radius:6px}input,select,textarea{width:100%;padding:.6rem .7rem;color:var(--ink);background:#fff;min-height:44px}textarea{resize:vertical;min-height:94px}input[type=checkbox]{width:20px;min-height:20px;margin:0;flex:0 0 20px;accent-color:var(--teal)}button{padding:.62rem .85rem;min-height:44px;background:#fff;color:var(--ink);cursor:pointer;font-weight:650}button:hover{background:#e8f0f1}button.primary{background:var(--teal);border-color:var(--teal);color:#fff}button.primary:hover{background:#005a55}button.danger{color:var(--red)}:focus-visible{outline:3px solid var(--focus);outline-offset:3px}.skip{position:absolute;left:1rem;top:-6rem;z-index:20;padding:.8rem 1rem;background:white}.skip:focus{top:1rem}.wrap{max-width:1360px;margin:auto;padding:0 32px}header{background:var(--navy);color:#fff;padding:44px 0 36px;border-bottom:5px solid #24ad98}.eyebrow{font-size:.78rem;font-weight:750;letter-spacing:.15em;text-transform:uppercase;color:#a8e1d6;margin:0 0 12px}.heading-line{display:flex;justify-content:space-between;align-items:start;gap:24px}h1{font-size:clamp(2rem,4vw,3.1rem);line-height:1.12;letter-spacing:-.04em;margin:0 0 16px;max-width:850px}header .intro{max-width:840px;color:#dbe8ef;margin:0;font-size:1.08rem}.edition{font-size:.82rem;border:1px solid #64818f;border-radius:7px;padding:10px 13px;white-space:nowrap}.edition span{display:block;color:#d1e1e8}main{padding-top:24px!important;padding-bottom:50px!important}.section{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:24px;margin-bottom:20px}h2{font-size:1.35rem;line-height:1.25;margin:0 0 12px;letter-spacing:-.02em}h3{font-size:1.03rem;margin:0 0 6px}p{margin:0 0 12px}p:last-child{margin-bottom:0}.muted,.help{color:var(--muted)}.help{font-size:.87rem;line-height:1.45}.section-intro{max-width:980px}.inline-note{padding:12px 15px;background:var(--amber-bg);border-left:4px solid #b37e06;color:#503a06;border-radius:3px;font-size:.94rem}.inline-note strong{color:#4c3200}.safety-grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}.safety-list{margin:0;padding-left:1.25rem}.safety-list li{margin:.35rem 0}details.policy{margin-top:15px}details.policy summary{font-weight:700;color:#005f61;cursor:pointer;padding:8px 0}.policy-content{padding:8px 0 0}.form-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.field.wide{grid-column:span 3}.field.half{grid-column:span 1}.field label{display:block;font-weight:650;margin-bottom:5px;font-size:.92rem}.field label .optional{font-weight:400;color:var(--muted)}.field .help{margin:5px 0 0}.scope{margin-top:20px}#scope-summary{cursor:pointer;font-weight:700;padding:4px 0}.scope-body{padding-top:18px}.scope-body .form-grid+.form-grid{margin-top:16px}.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-bottom:16px}.metric{padding:17px 18px;background:white;border:1px solid var(--line);border-radius:10px}.metric .number{display:block;font-size:2rem;font-weight:750;line-height:1.1;letter-spacing:-.03em}.metric .label{display:block;font-size:.84rem;color:var(--muted);margin-top:7px}.metric.blocked .number{color:var(--red)}.gate{background:#fff;border:1px solid var(--line);border-left:5px solid var(--amber);border-radius:9px;padding:20px;margin-bottom:20px}.gate.blocked{border-left-color:var(--red)}.gate.review{border-left-color:var(--amber)}.gate h2{font-size:1.2rem}.gate ul{margin:10px 0 0;padding-left:1.25rem}.gate ul li{margin:.3rem 0}.gate .subtle{font-size:.87rem;color:var(--muted);margin-top:12px}.toolbar{display:flex;gap:10px;flex-wrap:wrap;align-items:center}.storage-row{display:flex;gap:10px;align-items:flex-start;margin-top:16px}.storage-row label{font-size:.91rem}.toolbar-note{margin-top:12px}.notice{margin:12px 0 0;padding:12px 14px;border-radius:6px;background:var(--pale);border:1px solid #7cae9f}.notice.error{background:var(--red-bg);border-color:#d39aa0;color:#7e1520}.notice:empty{display:none}.filter-panel{padding-bottom:18px}.filters{display:grid;grid-template-columns:2fr 1.25fr 1fr 1.1fr 1.25fr;gap:12px}.filter-footer{display:flex;align-items:center;justify-content:space-between;gap:15px;margin-top:16px}.filter-footer p{font-size:.9rem;margin:0}.small-actions{display:flex;gap:8px;flex-wrap:wrap}.small-actions button{font-size:.86rem;padding:.45rem .7rem;min-height:38px}.catalog-heading{display:flex;justify-content:space-between;gap:16px;align-items:center;margin:28px 0 14px}.catalog-heading h2{margin:0}.catalog-heading p{margin:0;font-size:.86rem;color:var(--muted)}.control{margin-bottom:12px;background:#fff;border:1px solid var(--line);border-radius:10px;overflow:clip}.control>summary{list-style:none;cursor:pointer;padding:18px 20px;display:grid;grid-template-columns:92px 1fr auto;align-items:start;gap:14px}.control>summary::-webkit-details-marker{display:none}.control>summary::before{content:"+";font-weight:700;border:1px solid #829ba8;border-radius:4px;width:20px;height:20px;display:none;align-items:center;justify-content:center}.control[open]>summary{border-bottom:1px solid var(--line);background:#f7faf9}.control .id{font-size:.78rem;font-weight:750;letter-spacing:.04em;color:#4a6776;padding-top:3px}.title-text{font-size:1.03rem;font-weight:700;line-height:1.45}.title-sub{font-size:.79rem;color:var(--muted);margin-top:3px;font-weight:400}.badge-group{display:flex;gap:7px;align-items:center;justify-content:flex-end;flex-wrap:wrap;max-width:280px}.badge{font-size:.73rem;border-radius:4px;padding:3px 7px;border:1px solid #aabdc7;background:#f2f6f7;font-weight:650;white-space:nowrap}.badge.critical,.badge.fail{color:#82111d;background:#fff0f1;border-color:#d99ba3}.badge.high,.badge.blocked,.badge.risk{color:#644000;background:#fff3d5;border-color:#c9b272}.badge.pass{color:#00594c;background:#e6f4ed;border-color:#79ac98}.badge.medium{color:#324f63;background:#edf3f9;border-color:#a3b7c9}.badge.invalid{color:#82111d;background:#fff0f1;border-color:#d99ba3}.chevron{font-size:1.1rem;color:#3c6676;margin-left:2px}.control[open] .chevron{transform:rotate(180deg)}.control-body{padding:20px}.method-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}.method-block{font-size:.91rem}.method-block p{white-space:pre-wrap;overflow-wrap:anywhere}.method-block h3{font-size:.8rem;text-transform:uppercase;letter-spacing:.06em;color:#476572;margin-bottom:6px}.method-block.full{grid-column:span 2}.control-sources{font-size:.83rem;margin:14px 0 18px;padding-bottom:17px;border-bottom:1px solid var(--line)}.control-sources a{margin-right:14px}.record-grid{display:grid;grid-template-columns:1fr 1fr;gap:15px}.record-grid .field.full{grid-column:span 2}.risk-grid{display:grid;grid-template-columns:1fr 1fr;gap:15px;margin-top:15px;padding-top:14px;border-top:1px dashed var(--line)}.risk-grid .field.full{grid-column:span 2}.record-warning{font-size:.88rem;color:#8a1720;margin-top:10px}.record-warning:empty{display:none}.source-list{padding-left:1.5rem;font-size:.91rem}.source-list li{margin:0 0 14px;padding-left:4px;overflow-wrap:anywhere}.source-list .source-meta{display:block;color:var(--muted);font-size:.83rem}.source-url{display:block;font-size:.82rem}.footer{font-size:.85rem;color:var(--muted);border-top:1px solid var(--line);padding-top:20px;margin-top:25px}.empty{padding:32px;text-align:center;border:1px dashed #8ba0ac;border-radius:10px;background:white}.print-only,.print-value{display:none}[hidden]{display:none!important}.filtered-out{display:none}.screenreader-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
@media(max-width:1000px){.filters{grid-template-columns:repeat(2,minmax(0,1fr))}.filters>.field:first-child{grid-column:span 2}.form-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.field.wide{grid-column:span 2}.heading-line{display:block}.edition{display:inline-block;margin-top:20px}.control>summary{grid-template-columns:80px 1fr}.badge-group{grid-column:2;justify-content:flex-start;max-width:none}.metrics{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:640px){.wrap{padding:0 16px}header{padding:30px 0 26px}.section{padding:18px}.safety-grid,.form-grid,.method-grid,.record-grid,.risk-grid{grid-template-columns:1fr}.field.wide,.field.half,.method-block.full,.record-grid .field.full,.risk-grid .field.full{grid-column:auto}.filters{grid-template-columns:1fr}.filters>.field:first-child{grid-column:auto}.filter-footer,.catalog-heading{display:block}.small-actions{margin-top:12px}.control>summary{padding:15px;grid-template-columns:1fr;gap:7px}.badge-group{grid-column:auto;justify-content:flex-start}.control-body{padding:16px}.control .id{padding:0}.metric{padding:14px}.metric .number{font-size:1.7rem}.toolbar button{flex:1 1 40%}.catalog-heading p{margin-top:6px}h1{font-size:2.2rem}.method-grid{gap:15px}.gate{padding:16px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{@page{size:auto;margin:16mm}body{font:10pt/1.4 sans-serif;background:#fff;color:#000}.wrap{max-width:none;padding:0}header{background:#fff;color:#000;border-bottom:2pt solid #000;padding:0 0 12pt}header .intro,.eyebrow,.edition span{color:#222}h1{font-size:26pt;max-width:none}.eyebrow{font-size:8pt}.edition{border:1pt solid #999;padding:5pt;display:inline-block;margin-top:8pt;font-size:8pt}.heading-line{display:block}main{padding:12pt 0!important}.no-print,.filter-panel,.toolbar,.storage-row,.toolbar-note,#notice,.skip,.chevron,.record-warning,input,textarea,select,button{display:none!important}.print-only,.print-value{display:block!important}.print-value{white-space:pre-wrap;overflow-wrap:anywhere;font-weight:400;min-height:12pt;margin:3pt 0 8pt}.section,.gate{border:1pt solid #aaa;border-radius:0;padding:10pt;margin-bottom:12pt}.safety-grid,.form-grid,.method-grid,.record-grid,.risk-grid{display:block}.field,.method-block{margin-bottom:9pt}.field label,.method-block h3{font-size:9pt;color:#222}.field .help{display:none}.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:6pt}.metric{border:1pt solid #aaa;border-radius:0;padding:7pt}.metric .number{font-size:18pt;color:#000!important}.metric .label{font-size:8pt;color:#222}.control,.control.filtered-out{display:block!important;border:1pt solid #999;border-radius:0;margin:0 0 12pt;overflow:visible;break-inside:auto}.control>summary{display:block!important;padding:9pt;border-bottom:1pt solid #aaa!important;break-after:avoid;background:#fff!important}.control>summary .id{display:inline-block;margin-right:8pt;font-size:8pt}.title-text{display:inline;font-size:11pt}.title-sub{font-size:8pt}.badge-group{display:flex;justify-content:flex-start;margin-top:5pt}.badge{font-size:7pt;border-color:#999!important;background:#fff!important;color:#000!important}.control-body{display:block!important;padding:9pt}.control:not([open])>*:not(summary){display:block!important}.method-block{font-size:9pt}.control-sources{font-size:8pt;margin:6pt 0 9pt;padding-bottom:6pt}.risk-grid{margin-top:8pt;padding-top:8pt}.risk-grid[hidden]{display:none!important}.help,.muted{color:#333}.scope-body,.policy-content{display:block!important;padding-top:8pt}.scope>summary,.policy>summary{font-size:11pt;font-weight:700;list-style:none}.source-list{font-size:8pt}.source-list li{break-inside:avoid}.source-url{font-size:7pt}.source-list .source-meta{color:#333}.footer{font-size:8pt;margin-top:12pt;padding-top:10pt}.catalog-heading{margin:15pt 0 8pt}.catalog-heading h2{font-size:15pt}.catalog-heading p{display:none}h2,h3{break-after:avoid}.inline-note{color:#000;background:#fff;border-left:2pt solid #777;font-size:9pt}.inline-note strong{color:#000}a{color:#000;text-decoration:underline}#empty{display:none!important}.notice{display:none!important}.screenreader-only{display:none!important}}
@media print{.control>summary{break-inside:avoid;break-after:avoid}}
</style>
</head>
<body>
<a class="skip" href="#checklist">Skip to audit controls</a>
<header>
 <div class="wrap">
  <p class="eyebrow">Release assurance / Evidence workbook</p>
  <div class="heading-line"><div><h1>Website security audit</h1><p class="intro">A structured review of the application, its infrastructure, and the business rules that protect people and data. Record what was tested, what happened, and what still needs an answer.</p></div><div class="edition">Catalog <strong id="catalog-version"></strong><span id="catalog-date"></span></div></div>
 </div>
</header>
<main class="wrap" id="main">
 <section class="section" aria-labelledby="start-title">
  <h2 id="start-title">Start with permission and a defined scope</h2>
  <p class="section-intro">This workbook is guidance, not a scanner or a guarantee. Every control begins <strong>Untested</strong>, with applicability <strong>Unreviewed</strong>. A source link or successful scan is not evidence that a control passes.</p>
  <p class="section-intro"><strong>Active audit workflow:</strong> an agent using the companion skill must execute feasible, approved tests that attempt to violate security boundaries and business rules, using the smallest non-destructive proof. Record the actual requests, observations, fixes and retests. Missing tools, accounts or permission remain Blocked. Opening this HTML performs no tests.</p>
  <p class="section-intro"><strong>Maximum effort:</strong> the companion skill asks “Are you ready to get hacked?” with Yes/No and creates a test ledger before execution. Yes alone grants no testing permission: exact owned local/staging targets, accounts, shared traffic budgets, exclusions and stop conditions must be approved. It prohibits real-account brute force and DDoS; separately approved, capped local/staging resilience tests use health-triggered stops. This workbook records evidence; it does not implement that execution gate or run attacks.</p>
  <p class="inline-note"><strong>Safe default:</strong> review code and configuration; test only authorized local or staging systems using synthetic data, test accounts, bounded requests, and a rollback plan. Production, destructive, or availability-impacting tests need explicit scope and approval before execution.</p>
  <details class="policy"><summary>Testing boundaries and release decision rules</summary><div class="policy-content safety-grid"><div><h3>Keep tests controlled</h3><ul class="safety-list"><li>Record exact targets, accounts, allowed actions, request limits, stop signals, and an emergency contact before testing.</li><li>Never collect real secrets, exfiltrate data, charge real cards, spam users, brute-force real accounts, or load-test production.</li><li>Use sandboxes, inert canaries, and stubs. Stop on unexpected access, real data, unintended side effects, instability, or a request outside scope.</li><li>Mark prohibited or unavailable tests Blocked. Record the missing permission or dependency and continue independent authorized review.</li></ul></div><div><h3>Make an evidence-based decision</h3><ul class="safety-list"><li>Unassessed, High, or Critical findings block release regardless of control priority. Critical/High-priority failures, blocked checks, untested checks, and accepted risks also block an ordinary release recommendation while applicable or unresolved.</li><li>Resolve every applicability decision. Not applicable needs a specific rationale. Pass needs evidence tied to the reviewed build.</li><li>Risk acceptance needs a named owner, rationale, and review expiry. It never turns a finding into a pass.</li><li>Lower-priority gaps still need human review. Findings need reproduction, impact, remediation, and retest. No workbook result certifies a site as secure.</li></ul></div></div></details>
  <details class="scope" open><summary id="scope-summary">Audit scope and authorization record</summary><div class="scope-body"><p class="help">All scope fields are required for a reviewable release decision. Record approved boundaries; this document does not grant permission. Use “none” with a reason where appropriate.</p><div class="form-grid" id="audit-fields"></div></div></details>
 </section>
 <section aria-labelledby="decision-title">
  <div class="metrics"><div class="metric blocked"><span class="number" id="count-blockers">0</span><span class="label">Blocking issues to resolve</span></div><div class="metric"><span class="number" id="count-unreviewed">0</span><span class="label">Applicability decisions pending</span></div><div class="metric"><span class="number" id="count-passed">0</span><span class="label">Pass records with evidence</span></div><div class="metric"><span class="number" id="count-total">0</span><span class="label">Controls in this catalog</span></div></div>
  <div class="gate blocked" id="gate"><h2 id="decision-title">Release recommendation blocked</h2><p id="gate-message"></p><ul id="gate-reasons"></ul><p class="subtle">Counts describe recorded review work, not the probability of compromise. A human reviewer must evaluate evidence, unresolved findings, and the actual release scope.</p></div>
 </section>
 <section class="section no-print" aria-labelledby="record-title">
  <h2 id="record-title">Keep the audit record</h2><p class="help">The HTML is the reusable workbook. Your entered records belong in an exported JSON file. Keep evidence references redacted and access-controlled; do not paste credentials, tokens, payment data, or personal information.</p>
  <div class="toolbar"><button class="primary" id="export-button" type="button">Export audit JSON</button><button id="import-button" type="button">Import audit JSON</button><button id="print-button" type="button">Print full audit / Save PDF</button><button id="load-button" type="button">Load browser copy</button><button class="danger" id="reset-button" type="button">Reset this audit</button></div>
  <input type="file" id="import-file" accept="application/json,.json" hidden>
  <div class="storage-row"><input type="checkbox" id="local-save"><label for="local-save">Save audit records in this browser while I work. <span class="help">Off by default. Shared devices can expose stored records. Turning this off removes the saved browser copy.</span></label></div>
  <p class="help toolbar-note">Browser storage can be unavailable for local files. JSON export is the portable backup. Imports replace the current record only after validation and confirmation. Printing always includes every control, regardless of filters.</p>
  <div id="notice" class="notice" role="status" aria-live="polite" aria-atomic="true"></div>
 </section>
 <section class="section filter-panel" aria-labelledby="filter-title"><h2 id="filter-title">Find a control</h2><div class="filters"><div class="field"><label for="search">Search text or control ID</label><input id="search" type="search" placeholder="e.g. webhook, tenant, SVG, restore"></div><div class="field"><label for="domain-filter">Domain</label><select id="domain-filter"><option value="">All domains</option></select></div><div class="field"><label for="priority-filter">Priority</label><select id="priority-filter"><option value="">All priorities</option><option>Critical</option><option>High</option><option>Medium</option></select></div><div class="field"><label for="status-filter">Status</label><select id="status-filter"><option value="">All statuses</option><option>Untested</option><option>Pass</option><option>Fail</option><option>Blocked</option><option>Accepted risk</option></select></div><div class="field"><label for="app-filter">Applicability</label><select id="app-filter"><option value="">All decisions</option><option>Unreviewed</option><option>Applicable</option><option>Not applicable</option></select></div></div><div class="filter-footer"><p id="filter-result" role="status" aria-live="polite"></p><div class="small-actions"><button id="clear-filters" type="button">Clear filters</button><button id="expand-button" type="button">Expand all</button><button id="collapse-button" type="button">Collapse all</button></div></div></section>
 <div class="catalog-heading"><h2 id="checklist" tabindex="-1">Audit controls</h2><p>Open a control to see its test and record evidence.</p></div>
 <p class="print-only">Complete catalog and recorded evidence. Screen filters do not apply to this printed audit. Blank fields and untested controls remain unresolved.</p>
 <div id="controls"></div><p id="empty" class="empty" hidden>No controls match these filters. Clear a filter or try a broader search.</p>
 <section class="section" aria-labelledby="sources-title"><h2 id="sources-title">Primary sources and maintenance</h2><p class="help">Sources support the verification guidance; this catalog is not a complete ASVS requirement mapping or a certification. Check current stack versions, vendor security advisories, dependency advisories, and relevant CVEs for every audit. A finite checklist cannot enumerate every exploit or future vulnerability.</p><ol class="source-list" id="sources"></ol></section>
 <footer class="footer"><p><strong>Evidence over assurance claims.</strong> This document makes no network requests and performs no security tests. Data entered here stays in this tab unless you opt into browser storage, export, print, or follow a source link. Record only the minimum evidence needed and protect exported audits according to their sensitivity.</p><p>CORS policy and binding to <code>0.0.0.0</code> are contextual configuration choices, not automatic vulnerabilities. Assess the intended trust boundary, actual reachability, authentication, and possible impact.</p></footer>
</main>
<script type="application/json" id="catalog-data">__CATALOG__</script>
<script>
__SCRIPT__
</script>
</body>
</html>
'''


SCRIPT = r'''"use strict";
(() => {
  const DATA = JSON.parse(document.getElementById("catalog-data").textContent);
  const FORMAT = "website-security-audit-record";
  const SCHEMA = 1;
  const MAX_FILE_BYTES = 2 * 1024 * 1024;
  const MAX_TEXT = 20000;
  const STORAGE_KEY = "website-security-audit-v1:" + DATA.version;
  const STATUS = ["Untested", "Pass", "Fail", "Blocked", "Accepted risk"];
  const APPLICABILITY = ["Unreviewed", "Applicable", "Not applicable"];
  const SEVERITY = ["Unassessed", "Low", "Medium", "High", "Critical"];
  const RECORD_KEYS = ["id", "applicability", "status", "findingSeverity", "evidence", "notes", "riskOwner", "riskRationale", "riskExpiry"];
  const META = [
    ["project", "Project / application", "text", "Name the application without private client details."],
    ["build", "Build / commit / artifact", "text", "Record the exact release candidate and relevant configuration version."],
    ["environment", "Environment / exact targets", "text", "List authorized local or staging hosts and boundaries."],
    ["tester", "Reviewer / accountable owner", "text", "Use an agreed reviewer name or role identifier."],
    ["date", "Review date", "date", "Date of this audit, not the catalog reference date."],
    ["rateBudget", "Request / size / time budget", "text", "State numeric limits and concurrency for authorized tests."],
    ["authorization", "Authorization and allowed actions", "textarea", "Reference the approver and scope record; distinguish review, staging tests, and explicitly approved exceptions."],
    ["inScope", "In-scope assets, roles and data flows", "textarea", "Include interfaces, integrations, trust boundaries, test identities, and synthetic datasets."],
    ["outOfScope", "Exclusions and blocked work", "textarea", "Document excluded systems or techniques and their effect on confidence."],
    ["rollbackStop", "Rollback, stop criteria and emergency contact", "textarea", "Describe restoration, who can stop testing, and when to stop or escalate."]
  ];
  const META_KEYS = META.map(field => field[0]);
  const byId = new Map(DATA.controls.map(control => [control.id, control]));
  const sourceMap = new Map(DATA.sources.map(source => [source.id, source]));
  const cards = new Map();
  const metaInputs = new Map();
  let audit = Object.fromEntries(META_KEYS.map(key => [key, ""]));
  let records = new Map(DATA.controls.map(control => [control.id, freshRecord(control.id)]));
  let dirty = false;
  let beforePrint = null;

  function freshRecord(id) {
    return {id, applicability:"Unreviewed", status:"Untested", findingSeverity:"Unassessed", evidence:"", notes:"", riskOwner:"", riskRationale:"", riskExpiry:""};
  }
  function node(tag, text, className) {
    const element = document.createElement(tag);
    if (text !== undefined && text !== null) element.textContent = text;
    if (className) element.className = className;
    return element;
  }
  function put(id, value) { document.getElementById(id).textContent = value; }
  function announce(message, error = false) {
    const target = document.getElementById("notice");
    target.className = "notice" + (error ? " error" : "");
    target.textContent = message;
  }
  function createField(key, labelText, kind, help, value, onChange, prefix = "audit") {
    const wrapper = node("div", null, "field");
    const id = prefix + "-" + key;
    const label = node("label", labelText);
    label.htmlFor = id;
    const input = node(kind === "textarea" ? "textarea" : kind === "select" ? "select" : "input");
    input.id = id;
    if (input.tagName === "INPUT") input.type = kind;
    if (kind === "textarea") input.rows = 3;
    if (kind !== "select") input.maxLength = MAX_TEXT;
    input.value = value;
    const printValue = node("div", value || "[Not recorded]", "print-value");
    input.addEventListener("input", () => {
      printValue.textContent = input.value || "[Not recorded]";
      onChange(input.value);
    });
    wrapper.append(label, input, printValue);
    if (help) {
      const description = node("p", help, "help");
      description.id = id + "-help";
      input.setAttribute("aria-describedby", description.id);
      wrapper.append(description);
    }
    return {wrapper, input, printValue};
  }
  function addOptions(select, values) {
    values.forEach(value => {
      const option = node("option", value);
      option.value = value;
      select.append(option);
    });
  }
  function sourceLink(source, short = false) {
    const link = node("a", short ? source.title : source.title);
    link.href = source.url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    return link;
  }
  function buildMeta() {
    const container = document.getElementById("audit-fields");
    META.forEach(([key, label, kind, help]) => {
      const field = createField(key, label, kind, help, audit[key], value => {
        audit[key] = value;
        changed();
      });
      if (kind === "textarea") field.wrapper.classList.add("wide");
      metaInputs.set(key, field);
      container.append(field.wrapper);
    });
  }
  function createControl(control) {
    const record = records.get(control.id);
    const card = node("details", null, "control");
    card.id = "control-" + control.id;
    const summary = node("summary");
    const id = node("span", control.id, "id");
    const text = node("div");
    text.append(node("span", control.title, "title-text"), node("div", control.domain, "title-sub"));
    const badges = node("div", null, "badge-group");
    const priority = node("span", control.priority, "badge " + control.priority.toLowerCase());
    const statusBadge = node("span", record.status, "badge");
    const appBadge = node("span", record.applicability, "badge");
    const chevron = node("span", "⌄", "chevron");
    chevron.setAttribute("aria-hidden", "true");
    badges.append(priority, statusBadge, appBadge, chevron);
    summary.append(id, text, badges);
    card.append(summary);
    const body = node("div", null, "control-body");
    const methods = node("div", null, "method-grid");
    [["Applicability", control.applicability], ["Concrete verification", control.verify], ["Pass criteria", control.pass], ["Evidence to retain", control.evidence]].forEach(([title, content]) => {
      const block = node("section", null, "method-block");
      block.append(node("h3", title), node("p", content));
      methods.append(block);
    });
    const sources = node("div", null, "control-sources");
    sources.append(node("strong", "Sources: "));
    control.sourceIds.forEach(sourceId => sources.append(sourceLink(sourceMap.get(sourceId), true)));
    const fields = new Map();
    const recordGrid = node("div", null, "record-grid");
    const riskGrid = node("div", null, "risk-grid");
    const definitions = [
      ["applicability", "Applicability decision", "select", "Not applicable needs a specific reason in the notes."],
      ["status", "Verification status", "select", "Pass requires evidence for this build; acceptance is never a pass."],
      ["findingSeverity", "Finding severity (when failed or accepted)", "select", "Assess actual impact and exploitability independently of control priority. Unassessed, High, or Critical findings block release regardless of control priority."],
      ["evidence", "Evidence / reproduction / retest", "textarea", "Reference redacted test results, roles, expected vs. actual behavior, and build-specific evidence. Do not paste secrets or personal data."],
      ["notes", "Notes / finding / not-applicable rationale", "textarea", "Record severity rationale, impact, scope, remediation, retest result, blocked-test reason, or why this control does not apply."],
      ["riskOwner", "Risk owner", "text", "Named accountable owner for any accepted risk."],
      ["riskExpiry", "Risk review expiry", "date", "Required for accepted risk; expired acceptance remains unresolved."],
      ["riskRationale", "Risk acceptance rationale", "textarea", "Explain impact, compensating controls, residual exposure, and the owner's decision."]
    ];
    definitions.forEach(([key, label, kind, help]) => {
      const field = createField(key, label, kind, help, record[key], value => {
        records.get(control.id)[key] = value;
        syncCard(control.id);
        changed();
      }, control.id);
      if (kind === "select") {
        addOptions(field.input, key === "status" ? STATUS : key === "findingSeverity" ? SEVERITY : APPLICABILITY);
        field.input.value = record[key];
      }
      if (["findingSeverity", "evidence", "notes", "riskRationale"].includes(key)) field.wrapper.classList.add("full");
      (key.startsWith("risk") ? riskGrid : recordGrid).append(field.wrapper);
      fields.set(key, field);
    });
    const warning = node("p", "", "record-warning");
    warning.id = control.id + "-warning";
    body.append(methods, sources, recordGrid, riskGrid, warning);
    card.append(body);
    cards.set(control.id, {card, fields, statusBadge, appBadge, riskGrid, warning});
    return card;
  }
  function isoDate(value) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
    const date = new Date(value + "T00:00:00Z");
    return !Number.isNaN(date.getTime()) && date.toISOString().slice(0, 10) === value;
  }
  function recordIssues(control, record, metadata, today = new Date().toISOString().slice(0, 10)) {
    const problems = [];
    if (record.applicability === "Unreviewed") problems.push("Applicability is unresolved.");
    if (record.applicability === "Not applicable") {
      if (!record.notes.trim()) problems.push("Not applicable requires a specific rationale in notes.");
      if (record.status !== "Untested") problems.push("A not-applicable control must retain Untested status; explain the exclusion in notes.");
      return problems;
    }
    if (record.status === "Pass" && !record.evidence.trim()) problems.push("Pass requires build-specific evidence.");
    if (["Fail", "Accepted risk"].includes(record.status) && record.findingSeverity === "Unassessed") problems.push("Assign a finding severity from actual impact and exploitability; control priority is not finding severity.");
    if (["Fail", "Accepted risk"].includes(record.status) && (!record.evidence.trim() || !record.notes.trim())) problems.push("A finding requires reproducible evidence and notes covering impact, remediation, and retest or residual risk.");
    if (record.status === "Accepted risk") {
      if (!record.riskOwner.trim() || !record.riskRationale.trim()) problems.push("Risk acceptance requires an owner and rationale.");
      if (!isoDate(record.riskExpiry)) problems.push("Risk acceptance requires a valid expiry date.");
      else if (record.riskExpiry < today) problems.push("Risk acceptance has expired.");
    }
    return problems;
  }
  function evaluate(metadata, recordMap, today) {
    const result = {missingScope:[], unresolved:[], invalid:[], highGaps:[], findingBlockers:[], lowerGaps:[], accepted:[], passed:0, notApplicable:0, statusCounts:Object.fromEntries(STATUS.map(value => [value, 0]))};
    META.forEach(([key, label]) => { if (!metadata[key].trim()) result.missingScope.push(label); });
    if (metadata.date.trim() && !isoDate(metadata.date)) result.missingScope.push("Valid review date");
    for (const control of DATA.controls) {
      const record = recordMap.get(control.id);
      result.statusCounts[record.status]++;
      if (record.applicability === "Unreviewed") result.unresolved.push(control.id);
      const issues = recordIssues(control, record, metadata, today).filter(issue => issue !== "Applicability is unresolved.");
      if (issues.length) result.invalid.push({id:control.id, issues});
      if (record.applicability === "Not applicable") {
        if (!issues.length) result.notApplicable++;
        continue;
      }
      if (record.status === "Accepted risk") result.accepted.push(control.id);
      if (["Fail", "Accepted risk"].includes(record.status) && ["Unassessed", "High", "Critical"].includes(record.findingSeverity)) result.findingBlockers.push({id:control.id, severity:record.findingSeverity});
      if (record.applicability === "Applicable" && record.status === "Pass" && record.evidence.trim() && !issues.length) result.passed++;
      if (record.status !== "Pass" || issues.length) {
        if (["Critical", "High"].includes(control.priority)) result.highGaps.push({id:control.id, status:record.status, priority:control.priority});
        else result.lowerGaps.push({id:control.id, status:record.status});
      }
    }
    // Count unique controls with blockers; incomplete scope is one additional blocker.
    const blockedIds = new Set([...result.unresolved, ...result.invalid.map(value => value.id), ...result.highGaps.map(value => value.id), ...result.findingBlockers.map(value => value.id)]);
    result.blockerCount = blockedIds.size + (result.missingScope.length ? 1 : 0);
    result.blocked = result.blockerCount > 0;
    return result;
  }
  function syncCard(id) {
    const control = byId.get(id);
    const record = records.get(id);
    const ui = cards.get(id);
    const problems = recordIssues(control, record, audit);
    ui.statusBadge.textContent = record.status === "Pass" && problems.length ? "Pass · record incomplete" : record.status;
    const statusClass = record.status === "Pass" ? (record.applicability === "Applicable" && !problems.length ? "pass" : "invalid") : record.status === "Fail" ? "fail" : record.status === "Blocked" ? "blocked" : record.status === "Accepted risk" ? "risk" : "";
    ui.statusBadge.className = "badge " + statusClass;
    ui.appBadge.textContent = record.applicability;
    ui.riskGrid.hidden = record.status !== "Accepted risk" && !record.riskOwner && !record.riskRationale && !record.riskExpiry;
    ui.warning.textContent = problems.join(" ");
    for (const [key, field] of ui.fields) {
      if (field.input.value !== record[key]) field.input.value = record[key];
      field.printValue.textContent = record[key] || "[Not recorded]";
    }
    ui.fields.get("evidence").input.setAttribute("aria-invalid", String(record.status === "Pass" && !record.evidence.trim()));
    ui.fields.get("notes").input.setAttribute("aria-invalid", String(record.applicability === "Not applicable" && !record.notes.trim()));
  }
  function renderGate() {
    const result = evaluate(audit, records);
    put("count-blockers", result.blockerCount);
    put("count-unreviewed", result.unresolved.length);
    put("count-passed", result.passed);
    put("count-total", DATA.controls.length);
    const gate = document.getElementById("gate");
    gate.className = "gate " + (result.blocked ? "blocked" : "review");
    put("decision-title", result.blocked ? "Release recommendation blocked" : "No automatic blocker detected — human review required");
    put("gate-message", result.blocked ? "The record contains unresolved scope, applicability, evidence, or Critical/High controls. Complete or explicitly escalate these before a release decision." : "The recorded controls have cleared this workbook's automatic blockers. A qualified reviewer must still assess the evidence, residual risks, and any remaining lower-priority work.");
    const list = document.getElementById("gate-reasons");
    list.replaceChildren();
    const add = text => list.append(node("li", text));
    if (result.missingScope.length) add("Incomplete scope record: " + result.missingScope.join("; ") + ".");
    if (result.unresolved.length) add(result.unresolved.length + " controls still need an applicability decision.");
    if (result.highGaps.length) add(result.highGaps.length + " Critical/High controls have unresolved verification or risk. Accepted risk does not clear this blocker.");
    if (result.findingBlockers.length) add(result.findingBlockers.length + " findings have Unassessed, High, or Critical severity and block release regardless of control priority.");
    if (result.invalid.length) add(result.invalid.length + " records have missing evidence, inconsistent status, or incomplete/expired acceptance.");
    if (result.lowerGaps.length) add(result.lowerGaps.length + " Medium controls need review: failures, blocked or untested work, or accepted risks.");
    if (result.accepted.length) add(result.accepted.length + " applicable/unresolved controls record accepted risk; review the accountable owners and expiry dates.");
    add("Status totals: " + STATUS.map(status => status + " " + result.statusCounts[status]).join(" · ") + ". Valid not-applicable exclusions: " + result.notApplicable + ".");
  }
  function filterControls() {
    const search = document.getElementById("search").value.trim().toLocaleLowerCase();
    const domain = document.getElementById("domain-filter").value;
    const priority = document.getElementById("priority-filter").value;
    const status = document.getElementById("status-filter").value;
    const applicability = document.getElementById("app-filter").value;
    let count = 0;
    for (const control of DATA.controls) {
      const record = records.get(control.id);
      const haystack = [control.id, control.title, control.domain, control.applicability, control.verify, control.pass, control.evidence, ...Object.values(record)].join(" ").toLocaleLowerCase();
      const visible = (!search || haystack.includes(search)) && (!domain || control.domain === domain) && (!priority || control.priority === priority) && (!status || record.status === status) && (!applicability || record.applicability === applicability);
      cards.get(control.id).card.classList.toggle("filtered-out", !visible);
      if (visible) count++;
    }
    put("filter-result", count + " of " + DATA.controls.length + " controls shown. Filters do not change the release decision.");
    document.getElementById("empty").hidden = count !== 0;
  }
  function snapshot() {
    return {format:FORMAT, schemaVersion:SCHEMA, catalogVersion:DATA.version, exportedAt:new Date().toISOString(), audit:{...audit}, controls:DATA.controls.map(control => ({...records.get(control.id)}))};
  }
  function plainObject(value) { return value !== null && typeof value === "object" && !Array.isArray(value) && Object.getPrototypeOf(value) === Object.prototype; }
  function exactKeys(value, keys, label) {
    if (!plainObject(value)) throw new Error(label + " must be an object.");
    const actual = Object.keys(value);
    if (actual.length !== keys.length || actual.some(key => !keys.includes(key))) throw new Error(label + " has missing or unknown fields.");
  }
  function rejectDangerousKeys(value) {
    if (value === null || typeof value !== "object") return;
    for (const key of Object.keys(value)) {
      if (["__proto__", "constructor", "prototype"].includes(key)) throw new Error("Import contains a prohibited object key.");
      rejectDangerousKeys(value[key]);
    }
  }
  function validText(value, label) {
    if (typeof value !== "string" || value.length > MAX_TEXT || /\u0000/.test(value)) throw new Error(label + " must be text no longer than " + MAX_TEXT + " characters, without NUL characters.");
  }
  function validateImport(value) {
    rejectDangerousKeys(value);
    exactKeys(value, ["format", "schemaVersion", "catalogVersion", "exportedAt", "audit", "controls"], "Audit file");
    if (value.format !== FORMAT || value.schemaVersion !== SCHEMA) throw new Error("Unsupported audit file format or schema version.");
    if (value.catalogVersion !== DATA.version) throw new Error("This file belongs to a different catalog version. Use its matching workbook; do not silently migrate evidence.");
    if (typeof value.exportedAt !== "string" || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/.test(value.exportedAt) || !Number.isFinite(Date.parse(value.exportedAt)) || new Date(value.exportedAt).toISOString() !== value.exportedAt) throw new Error("Invalid export timestamp.");
    exactKeys(value.audit, META_KEYS, "Scope record");
    META_KEYS.forEach(key => validText(value.audit[key], "Scope field " + key));
    if (value.audit.date && !isoDate(value.audit.date)) throw new Error("Invalid review date.");
    if (!Array.isArray(value.controls) || value.controls.length !== DATA.controls.length) throw new Error("The file must contain every control from this catalog exactly once.");
    const seen = new Set();
    const validatedRecords = new Map();
    value.controls.forEach((record, index) => {
      exactKeys(record, RECORD_KEYS, "Control record " + (index + 1));
      RECORD_KEYS.forEach(key => validText(record[key], "Control field " + key));
      if (!byId.has(record.id) || seen.has(record.id)) throw new Error("Unknown or duplicate control ID.");
      if (!APPLICABILITY.includes(record.applicability) || !STATUS.includes(record.status)) throw new Error("Unknown applicability or status.");
      if (!SEVERITY.includes(record.findingSeverity)) throw new Error("Unknown finding severity.");
      if (record.riskExpiry && !isoDate(record.riskExpiry)) throw new Error("Invalid risk expiry date.");
      seen.add(record.id);
      validatedRecords.set(record.id, Object.fromEntries(RECORD_KEYS.map(key => [key, record[key]])));
    });
    return {audit:Object.fromEntries(META_KEYS.map(key => [key, value.audit[key]])), records:validatedRecords};
  }
  function parseImport(text, bytes = new TextEncoder().encode(text).length) {
    if (bytes > MAX_FILE_BYTES) throw new Error("Import exceeds the 2 MiB limit.");
    return validateImport(JSON.parse(text));
  }
  function applyValidated(value) {
    audit = value.audit;
    records = value.records;
    for (const [key, field] of metaInputs) {
      field.input.value = audit[key];
      field.printValue.textContent = audit[key] || "[Not recorded]";
    }
    DATA.controls.forEach(control => syncCard(control.id));
    changed();
  }
  function saveLocal() {
    if (!document.getElementById("local-save").checked) return;
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(snapshot())); }
    catch (error) {
      document.getElementById("local-save").checked = false;
      announce("Browser saving failed or storage is unavailable. Export JSON now to keep your current work. An older saved copy may still exist.", true);
    }
  }
  function changed() {
    dirty = true;
    renderGate();
    filterControls();
    saveLocal();
  }
  function exportAudit() {
    const json = JSON.stringify(snapshot(), null, 2);
    const blob = new Blob([json], {type:"application/json"});
    if (blob.size > MAX_FILE_BYTES) {
      announce("Audit exceeds the 2 MiB portable import limit. Shorten evidence to references and remove unnecessary copied text before exporting.", true);
      return;
    }
    const url = URL.createObjectURL(blob);
    const link = node("a");
    link.href = url;
    link.download = "website-security-audit-" + (audit.date || new Date().toISOString().slice(0,10)) + ".json";
    document.body.append(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    dirty = false;
    announce("Audit JSON download requested. Verify that your browser saved it before closing this tab. The HTML template does not contain your records.");
  }
  async function importFile(file) {
    if (!file) return;
    try {
      if (file.size > MAX_FILE_BYTES) throw new Error("Import exceeds the 2 MiB limit.");
      const validated = parseImport(await file.text(), file.size);
      if (!window.confirm("Replace all current audit fields and control records with this validated JSON file? Export the current record first if you need to keep it.")) {
        announce("Import cancelled. Current records were kept.");
        return;
      }
      announce("Audit imported. Statuses reflect the supplied record and still require independent evidence review.");
      applyValidated(validated);
    } catch (error) { announce("Import rejected; current records were kept. " + error.message, true); }
    finally { document.getElementById("import-file").value = ""; }
  }
  function initialize() {
    put("catalog-version", DATA.version);
    put("catalog-date", "Source check: " + DATA.checked);
    buildMeta();
    const container = document.getElementById("controls");
    const fragment = document.createDocumentFragment();
    DATA.controls.forEach(control => fragment.append(createControl(control)));
    container.append(fragment);
    DATA.controls.forEach(control => syncCard(control.id));
    const domains = [...new Set(DATA.controls.map(control => control.domain))].sort();
    addOptions(document.getElementById("domain-filter"), domains);
    const sources = document.getElementById("sources");
    DATA.sources.forEach(source => {
      const item = node("li");
      item.append(sourceLink(source), node("span", source.version + " · Checked " + source.checked, "source-meta"), node("span", source.url, "source-url"));
      sources.append(item);
    });
    ["search", "domain-filter", "priority-filter", "status-filter", "app-filter"].forEach(id => document.getElementById(id).addEventListener("input", filterControls));
    document.getElementById("clear-filters").addEventListener("click", () => {
      ["search", "domain-filter", "priority-filter", "status-filter", "app-filter"].forEach(id => { document.getElementById(id).value = ""; });
      filterControls();
    });
    document.getElementById("expand-button").addEventListener("click", () => cards.forEach(ui => { ui.card.open = true; }));
    document.getElementById("collapse-button").addEventListener("click", () => cards.forEach(ui => { ui.card.open = false; }));
    document.getElementById("export-button").addEventListener("click", exportAudit);
    document.getElementById("import-button").addEventListener("click", () => document.getElementById("import-file").click());
    document.getElementById("import-file").addEventListener("change", event => importFile(event.target.files[0]));
    document.getElementById("print-button").addEventListener("click", () => window.print());
    document.getElementById("local-save").addEventListener("change", event => {
      if (event.target.checked) {
        try {
          if (localStorage.getItem(STORAGE_KEY) && !window.confirm("Saving this audit will replace the existing browser copy for this catalog. Load or export that copy first if you need to keep it. Replace it now?")) {
            event.target.checked = false;
            announce("Browser saving remains off. The previous saved copy was kept.");
            return;
          }
        } catch (error) {
          event.target.checked = false;
          announce("Browser storage is unavailable. Export JSON to preserve this audit.", true);
          return;
        }
        saveLocal();
        if (event.target.checked) announce("Browser saving is enabled for this tab. Export JSON as your portable backup.");
      } else {
        try { localStorage.removeItem(STORAGE_KEY); announce("Browser saving disabled and saved copy removed. Current tab records remain."); }
        catch (error) { announce("Browser saving disabled, but removing the previous copy failed. Clear this file's browser storage manually if needed.", true); }
      }
    });
    document.getElementById("load-button").addEventListener("click", () => {
      try {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (!saved) { announce("No saved browser copy was found for this catalog. Import an exported JSON file instead."); return; }
        const validated = parseImport(saved);
        if (!window.confirm("Replace the current audit with the saved browser copy? Browser saving will remain at its current setting.")) return;
        announce("Saved browser copy loaded. Confirm its build and review date before relying on it.");
        applyValidated(validated);
      } catch (error) { announce("Browser copy could not be loaded; current records were kept. " + error.message, true); }
    });
    document.getElementById("reset-button").addEventListener("click", () => {
      if (!window.confirm("Clear all entered audit data and return every control to Untested / Unreviewed? Export JSON first to preserve your work. The saved browser copy will also be removed.")) return;
      document.getElementById("local-save").checked = false;
      let storageRemoved = true;
      try { localStorage.removeItem(STORAGE_KEY); } catch (error) { storageRemoved = false; }
      applyValidated({audit:Object.fromEntries(META_KEYS.map(key => [key, ""])), records:new Map(DATA.controls.map(control => [control.id, freshRecord(control.id)]))});
      dirty = false;
      announce(storageRemoved ? "Audit reset. Every control is Untested and applicability Unreviewed." : "Audit reset in this tab. The saved browser copy could not be removed; clear its browser storage manually if needed.", !storageRemoved);
    });
    window.addEventListener("beforeunload", event => {
      if (dirty && !document.getElementById("local-save").checked) { event.preventDefault(); event.returnValue = ""; }
    });
    window.addEventListener("beforeprint", () => {
      beforePrint = [...document.querySelectorAll("details")].map(detail => [detail, detail.open]);
      beforePrint.forEach(([detail]) => { detail.open = true; });
    });
    window.addEventListener("afterprint", () => {
      if (beforePrint) beforePrint.forEach(([detail, wasOpen]) => { detail.open = wasOpen; });
      beforePrint = null;
    });
    renderGate();
    filterControls();
  }
  // Deliberately small test interface. The catalog is a detached copy; there is no state mutation hook.
  window.AuditWorkbook = Object.freeze({parseImport, validateImport, evaluate, freshRecord, snapshot, catalog:JSON.parse(JSON.stringify(DATA)), schemaVersion:SCHEMA, maxFileBytes:MAX_FILE_BYTES});
  initialize();
})();'''


def validate_catalog(catalog: dict) -> None:
    """Reject incomplete or unsafe catalog structure before embedding it."""
    for key in ("version", "checked", "controls", "sources"):
        if key not in catalog:
            raise ValueError(f"Missing catalog key: {key}")
    if not catalog["controls"] or not catalog["sources"]:
        raise ValueError("Catalog must include controls and sources")
    source_ids = set()
    for source in catalog["sources"]:
        for field in ("id", "title", "url", "version", "checked"):
            if not isinstance(source.get(field), str) or not source[field].strip():
                raise ValueError(f"Missing source field {field}")
        if source["id"] in source_ids:
            raise ValueError(f"Duplicate source ID: {source['id']}")
        if not source["url"].startswith("https://"):
            raise ValueError(f"Source must use HTTPS: {source['id']}")
        source_ids.add(source["id"])
    control_ids = set()
    for control in catalog["controls"]:
        for field in ("id", "domain", "title", "priority", "applicability", "verify", "pass", "evidence"):
            if not isinstance(control.get(field), str) or not control[field].strip():
                raise ValueError(f"Missing control field {field}: {control.get('id')}")
        if control["id"] in control_ids:
            raise ValueError(f"Duplicate control ID: {control['id']}")
        if control["priority"] not in ("Critical", "High", "Medium"):
            raise ValueError(f"Unknown priority: {control['id']}")
        if not isinstance(control.get("sourceIds"), list) or not control["sourceIds"]:
            raise ValueError(f"No sources: {control['id']}")
        if any(source_id not in source_ids for source_id in control["sourceIds"]):
            raise ValueError(f"Unknown source reference: {control['id']}")
        control_ids.add(control["id"])


def build(catalog_path: Path, output_path: Path) -> None:
    catalog = json.loads(catalog_path.read_text(encoding="utf-8-sig"))
    validate_catalog(catalog)
    encoded = json.dumps(catalog, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    executable = "\n" + SCRIPT + "\n"
    digest = base64.b64encode(hashlib.sha256(executable.encode("utf-8")).digest()).decode("ascii")
    csp = "default-src 'none'; script-src 'sha256-" + digest + "'; style-src 'unsafe-inline'; img-src data:; object-src 'none'; base-uri 'none'; form-action 'none'; connect-src 'none'"
    html = PAGE.replace("__CATALOG__", encoded).replace("__SCRIPT__", SCRIPT).replace("__CSP__", csp)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8", newline="\n")
    print(f"Built {output_path}: {len(catalog['controls'])} controls, {len(catalog['sources'])} sources, {len(html.encode('utf-8')):,} bytes")


if __name__ == "__main__":
    base = Path(__file__).resolve().parent.parent
    catalog_file = Path(sys.argv[1]) if len(sys.argv) > 1 else base / "references/controls.json"
    output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else base / "assets/security-audit.html"
    build(catalog_file, output_file)
