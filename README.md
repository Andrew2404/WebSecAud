# Website security audit

A portable audit skill and self-contained offline checklist for evidence-based website release reviews. It supports Next.js/Node.js, Python and .NET applications, AWS deployments, payments, booking/auction workflows and CRM/Odoo integrations through conditional controls.

**Does it actually try to break the system?** An agent using this skill must execute feasible, authorized tests that attempt to violate security boundaries and business rules, then report evidence, remediation and retest results. The [active-testing playbook](references/active-testing.md) makes that work concrete. It defaults to owned local/staging systems, synthetic data, test accounts, bounded requests and non-destructive proofs. Missing authorization, tools or test environments stay visible as blockers.

The skill itself is instructions, not a standalone autonomous scanner. It does not run just because this repository exists. Invoke it through a capable agent with the repository and approved test environment available. Opening the HTML only opens the evidence workbook. The package cannot guarantee security or enumerate every exploit.

In [maximum-effort mode](references/maximum-effort.md), the agent asks **“Are you ready to get hacked?”** with Yes/No, records a bounded plan before execution, and updates the [test ledger](templates/test-plan-ledger.json) as assigned tests run. Yes is followed by explicit target/ownership/account/budget/stop-condition review; it never grants unlimited permission. Agents share a single coordinator and aggregate traffic budget. Synthetic-account guessing and separately approved isolated load/resilience checks replace unsafe brute-force or DDoS requests. The result is an evidence-backed [findings, fixes and retest handoff](templates/final-report.md), including every skipped or blocked case.

Create a private plan with `python scripts/new_ledger.py private-audits/test-plan.json`; it prepopulates all 130 controls as Planned/Unreviewed with zero budgets. `python scripts/validate_ledger.py private-audits/test-plan.json` checks record consistency only and never dispatches requests. See the [example-only ledger/report flow](examples/handoff-dry-run.md). The ledger is separate from the HTML's simpler per-control JSON format; neither is a traffic enforcer or proof of consent.

Package/catalog edition: **1.1.0**. The active-testing edition preserves the 130-control coverage and adds an explicit execution playbook. Import records using the matching catalog version; do not silently transfer old evidence to a different release.

Download [`assets/security-audit.html`](assets/security-audit.html) using GitHub’s raw-file download, then open the saved file in a modern browser. Search/filter the catalog, document applicability and evidence, and export a private JSON audit record. Every control starts untested. No scans or tests run merely by opening the document. No network dependencies are required; source links open only when selected. Print output includes the complete catalog and entered record regardless of screen filters.

Use [`SKILL.md`](SKILL.md) as the agent entrypoint and [`references/integration.md`](references/integration.md) for repository adoption. GitHub storage alone does not make other agents invoke a skill. The package does not change global settings or authorize live testing.

The catalog is a broad, original synthesis of primary sources, not a complete exploit list, ASVS certification or security guarantee. See the dated [source register](references/sources.md), [safe audit protocol](references/audit-protocol.md), [stack guide](references/stack-guide.md) and [validation record](VALIDATION.md). Refresh official advisories for the actual release versions at every audit.

Keep completed audits, screenshots with sensitive information and actual findings private. The public repository contains generic blank guidance only. The HTML does not upload data; local persistence is opt-in, browser-dependent and unencrypted. Export JSON before closing and store it securely. Downloading the original HTML does not embed your entered record.

## Maintenance

The canonical catalog is `references/controls.json`. Regenerate the HTML using `python scripts/build_html.py`, then run `python scripts/validate_package.py` and `node scripts/test_workbook.cjs`. CI runs these package checks; it does not attack a website or certify a deployment. Bump the catalog version whenever controls change; old audit records must remain tied to their reviewed catalog and release artifact.

## Attribution

Control text is independently written guidance with per-control links to primary OWASP, standards-body and platform documentation. Referenced publications retain their own copyrights and licenses. No vendor endorsement is implied; consult the original documents for the full requirements and current details.
