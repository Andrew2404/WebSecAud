# Authorized security audit handoff

This is a blank template. Do not treat an empty section, a planned test or an owner approval as a successful test. Keep completed copies and evidence private.

## Decision

Decision: **Not assessed**. Replace only after evidence review with **Blocked**, **Human review required**, or **No release-blocking findings identified within the tested scope, subject to owner review**.

Project / release artifact / environment:

Audit dates / tester / accountable release owner:

Authorization reference and approved time window:

Gate prompt: **Are you ready to get hacked?**

Gate decision: **Pending**. Decision-maker, time and reviewed-plan reference:

Scope approval: **Not recorded**. A Yes answer alone does not authorize testing beyond the approved local/staging plan.

Decision rationale, remaining blockers and residual risk:

## Scope and limits

Exact owned targets, approved paths, roles/tenants and synthetic accounts (identifiers only):

Build/configuration/dependency versions; catalog version and fresh official advisory checks:

Excluded targets/methods; third-party boundaries and integration sinks:

Relevant backup/restore verification, cleanup plan and emergency contact:

Global caps: requests / requests per second / concurrency / elapsed time / request-response bytes / external cost:

Actual aggregate consumption, peak concurrency/rate, start/deadline/end, and accounting limitations:

Stop events, uncertain outcomes, owner notifications and remaining cleanup:

## Coverage and execution record

Canonical ledger reference, final revision and single coordinator:

| Test ID / control | Category and activity | Target / assigned owner | Safe method | Status | Actual timestamps | Evidence / limitations |
|---|---|---|---|---|---|---|

Summarize separately: executed active tests, load/resilience tests separately approved and run, offline review, not-applicable decisions with rationale, and Blocked/Skipped/Not run cases. Include exact tool/version/configuration, fixture boundaries and whether caps were enforceable. Do not equate a passed offline review with an executed runtime check or convert omitted tests into passes.

## Findings and supported fixes

Repeat for each finding; keep original failed evidence after remediation.

- Finding ID / test IDs / affected controls:
- Affected build/component/route and synthetic preconditions:
- Severity and rationale from impact, exposure and exploitability; distinguish it from control priority:
- Expected versus observed behavior, including persisted state and downstream effects:
- Minimal non-destructive reproduction, bounded request count and redacted evidence references:
- Root cause and evidence supporting it:
- Fix recommendation and basis: **Uninspected / Inspected code / Conditional guidance**:
- For an exact fix, inspected file/line/symbol, proposed change and relevant invariant. If code/configuration was not inspected, label the recommendation conditional and name the missing evidence:
- Remediation owner, due date and deployment/review prerequisites:
- Fix commit/artifact and tests added or updated, only if actually implemented:
- Retest test IDs, exact release artifact, method, timestamps, positive/negative cases, state/side-effect checks and evidence:
- Retest result: **Not run** until executed; remaining risk and gaps:
- If risk accepted: accountable owner, rationale, compensating controls, decision date, expiry and remediation/retest plan. Acceptance is not a pass; Critical/High accepted findings still block an ordinary clean recommendation:

## Blocked and incomplete work

| Test ID / action | Exact target | Reason and missing prerequisite | State: Blocked / Skipped / Not run / Uncertain | Independent work completed | Required next action / owner |
|---|---|---|---|---|---|

State whether any attempted action was denied, timed out, or had an uncertain side effect. Check synthetic state before retrying an uncertain mutation. Do not bypass a denied action or imply that unavailable tools ran.

## Handoff

Unresolved findings and checks that block the readiness recommendation:

Lower-risk exceptions requiring human review:

Remaining cleanup and restoration tasks:

Private locations of the final ledger, redacted evidence, inspected-code references and retest artifacts:

Named owners, deadlines and the minimum next scope/permission/environment needed:

Scope limitations, untested variants, tool limitations and residual risk:

Release owner/reviewer acknowledgement and next review trigger:

This report describes evidence within an approved scope. It does not establish that every exploit was attempted or that the system is hacker-proof.
