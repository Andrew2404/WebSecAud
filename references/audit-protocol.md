# Audit protocol and release decision

This protocol governs use of the catalog. It is reusable guidance, not authorization to test a particular system.

## 1. Scope before traffic

Record the accountable owner and authorization reference, exact repository/build/deployment digest, environment, domains/IPs and services in scope, tenant/role test accounts, prohibited actions, dates, data classification, notification plan and evidence retention. Agree a numeric request-rate and concurrency budget appropriate to staging, an abort threshold and a rollback owner. No universal rate is safe; start with isolated single requests and only expand within the approved budget.

Separate permissions for code review, local execution, staging traffic, provider consoles, production observations and production active tests. Being able to reach a URL or possessing credentials does not grant permission. Read-only cloud inspection can still expose secrets; query only necessary configuration and redact output. External vendors, customer accounts and shared infrastructure need their own authority. Reuse current valid permission instead of repeatedly asking.

If production/destructive/availability-impacting testing is not explicitly authorized, leave it blocked and continue static review, unit/integration tests, local fixtures or a staging simulation. Never substitute real charges, production concurrency or customer notifications for unavailable sandbox facilities. Record the exact blocked action, target, reason and what independent work completed. An ambiguous/timeout outcome must be checked before a retry; a denial must not be bypassed.

Stop immediately for instability, error-budget breach, unexpected private data, unintended notification/financial effect, a boundary outside scope or uncertainty about authorization. Preserve minimal redacted evidence, stop traffic, notify the designated owner using only authorized channels and execute only the approved rollback. Do not continue exploitation to prove maximum impact.

## 2. Threat model and coverage

Map browser/mobile clients, CDN/WAF/load balancers, origin, API, workers/queues, database/cache/storage, identity provider, payment provider, email/SMS, CRM/Odoo, analytics and AI services. Label each trust boundary and data flow with authentication, authorization, integrity, encryption, retention and failure handling. Include administrative/support interfaces and scheduled jobs.

List assets and attacker goals: account takeover, cross-tenant data access, privilege escalation, payment manipulation, inventory theft, malicious content execution, secret exposure, fraud, availability/cost abuse and poisoned automation. Identify least-trusted inputs, privileged confused-deputy actions and irreversible side effects. Express business invariants before choosing tests.

Inventory exact runtime/framework/provider/API versions, plugins, lockfiles, transitive dependencies, deployment images and service exposure. Choose the ASVS level and any sector/contractual requirements; enumerate extra controls when the baseline does not cover the actual architecture. This package synthesizes primary guidance; it does not assert one-to-one or complete ASVS/WSTG coverage.

## 3. Test design and evidence

Use [active-testing.md](active-testing.md) to convert this protocol and the control catalog into executed, bounded cases. Where testing is authorized and feasible, perform it rather than returning only a proposed checklist. The goal is to establish or reject a concrete security hypothesis using a harmless proof; once impact is established, stop that case and move to remediation/retest within scope. Keep missing runtime evidence separate from static-review conclusions.

Use synthetic data, at least two tenants and role-distinct test users where applicable, stub notifications and external services, test-mode payment credentials and disposable upload storage. Never paste secrets or real personal data into audit exports, screenshots, public issues or model prompts. Evidence should reference private records by safe identifier and include relevant redacted snippets or hashes.

For each applicable control capture: tester/date, exact build/environment, permission reference, preconditions, bounded action, expected outcome, actual observation, evidence location and cleanup. A test that only returns HTTP 403 is insufficient if a background action still occurred; inspect persisted state and side effects. Verify both allowed and denied actions and inspect backend state when the UI could be misleading.

Use static review, SAST, dependency/secret/IaC scans and authorized dynamic tests as complementary signals. Record tool/version/rules, exclusions and coverage. Review false positives and false negatives. Do not disable gates to obtain green output; suppressions need a narrow explanation and expiry. Recheck upstream advisories at the audit date rather than trusting this package's research date.

## 4. Status and priority semantics

| Field | Meaning |
|---|---|
| Applicability: Unreviewed | No architecture-backed decision yet; prevents completion. |
| Applicable | Control applies to the stated release scope. |
| Not applicable | The feature/exposure is absent, supported by a recorded rationale and evidence. This is not a pass. |
| Untested | No adequate verification completed. |
| Pass | Concrete, current evidence meets the control's criteria. |
| Fail | Reproduced noncompliance; create a finding. |
| Blocked | Cannot verify because of permission, environment, tooling or access limits. |
| Accepted risk | A named owner documented an exception. It remains a risk, never a pass. |

Critical/High/Medium in the catalog are **triage priorities**, not preassigned CVSS scores. Judge each actual finding's severity from impact, reachability, attacker prerequisites, likelihood, sensitive data/financial effects and compensating controls. Use a documented CVSS vector when useful; business-logic financial loss can require contextual prioritization beyond a scanner score.

## 5. Release recommendation

Block the ordinary readiness recommendation for unresolved Critical/High findings, accepted Critical/High risks, any applicable Critical/High control that is untested or blocked, unresolved applicability, invalid evidence, incomplete scope or missing audit-time advisory checks. This package intentionally gates untested High checks as well as Critical checks.

Lower-risk open findings, gaps or exceptions need explicit human review. Record the accountable owner's name/role, rationale, compensating control, decision date, expiry, remediation deadline and retest plan. An owner can make a business release exception; the audit must still state the exception and blockers without issuing a clean security recommendation. Do not invent an approval or security percentage.

For a completed review, state the exact build/scope, meaningful coverage, remaining limitations and residual risk. A statement such as "No release-blocking findings identified within the tested scope; owner review required" is narrower than a guarantee and is supported only after evidence review. Refresh evidence after relevant changes and retest fixes at the release artifact, including regression of the original failing path and nearby permissions/side effects.
