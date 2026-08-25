# Routing Cases

These cases are a behavioral test corpus for `adaptive-routing`. Expected routes are guidance; implementations may choose a stronger path when repository evidence reveals additional risk.

| # | Prompt | Expected | Why |
| --- | --- | --- | --- |
| 1 | Fix a typo in this README heading. | Direct | local and trivial |
| 2 | Rename this private helper and update its two callers. | Direct | bounded low-risk change |
| 3 | Add validation rejecting negative page sizes in this endpoint. | Direct | local behavior with cheap tests |
| 4 | Explain why this function returns stale data. | Direct | inspection only unless broader evidence appears |
| 5 | Add one focused unit test for the parser edge case. | Direct | isolated test work |
| 6 | Fix pagination; I do not know where it is implemented. | Guided | ownership/context uncertain |
| 7 | Add a feature touching controller, service, and tests in one module. | Guided | multi-file subsystem work |
| 8 | Upgrade a dependency and fix compatibility errors in this package. | Guided | discovery + targeted plan useful |
| 9 | Refactor this service interface and all consumers in one package. | Guided | multi-file contract work, usually sequential |
| 10 | Debug an intermittent test failure. | Guided | evidence gathering before edits |
| 11 | Add forgot-password across API, mailer, UI, and integration tests. | Orchestrated | separable cross-system work |
| 12 | Migrate user IDs and update application code that consumes them. | Orchestrated | migration + contract risk |
| 13 | Replace auth middleware across multiple services. | Orchestrated | security-sensitive cross-system change |
| 14 | Split a monolith module into three packages with stable interfaces. | Orchestrated | broad architecture and package boundaries |
| 15 | Implement backend and frontend independently against an agreed API. | Orchestrated | strong parallel benefit |
| 16 | Add a database index for one known slow query. | Guided | data-layer risk merits planning/verification, not necessarily delegation |
| 17 | Change one auth condition in a known file. | Guided | local scope but elevated security risk |
| 18 | Delete unused CSS classes across one file. | Direct | cheap local cleanup |
| 19 | Apply the same mechanical rename in 40 independent files. | Guided | broad but little architecture; delegation optional by cost |
| 20 | Rewrite one core algorithm used by billing. | Guided | one workstream; high business risk raises verification rather than orchestration |
| 21 | Add three independent adapters implementing an existing stable interface. | Orchestrated | clean parallel packages |
| 22 | Update docs after a completed code change. | Direct | documentation-only bounded work |
| 23 | Investigate where this config value comes from; do not edit. | Guided | read-only exploration still needs repository discovery |
| 24 | Do this yourself; do not use subagents. | Guided without delegation | execution constraint disables delegation, while unknown ownership still requires discovery |
| 25 | User explicitly requests independent security review. | route by implementation scope + Level 3 verification | review requirement is orthogonal to executor count |

## Assertions

A router should fail this corpus if it:

- defaults every multi-file task to Orchestrated
- uses agent count as a proxy for quality
- treats elevated risk alone as sufficient reason to orchestrate
- treats read-only work as automatically Direct despite unresolved repository uncertainty
- converts a no-subagent constraint into a Direct route when exploration or planning is still needed
- ignores security/data risk because a change is one-file
- keeps the previous task's route automatically
- delegates when package boundaries overlap heavily
- reports route ceremony to the user when it adds no value
