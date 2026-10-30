# Example-only handoff: static checkout fixture

This is a teaching example, not a website audit. No server or target was contacted. The corresponding [ledger](ledger-dry-run.json) records a No decision for active testing and separately permitted offline review of a synthetic text fixture.

**Decision: blocked for any real release recommendation.** Only the supplied [fixture](unsafe-checkout.txt) was inspected; application context and runtime behavior are unavailable. Active authorization, invitation and load checks remain explicitly unrun.

| Ledger ID | Result | Evidence and limitation |
|---|---|---|
| EX-001 | Failed, offline code review | The fixture's line 4 calls `orders.markPaid` from a client-controlled return-page path. This is a code-level state-transition flaw in the fictional snippet, not evidence of runtime exploitability in a real system. |
| EX-002 | Blocked | No approved target, test identities, runtime or observable persisted state. |
| EX-003 | Skipped | No separate local/staging load approval or health budget; no DDoS or load traffic was attempted. |
| EX-004 | Not run | Active decision is No and no test account or approved attempt cap exists. |

**F-EX-001 — High, fictional checkout state transition.** If a real application used this path, visiting a return URL could mark an unpaid order paid. The exact supported proposed edit is to remove `orders.markPaid(request.query.orderId)` from this return handler. The return page should display authoritative stored state. The provider event handler is absent, so adding signature verification, order/amount/currency binding and durable idempotency there is conditional guidance pending inspection of that code and provider version; no fabricated patch is supplied.

Retest after a permitted fix: with payment test mode and a CRM sink, visit the return URL for one unpaid synthetic order and confirm app/CRM state stays unpaid; then verify a valid paid event transitions once, a duplicate does not repeat fulfillment, and invalid/mismatched events do not mutate state. These are **planned**, not executed. The original failing evidence remains in the ledger; no fix effectiveness or runtime pass is claimed.

Handoff: a real owner must provide the exact source/build, scope, synthetic identities, payment sandbox and integration sink, numeric aggregate budgets, stop conditions and cleanup plan before runtime cases can proceed. The example has no real accountable owner, authorization or infrastructure. Its `exampleOnly` flag must remain true.
