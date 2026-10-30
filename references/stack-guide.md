# Stack and business-flow extensions

Read only the relevant sections after inventorying the deployed stack. These are routing notes for the detailed controls, not evidence that a framework default is enabled. Source versions and verified URLs are in [sources.md](sources.md); each control has direct source IDs in [controls.json](controls.json). Match documentation to the **deployed** version and refresh official advisories on the audit date.

## Next.js and Node.js

Treat Route Handlers, Server Actions, API routes and background tasks as independently reachable server entrypoints. Enforce session and object/action/tenant authorization near the data access, including actions called outside the expected UI flow. Middleware alone is insufficient evidence. Check serialized props, React Server Component data, `NEXT_PUBLIC_*`, source maps, static builds, shared caches, redirects and preview endpoints for unintended disclosure. Verify request-origin/CSRF handling and deployment/proxy configuration for the installed version. See STACK-01, STACK-02 and authorization controls; official [Next.js data-security guide](https://nextjs.org/docs/app/guides/data-security) and [Node.js security guide](https://nodejs.org/learn/getting-started/security-best-practices).

Inventory Node.js/Next.js/React versions and package-manager lockfiles; examine official framework/runtime security releases and affected transitive versions before release. Record affected/not affected with version and reachability evidence; do not dismiss an advisory only because a scanner missed it. Set server/proxy limits consistently for bodies, headers, timeouts and expensive computations. Check prototype pollution, unsafe object merges, command/template execution and process/container privilege.

## Python applications

Identify the actual framework and server (for example Django, Flask/FastAPI and WSGI/ASGI serving stack), exact supported versions and trusted proxy arrangement. Check production debug/error behavior, host validation, cookie/session and CSRF configuration, template escaping, ORM/raw queries, upload processing, serialization and subprocess use. Isolate parser/conversion workers and cap body, archive, query and task sizes. Do not deserialize untrusted pickle-like content. Interpreter and library extraction defaults vary by version; inspect explicit archive filters and destination containment. Use [Python security considerations](https://docs.python.org/3/library/security_warnings.html) and the actual framework's deployment/security documentation, such as [Django's versioned deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/). The Django link does not imply that every Python app uses Django or that 5.2 is the deployed version.

## ASP.NET Core / .NET

Review middleware order, authentication schemes, endpoint policies and resource authorization, antiforgery for cookie-authenticated state changes, model binding/mass assignment, Razor output encoding, file handling and exception details. Validate issuer/audience/algorithm/lifetime and signing-key rotation for JWT handlers. Check Data Protection key persistence, protection and application/tenant isolation where used. Configure forwarded headers only for trusted proxies/networks and validate host/origin interpretation. Confirm actual runtime/framework support and patched packages, container images and hosting module. See STACK-04 and official [ASP.NET Core security](https://learn.microsoft.com/en-us/aspnet/core/security/?view=aspnetcore-10.0) and [proxy guidance](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/proxy-load-balancer?view=aspnetcore-10.0), switching the documentation selector to the deployed version.

## Payments and CRM/Odoo

Define explicit states: created/pending/authorized/paid/failed/cancelled/refunded/disputed as appropriate to the provider. A success page or redirect is a display event, not proof of settlement. Derive amounts/currency/discounts/taxes and item identities on the server, bind provider objects to the correct local order/tenant, and verify the provider's authoritative event/state. Decide deliberately whether authorized versus captured/settled means paid for the business model.

In sandbox tests exercise failure/cancel/pending/delayed events, forged/invalid signatures, duplicate delivery, reordering, timeout/retry and reconciliation. Enforce durable idempotency across webhook processing, delivery, booking/inventory and CRM updates; a request-local flag is insufficient. Verify raw-body signature/timestamp handling for the actual provider, and only acknowledge success after the durable processing contract is met. Distinct events can refer to the same payment: guard the business operation as well as event IDs.

The regression invariant is: an unpaid or pending order cannot become fully paid in the application or CRM because a client visited the thank-you page or supplied a status flag. Use test payment objects and a synthetic CRM record; confirm persisted state and downstream effects, not only screen text. Keep payment data collection minimal and follow the provider's hosted/tokenized integration guidance; compliance obligations need separate scoping.

For Odoo, review access rights, record rules, field restrictions and public RPC methods; check `sudo`/superuser use, raw SQL and multi-company context. Confirm the actual Odoo version, installed modules and external API behavior. Integration service accounts should have only required tenant/company and object permissions. Treat CRM fields and webhook payloads as untrusted input; they can introduce stored XSS or trigger privileged workflows.

## Booking and auction logic

Write invariants for availability, capacity, hold expiry, one-time redemption, bid eligibility, minimum increments, deadline/timezone, auction closing, winner selection, refunds and settlement. Use controlled two-request races in isolated staging with agreed limits and synthetic inventory. Verify atomicity/transaction constraints and authoritative server time; prevent duplicates and inconsistent states after retries or partial failure. Never use real stock, real bidders or paid notifications to test these paths.

## AWS and deployment boundaries

Inspect effective exposure through DNS/CDN/load balancer, security groups, routing, public IPs, origin restrictions and application authentication. Binding a process to `0.0.0.0` means it listens on all local interfaces; whether that creates unintended public access depends on these other boundaries. Do not report the bind address alone as a vulnerability. CORS is a browser read-access policy, not server authentication or a network firewall; wildcard access can be intentional for public noncredentialed assets.

Use read-only configuration/IaC review first for IAM trust/permission/resource policies, role assumption, workload identity, S3 public access, encryption/KMS, secrets, egress and origin access. Test negative access only against owned synthetic resources within scope. Use a local metadata-service stub for SSRF cases rather than requesting real workload credentials. Check private administration access, backups and recoverability, account/audit boundaries, alert delivery and incident ownership. Account for the shared-responsibility boundary for each actual AWS service.

## Every release: advisory and supply-chain refresh

Record date, tool/database version, exact dependency inventory and official advisory/support sources for runtime, framework, packages, Odoo modules, operating system/base image, web server/proxy and deployed services. Include transitive/dev/build dependencies capable of affecting shipped code or secrets. Reconcile scanner results with vendor affected/fixed ranges, lockfiles and deployed artifacts. Evaluate vendor workarounds as temporary risk decisions with expiry; retest updates. This document intentionally avoids a frozen list of CVEs, which would become incomplete immediately.

Include new surfaces such as AI tools, retrieval, browser extensions or customer-provided plugins only when present. Constrain AI retrieval and tool authorization outside model prompts, validate outputs and require meaningful approval for consequential actions; prompt text is not an access-control boundary.
