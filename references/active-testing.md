# Authorized active-testing workflow

Use this workflow during a requested audit when execution is within the recorded authorization. The agent should attempt the applicable checks with available tools, observe what happens, and report evidence. Do not stop at a plan or fill a checklist from assumptions when a safe, authorized test is feasible. This skill is agent guidance: it needs an agent, tools, a reachable approved environment and test fixtures. Neither installing the skill nor opening the HTML launches an autonomous scanner or grants authority over a website.

Read [audit-protocol.md](audit-protocol.md) first. Use [controls.json](controls.json) for the exact applicability, method, pass criteria and primary sources. Source/configuration review and dynamic verification complement each other; neither proves every possible exploit is absent.

## 1. Turn the scope into an executable plan

Bind the plan to the exact build, owner-approved local/staging targets, roles/tenants, permitted operations, time window, synthetic data and allowed integration sinks. Explicitly list destinations that must never receive test traffic. Confirm that redirects, callbacks, queues, email/SMS, payments and CRM jobs remain inside the approved boundary; a staging frontend can still call production services.

For each planned case, record:

- Control ID and suspected failure or invariant to challenge.
- Target route/component and test identities; positive and negative cases.
- Prerequisites, expected outcome, observable state and side effects.
- Request count, maximum rate/concurrency, body/response bounds and timeout.
- Stop condition, cleanup method and evidence location.

Start with single requests. A candidate budget for owner review might be one in-flight request, at most one request per second, at most 40 requests per case and a two-minute deadline. These are examples, not universal safe limits or implied permission. Use smaller limits for expensive or externally metered actions. An isolated two-request transaction race needs an explicitly included concurrency allowance; it is not authorization for a stress test. Stop at the budget instead of silently extending it.

Reuse valid authorization already supplied. If the requested case exceeds it, mark that case Blocked and continue independent permitted checks. Missing tools, test accounts, sandboxes or observability are visible gaps. Do not turn a review-only request into network testing, substitute production for missing staging, or retry a denied action through another route.

## 2. Prepare a contained test environment

Prefer the project's existing unit/integration test harness and a disposable database/storage namespace. Use role-distinct synthetic users in at least two tenants where relevant. Configure local mail/CRM/webhook sinks and payment test mode; verify their effective configuration before actions with side effects. Reset only the disposable fixtures covered by the cleanup plan.

Choose tools for the case: a local framework test client for server guards and state assertions, a browser test runner for rendered content/cookies, a bounded HTTP client for an approved endpoint, and read-only configuration or dependency tools for deployment and advisory evidence. Inspect scanner defaults before use. Disable out-of-scope crawling, external callbacks, broad fuzzing, exploit modules and unbounded concurrency. Do not install tools globally or expand access to make a test run; use available permitted capabilities or record the dependency.

Any disposable harness must stay in an isolated audit directory unless repository changes are separately authorized. Never embed actual secrets in scripts or artifacts. If a tool cannot enforce the approved destination, rate, payload or side-effect limits, use a narrower harness or leave that test Blocked.

## 3. Execute a baseline, challenge, and state check

Run a legitimate positive case first to show the fixture and instrumentation work. Change one relevant property for the negative case. Observe the response, persisted state and queued/downstream effects; a 403 or a reassuring screen does not prove that no mutation happened. Record exact observations, distinguishing a reproduced flaw from a code suspicion or an unexecuted hypothesis.

Stop after the smallest non-destructive proof that establishes the boundary failure. Do not enumerate other users, read extra records, collect credentials, establish persistence, evade controls or chain a demonstrated weakness into a larger compromise. A synthetic sentinel crossing a boundary can establish impact without exposing real information. Unexpected real data, a real payment/notification, new out-of-scope destination, instability, timeouts beyond the agreed abort condition or uncertain authorization stops the case immediately.

These examples illustrate execution, not additional authority:

| Case and controls | Bounded active attempt | Required observation and limitation |
|---|---|---|
| Two-user object/tenant access: AZ-02, AZ-03, AZ-06 | Create one synthetic record for each of two test tenants. Confirm the owner can read/update its record; then make one request using the other user's session and the known fixture ID. Include an approved list/export path where applicable. | The non-owner receives no protected fields and cannot alter the fixture or trigger a job. Retain redacted before/after state. Do not enumerate unknown IDs. Without the second identity or state visibility, record the missing test as Blocked. |
| Stored content and cross-role rendering: INPUT-10, INPUT-12 | Submit a unique inert marker containing markup metacharacters through a local contact/CRM/listing fixture. Open the relevant preview as a different synthetic role and inspect the DOM. When execution verification is explicitly scoped, use an isolated synthetic browser fixture whose only effect is an in-page marker; it must not read cookies/storage or make network requests. | Unexpected interpretation of inert markup is evidence of an unsafe rendering path, not automatically proof of script execution. A harmless marker test alone cannot pass all XSS criteria. Record actual parsing/execution observations, review contextual encoding/sanitization, and keep untested render paths visible. |
| Upload policy and serving isolation: FILE-01, FILE-02, FILE-04 | Upload tiny harmless MIME/extension/signature mismatches and an approved inert SVG/HTML fixture into disposable storage. Inspect direct viewing and administrator preview. If path containment is in scope, use only a synthetic sentinel beside the disposable directory. | Invalid types/paths are rejected or safely contained; permitted content is served under the intended isolation and headers. Never use malware, decompression bombs or system files. A rejected filename does not establish parser or preview safety; verify those separate paths or leave them untested. |
| Payment/CRM truth and duplicate delivery: PAY-01 through PAY-04 | Use a test-mode order and a CRM sink. Visit the return URL without successful payment; compare app and CRM state. Submit one altered amount/order fixture and one invalid-signature fixture. Deliver one valid synthetic event twice; use an approved two-request local transaction test only if concurrency is in scope. | Unpaid stays unpaid; invalid events cause no payment, fulfillment or CRM transition; duplicate delivery causes at most one business operation. Check persisted state and side effects, not just response codes. No real charges/refunds. If provider test mode or the CRM sink cannot be confirmed, block the affected cases. |
| Invitations and recovery: AUTH-07, AUTH-08 | Send one invitation to a local sink for a synthetic identity and tenant. Test wrong identity/tenant, changed requested role, one replay after redemption and expiry using a controlled clock. | Only the intended allowed grant succeeds once; expired/replayed tokens cannot grant access. Inspect role/membership state. Do not guess real tokens, send external invitations or reset customer accounts. Missing identity or clock control leaves those variants unverified. |
| Rate, size and query limits: ABUSE-01 through ABUSE-03 | Lower a limiter or query/body cap in an isolated test configuration, then exercise the boundary and one excess request/item. Use a small dataset and local outbound sink; assert cancellation/deadline behavior with a stub. | The server rejects or bounds excess work, counters have the intended scope, and queued/external effects remain bounded. Restore test settings and separately review the intended release configuration. A reduced-limit test is not a production capacity or DDoS-resilience result. Do not raise traffic to reach a production threshold. |

## 4. Close each case and remediate

Capture the build/environment, identity roles, timestamp, bounded request or test command, expected/observed result, relevant redacted response, persisted state and side effects. Use a trace/test ID or private evidence reference instead of real data. Record counts and whether the case hit a limit or stop condition. Mark the case Pass only when its actual criteria are satisfied; absence of an error, missing scanner output or a blocked attempt is never a pass.

When a failure is demonstrated, assign impact-based finding severity separately from catalog priority, identify the root cause and propose a concrete fix with an owner. Implement changes only within the user's authorized editing scope. After a permitted fix, repeat the original failing case, the legitimate positive case and nearby permissions/side effects against the exact new release artifact. Preserve the original evidence and link it to the retest. A scanner becoming green does not replace the regression test.

If an operation times out or its outcome is uncertain, inspect the synthetic operation ID and destination state before any retry. Do not repeat a payment, invite, reset or other mutation blindly. Clean up only known disposable records, restore test settings and confirm no test jobs remain queued. Record any incomplete cleanup as an operational issue for the owner.

## 5. Report what actually ran

Separate **executed and evidenced**, **reviewed without execution**, **not applicable with rationale**, and **blocked/untested** coverage in the final audit. Report the failing path, impact, fix, retest and remaining uncertainty in terms the owner can act on. State which tools and checks ran, rather than claiming the agent "hacked everything." Apply the release gates in [audit-protocol.md](audit-protocol.md): unresolved Critical/High findings and applicable untested/blocked Critical/High checks prevent an ordinary production-readiness recommendation.

Follow primary sources linked by the cited control IDs; the examples are bounded adaptations for synthetic local/staging verification. Refresh official stack advisories at audit time. A completed active review provides evidence within its scope, not a guarantee of hacker-proof software.
