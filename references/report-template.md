# Security audit record template

Keep completed copies private. This blank template contains no findings.

## Scope and authority

- Project; release commit/artifact digest; environment; date; tester; accountable owner.
- Authorization reference, permitted actions/targets/time window, excluded targets/actions.
- Synthetic accounts/roles/tenants, approved request/concurrency budget, stop thresholds.
- Rollback/cleanup owner and method; evidence location/retention/redaction policy.
- Stack and exact versions; ASVS version/target level; refreshed advisory date and sources.

## Architecture and test plan

Data-flow/trust-boundary diagram, assets/data classifications, entrypoints, role/action/object/tenant matrix, third-party dependencies, abuse cases, business invariants and control applicability decisions. List missing artifacts and blocked tests separately from failures.

## Per-control record

Control ID; applicability with rationale; status; tester/date/build; method; expected and actual result; redacted evidence reference; limitations; linked finding; retest result. Not applicable needs an architecture-backed rationale. Pass needs observed evidence.

## Finding

- ID/title and related controls; affected route/component/build.
- Severity and impact/exploitability/exposure rationale (CVSS vector if appropriate).
- Preconditions and safe reproducible bounded steps; expected versus observed result.
- Redacted evidence and confirmed scope of impact; no real secret values or customer records.
- Root cause, recommended fix, responsible owner and due date.
- Fix commit/artifact and retest date/method/result; side-effect/regression verification.
- If accepted: named accountable owner, rationale, compensating controls, decision date, expiry and planned remediation/retest. Critical/High accepted risks still block an ordinary clean recommendation.

## Decision and limitations

State: **Blocked**, **Human review required**, or **No release-blocking findings identified within the tested scope, subject to owner review**. Include unresolved findings by severity, applicability/coverage gaps, blocked checks with exact permission/environment reason, advisory freshness, tool limitations and residual risk. No automatic pass rate or claim of perfect security.

## Retest ledger

Original finding → fix → exact release artifact → repeated failing case → adjacent positive/negative paths → data/side-effect checks → outcome → reviewer. Invalidate prior results when relevant implementation, configuration, dependency or exposure changes.
