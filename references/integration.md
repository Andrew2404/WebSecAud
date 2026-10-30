# Repository integration

Publishing this package on GitHub makes it available; it does not install it, guarantee discovery or force any agent to invoke it. No global settings need to change.

1. Review the package and pin a reviewed commit or release. Copy the complete `website-security-audit` skill folder into your agent's supported repository-local skill directory (for agents supporting it, `.agents/skills/website-security-audit/`). Keep `SKILL.md`, references, scripts and assets together. Check the actual agent's discovery conventions.
2. Add a repository policy in the applicable `AGENTS.md` or equivalent. Put it where it applies to release work, and adapt paths to the copied location. Do not overwrite existing instructions.
3. Add a human-owned release checklist and protected CI checks suitable for your stack. The skill is guidance, not an executable security scanner or branch-protection setting. Never put deployment/payment/cloud credentials into it.
4. Run the first review in local/staging with an approved scope. Save completed audit exports and evidence in an access-controlled location outside this public repository. Link a safe release record to the exact build.

Suggested repository instruction:

```text
Before recommending production readiness, use the repository-local
website-security-audit skill at .agents/skills/website-security-audit/SKILL.md.
During a requested review, recheck security-relevant changes to identity,
permissions, payments, uploads, data access, dependencies or infrastructure.
Record scope, authorization, applicability, evidence, findings and retests.
Critical/High unresolved findings or applicable untested/blocked Critical/High
checks block an ordinary readiness recommendation. Do not claim hacker-proof
or infer a pass from scanner success. Live testing needs its own valid scope;
this policy does not authorize production, destructive or third-party tests.
```

Explicit invocation example: `Use $website-security-audit to review this release. Code review and local synthetic tests are authorized; active network and production tests are out of scope.`

For active verification, explicitly identify the owned local/staging target and approved actions, test identities, numeric budget, stop criteria and cleanup. The skill then instructs the agent to execute feasible bounded negative tests and report actual observations. If those prerequisites are missing it must report the exact blocked test and continue independent permitted work. Installing a skill supplies guidance, not credentials, a running test environment or an autonomous scanner.

Use CI to enforce concrete checks such as dependency advisory review, secret scanning, targeted authorization/payment regression tests and approved infrastructure validation. Pin action dependencies to reviewed commit SHAs, minimize job permissions and keep untrusted pull-request code away from secrets. CI can require a signed-off audit artifact for a commit, but cannot determine security from a checkbox count. Do not configure automatic attack tools against production.

Update this package through reviewed changes. At each audit refresh the exact stack's supported-version status and official advisories, even when the package itself has not changed.
