# Artifact validation record

Package version: **1.1.0**. Research and validation: **2026-10-29**. This record validates the reusable package and offline workbook, **not any website or live deployment**. Every shipped control remains Untested with Unreviewed applicability.

## Completed checks

- 130 controls and 105 primary-source records. Every control has applicability, a concrete bounded verification method, pass criteria, evidence requirements, priority and resolvable source IDs.
- Official skill-creator `quick_validate.py`: **passed** for the final SKILL.md frontmatter, naming and scaffold checks. This structural validator does not prove audit quality.
- Independent paper/code review exercised four synthetic scenarios: payment/CRM state handling, upload/invitation handling, unauthorized production testing requests, and interpreting CORS/bind-address observations. It distinguished code evidence from unverified runtime assumptions, kept blocked tests visible and issued no false clean recommendation. No fixture was executed against a service.
- Independent review identified and resolved four material issues: finding severity separate from control priority, consistent High/Critical release gating, weak-hash migration criteria, and explicit HTTPS/HSTS plus authority/proxy trust checks. Seven targeted severity-gate assertions passed after correction.
- The shipped dependency-free Node test suite passed **40 assertions** against the built HTML: initial untested records, scope/evidence gates, accepted-risk expiry, lower-priority controls with severe findings, N/A consistency, JSON round trip, CSP script hash, unknown/duplicate/missing IDs, malformed types/status/versions/dates, text and file-size bounds, prototype keys and inert markup strings.

## Active workflow and maximum-effort edition

The active playbook, exact Yes/No prompt, explicit scope approval, single-writer ledger, shared budget leases, separate load approval, status mapping and final handoff templates were independently reviewed. The ledger generator creates **130 Planned/Unreviewed records**, a Pending gate, unapproved scope and zero budgets. It refuses to overwrite an existing path. It does not send requests or launch tests.

**36 pure ledger assertions passed.** They cover draft defaults, Yes without scope, No/Pending, combined rate/concurrency/request caps, campaign/lease windows, synthetic accounts, target boundaries, separate load approval, stop requests, duplicate assignments, evidence requirements, exact-fix source references and retest claims. Five independent adversarial records exposed defects that were corrected: lease overspending, unsupported embedded retest passes, noncanonical target paths, premature execution and retrospective load approval. All five invalid records are now rejected and the valid historical baseline is accepted.

The example-only ledger/report flow records one static finding in a fictional text snippet plus Blocked, Skipped and Not run cases, with **zero Passed records**. It demonstrates an exact inspected-source recommendation versus conditional guidance for unavailable code. No server, real account, payment or live website was tested. The ledger validator checks record consistency only; it cannot verify actual ownership, consent, honest evidence or traffic enforcement. A shared limiter and authorized tools are still required for any future active audit.

## Browser validation

An isolated headless Chromium 156.0.8078.74 session opened only the local HTML with all HTTP(S) traffic blocked. **51 interaction assertions passed**, with **zero JavaScript errors and zero document network attempts**. Checks included initial blank state, actual filter/status/evidence interactions, labels and keyboard focus, hostile HTML/SVG/script strings imported as inert text, atomic rejection of malformed imports, downloaded JSON round trips, applicability and severity gates, expiry, opt-in storage, and quota/denied-storage error handling.

Testing found a storage-warning overwrite after import/load; the final code preserves the warning and both regression tests pass. Desktop (1440 x 1000) and mobile (390 x 844) screenshots showed readable controls and no horizontal overflow. This is practical accessibility inspection, not formal WCAG certification or assistive-technology testing.

The final synthetic print test produced **104 A4 pages**. PDF text extraction confirmed all **130 control IDs**, **105 source titles**, and all **28 long-evidence test lines**, even with a screen filter active. There were no empty pages. Sampled pages 1, 3, 4, 65, 97 and 104 were visually inspected; control headings stayed together and no clipping was seen. The PDF and screenshots contain synthetic test records and are development evidence, not a completed website audit or shipped audit result.

Final standalone HTML SHA-256: `e807e3963ad22cfbf1f3a837a19dc842e82d3b14a226774a12c48621808c391c`.

Package consistency checks passed: catalog schema/source references, bundled relative links, deterministic HTML rebuild, offline dependencies, CSP executable-script integrity and absence of unsafe HTML-rendering sinks. ZIP packaging verifies each entry byte-for-byte against the reviewed package and excludes development dependencies, fixtures and caches.

## Reproduce artifact checks

From the package root, with Python 3 and Node.js installed:

```text
python scripts/build_html.py
python scripts/validate_package.py
node scripts/test_workbook.cjs
python scripts/test_ledger.py
python scripts/validate_ledger.py examples/ledger-dry-run.json
```

The commands operate on local files and do not test a website. No runtime dependencies are needed for these shipped checks. The official skill-creator validator is an external development check and additionally needs its own PyYAML dependency.

## Limits

Source links and version statements were checked during authoring; future availability or contents can change. Full source conformance, exhaustive exploit coverage, formal accessibility certification, every browser/OS, future CVEs and any actual deployed system are outside this artifact validation. The source register identifies living documentation and requires audit-time official advisory checks. Odoo rendered documentation was unavailable during research; its official versioned source was used.

The workbook requires human judgment: text evidence can be incomplete or false, the user chooses applicability, and no software here verifies a real security claim. A record clearing automatic blockers still requires qualified review. Completed records and sensitive evidence must be kept out of the public package.
