# Maximum-effort audit protocol

Maximum effort means deeper, systematic verification inside an approved boundary. It does not remove safety limits, extend permission, guarantee every exploit has been attempted or make this skill an autonomous scanner. No tests run merely because the skill, ledger or HTML exists. Follow [audit-protocol.md](audit-protocol.md) and [active-testing.md](active-testing.md).

## Review the plan, then ask the exact question

Before active execution, prepare a reviewable scope and populate a working copy of [test-plan-ledger.json](../templates/test-plan-ledger.json). Show the owner the exact owned local/staging targets and paths, test identities, methods, exclusions, aggregate request/rate/concurrency/time and payload caps, integration sinks, relevant backup/restore arrangements, health-triggered stops and cleanup. Identify any unavailable or prohibited tests before presenting the gate.

Ask exactly: **Are you ready to get hacked?** Offer **Yes** and **No**, and immediately explain: **Yes approves only the displayed, explicitly authorized local/staging test plan and its limits. It does not authorize production testing, third-party attacks, real-account guessing, destructive actions or unlimited traffic.** Keep the scope and plan available for review; do not hide the consequences behind playful wording.

Record the answer and its time/reference. Pending or No prevents active/load execution; already-authorized offline review may continue only when `scope.offlineReviewAuthorized` is true and its authority is recorded. Yes alone is insufficient: execution also requires `scopeApproved: true`, a valid owner authorization reference and time window, explicit targets/accounts, positive approved caps, a safe method and an issued test lease. Reuse valid existing authorization without repeatedly asking for the same permission. A scope, target or budget expansion needs a new concrete review and authorization; an old Yes cannot cover it. Missing prerequisites remain Blocked, Skipped with a reason, or Not run. Never translate consent to filling in Passed statuses.

## Inventory before execution

Generate a private working ledger with `python scripts/new_ledger.py private-audits/test-plan.json`. It expands every catalog control into a Planned, Unreviewed record with zero budgets and no target. It will not overwrite an existing ledger and makes no network requests. Resolve applicability and split these baseline records into the actual positive/negative cases before approval. Validate records with `python scripts/validate_ledger.py private-audits/test-plan.json`; validation checks consistency, not ownership, consent or live enforcement.

Use the catalog and actual stack to populate tests **before** launching them. Start every planned case unexecuted. Cover the relevant attack surface and record an applicability rationale for absent features: threat model and trust boundaries; identity, sessions, recovery, MFA and invitations; object/action/field/tenant authorization; injection, XSS, CSRF and SSRF; files, paths and parsers; REST, GraphQL and WebSockets; secrets, crypto/TLS and browser policy; payment/webhook/CRM integrity; booking/auction races; abuse and resource bounds; dependencies and CI/CD; cloud IAM/storage/network/origins; privacy/logging; restore/incident operations; third-party and AI trust boundaries where present.

This is a coverage inventory, not a promise to try every historical exploit. Use exact framework/runtime/module versions and fresh official advisories to add relevant cases. Split a category into distinct tests when targets, identities, methods, evidence or outcomes differ. Record controls reviewed without execution separately from executed cases; do not give a whole category a pass because one variant succeeded. If a new case is discovered during testing, the coordinator adds it first and verifies that existing scope and remaining budget cover it before issuing a lease.

For password-guessing protections, use only a few pre-agreed attempts against disposable synthetic accounts, preferably with reduced local lockout/rate thresholds. Do not use real credentials, leaked password sets, credential stuffing or real-user accounts. For injection or file tests use tiny harmless fixtures and minimal proofs; do not extract real data, obtain persistence, evade controls or escalate a proven flaw into a broader compromise.

Do not interpret "DDoS" as permission for flooding. A load/resilience case is a separate `load_test` activity requiring its own explicit approval, isolated owned local/staging target, bounded single-origin traffic, synthetic data, verified relevant recovery arrangements and health-triggered stops. It remains within the same global caps. Prefer threshold reduction, stubs and deterministic boundary tests. No distributed flood, production load test or disruption of third-party/shared services is permitted. If isolation or bounds cannot be enforced, mark it Blocked and use an offline design review or local simulation.

## One coordinator owns the ledger and aggregate budget

The coordinating agent is the **single writer** of the canonical ledger. Workers send append-only result messages or separate per-test result files to the coordinator; they never concurrently edit the canonical JSON. Assign each test a unique ID and exactly one assigned agent. The coordinator serializes updates, increments `coordination.revision`, records timestamps and writes atomically where supported. Reject stale revisions and duplicate IDs; preserve prior outcomes and evidence instead of overwriting an inconvenient failure.

Before any active/load case, issue a unique, expiring lease with its test ID, assigned agent and reserved budget. Store it in `coordination.activeLeases` and copy its `leaseId` into the test. The sum of outstanding request reservations plus requests already used must not exceed the global request cap. The sum of concurrent lease slots and allocated request rates must not exceed global concurrency/rate caps. The campaign deadline is fixed from its start; giving another agent a lease must not restart the clock. A worker must stop when its lease or the campaign expires and must never self-renew.

Count setup requests, redirect hops, retries, health polling, scanner subrequests, cleanup traffic and retests against the same aggregate caps. Reserve sufficient capacity for required observation and cleanup. Use a single request dispatcher or another auditable shared limiter for global pacing and concurrency. A spreadsheet or JSON ledger records limits but cannot enforce them by itself. If a tool hides requests or cannot enforce the approved scope/limits, do not run it. Independent agent budgets are not permission to multiply traffic.

Workers submit actual counts, timestamps, observations and evidence; the coordinator reconciles them, closes the lease and releases only unused reservations. For a timeout or uncertain mutation, inspect synthetic state before any retry and retain the uncertainty until resolved. On a stop condition, set `stopRequested`, revoke outstanding leases, prevent further dispatch and cancel in-flight work where supported. Stop conditions include unexpected real data, out-of-scope destinations, financial/notification effects, instability, agreed error/latency thresholds, authorization uncertainty and exhaustion of any cap. Only the approved recovery/cleanup procedure may continue, within its reserved budget; otherwise hand it to the owner.

## Ledger schema and record contract

The top-level `exampleOnly` flag must be true for teaching/dry-run ledgers; such files cannot authorize real execution. `scope.loadTestApproval` separately records an approval reference, owner, time and numeric health stop conditions for any load case. Keep verified closed/revoked lease records in `coordination.leaseHistory`, with the original lease fields plus `state` (`Closed` or `Revoked`), `closedAt` and `requestsUsed`; never erase an earlier reservation or finding. An uncertain worker remains in activeLeases with its reservation held until verified stopped; uncertainty is not a completed historical lease.

Each active lease also records `remainingRequests`. It starts at the reserved request count and decreases as the coordinator records spent requests; the campaign total is `coordination.usedRequests` plus remaining outstanding reservations. Request rates and concurrency reservations remain bounded across all simultaneous leases. An uncertain or unreachable worker retains its reservation until cancellation/expiry and in-flight outcome are verified; never assume a lost worker stopped. Revoking a lease alone does not prove it has stopped sending traffic.

The blank template uses `version: 1`, `gate.decision: "Pending"`, `scopeApproved: false`, zero caps and an empty `tests` array. It is deliberately non-executable and must be populated before a campaign. Each test records its own `releaseArtifact`, including the fixed artifact for distinct retest cases; do not overwrite the original build evidence. Timestamps are UTC ISO 8601 strings when observed; use null for events that have not happened. Do not backfill invented timestamps or evidence.

Gate decisions: `Pending | Yes | No`. Activities: `offline_review | active_test | load_test`. Test statuses: `Planned | Ready | Running | Passed | Failed | Blocked | Skipped | Not run | Retest pending | Retest passed | Retest failed`. Applicability: `Unreviewed | Applicable | Not applicable`. Finding severity: `Unassessed | Low | Medium | High | Critical`. A Ready active/load test is still unexecuted; it requires the approved gate/scope and a valid lease. Passed/Failed and Retest passed/Retest failed require genuine execution/review evidence appropriate to the activity. Never-run Blocked/Skipped/Not run records can have null execution timestamps; they require a reason and remain visible. A passed offline review does not substitute for an unexecuted runtime test.

Define each `scope.targets` item as `{id, origin, environment, ownedBy, authorizationReference, allowedPathPrefixes}`; paths are explicit strings and environment identifies local/staging. Define each `scope.testAccounts` item as `{id, role, tenant, synthetic}`; include no password, token or secret. Define each active lease as `{leaseId, testId, assignedAgent, issuedAt, expiresAt, budget}`. `budget` has numeric `requests`, `requestsPerSecond`, `concurrency` and `seconds`. All numbers are nonnegative; request counts and concurrency are integers. Zero prohibits that active resource, rather than meaning unlimited.

Example **unexecuted record structure** (replace the synthetic identifiers during planning; it grants no permission):

```json
{
  "id": "TEST-0001",
  "category": "Object and tenant authorization",
  "controlIds": ["AZ-02", "AZ-03"],
  "activity": "active_test",
  "applicability": "Unreviewed",
  "targetId": "owned-staging-app",
  "target": "https://staging.example.invalid/api/orders/{synthetic-id}",
  "releaseArtifact": "",
  "owner": "",
  "assignedAgent": "",
  "safeMethod": "Use two synthetic users and one known disposable order; compare allowed and denied access plus persisted state.",
  "expected": "The non-owner receives no protected data and causes no mutation or downstream action.",
  "status": "Planned",
  "reason": "Scope, identities and budget have not been approved.",
  "approvalReference": "",
  "leaseId": null,
  "budget": {"requests": 0, "requestsPerSecond": 0, "concurrency": 0, "seconds": 0},
  "timestamps": {"plannedAt": null, "startedAt": null, "finishedAt": null, "updatedAt": null},
  "requestsUsed": 0,
  "observed": "",
  "evidence": [],
  "severity": "Unassessed",
  "remediation": {"recommendation": "", "basis": "Uninspected", "codeReferences": [], "owner": "", "fixArtifact": ""},
  "retest": {"status": "Not run", "testIds": [], "releaseArtifact": "", "evidence": [], "remainingRisk": ""}
}
```

Evidence entries are private redacted references with method, expected/observed result and release/environment context, not copied credentials or customer records. `remediation.basis` is `Uninspected | Inspected code | Conditional guidance`. Inspected source/configuration and version evidence can support an exact proposed file/line/patch fix even if runtime testing is blocked. Distinguish a static code finding from demonstrated runtime exploitability, and do not claim the fix works until retested. Without the relevant inspected source, state the missing evidence and give conditional guidance. `retest.status` uses the same test status vocabulary and links distinct retest IDs so prior results remain intact. A Failed case may become Retest pending, but its original evidence and finding remain visible until a proven fix/retest resolves them.

## Report and handoff

Map ledger outcomes conservatively to the HTML: Planned, Ready, Running and Not run remain Untested; Blocked remains Blocked. Skipped becomes Not applicable only with architecture-backed exclusion rationale, otherwise it remains Untested/Blocked. Failed and Retest failed map to Fail; Retest pending preserves the original failure. Passed/Retest passed supplies candidate evidence only: all applicable variants and the control's full criteria must be satisfied before a control passes. Risk acceptance never erases a failed case.

Use [final-report.md](../templates/final-report.md). Report what ran, what did not, global budget consumption, stop events, coverage gaps, reproducible findings, impact-based severity, supported fixes and exact retest results. Keep actual targets, credentials and findings in an appropriate private audit location. Hand off unresolved items with an accountable owner and the minimum next action/permission needed. Do not claim testing completed because the agents exhausted a budget, all tools exited successfully or the owner said Yes.

Apply the existing release gates. Unresolved Critical/High findings, including accepted risks at those severities, and applicable untested/blocked Critical/High checks block an ordinary readiness recommendation. State residual risk and scope limitations even after successful retests. Maximum effort ends at the agreed scope and caps; extending either requires a new reviewed plan.
