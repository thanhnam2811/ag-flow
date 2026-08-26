# Routing Matrix

Use this as guidance, not a rigid scoring system. Choose the cheapest path that can reliably complete and verify the task.

| Signal | Direct | Guided | Orchestrated |
| --- | --- | --- | --- |
| Scope | local | subsystem / multi-file | cross-system / broad |
| Repository uncertainty | low | medium/high | medium/high with multiple boundaries |
| Risk | low | any, if the work stays one coherent workstream | broad integration/cross-system risk (high risk alone is not enough) |
| Parallel benefit | none | usually none | strong and cleanly partitionable |
| Planning need | little | useful | required |
| Independent review | optional | risk-dependent | normally required |

## Strong Direct examples

- local bug with known cause
- small validation change
- rename or targeted cleanup
- explain or inspect code without modification
- one-file test update with clear behavior

## Strong Guided examples

- multi-file feature within one subsystem
- bug whose ownership is unclear
- refactor with known architecture but several call sites
- dependency upgrade requiring targeted compatibility work

## Strong Orchestrated examples

- full-stack feature with separable backend/frontend work
- migration plus application changes
- cross-package contract change
- broad refactor with independently owned modules
- implementation where independent security/reliability review is valuable

## Risk overrides

Raise verification depth for:

- authentication/authorization
- secrets or security boundaries
- schema/data migration
- destructive operations
- public API/protocol contracts
- concurrency and distributed state
- deployment/release behavior

High risk does not automatically require many executors. It does require stronger planning and verification.

## Skill activation by route

Route sets the ceiling of effort and verification depth. It does not fix which skills run — that is decided by each skill's own gate (see `skills/agf-route-adaptive/SKILL.md`'s `needs` contract).

| Route | Core (always) | Conditional (only if that skill's own gate fires) |
| --- | --- | --- |
| Direct | `agf-route-adaptive`, `agf-verify-confidence` L1 | any gate can still fire if genuinely triggered (e.g. a small behavior change with an existing test harness triggers the TDD gate) |
| Guided | `agf-route-adaptive`, `agf-verify-confidence` L2 | `agf-spec-clarify`, `agf-explore-code`, `agf-plan-impl`, TDD gate |
| Orchestrated | `agf-route-adaptive`, `agf-plan-impl`, `agf-verify-confidence` L3 | `agf-explore-code` (skip only if context is already sufficient), `agf-dispatch-package`/`agf-exec-package` (only with ≥2 genuinely independent work packages), `agf-spec-clarify`, TDD gate, `agf-debug-systematic`, `agf-session-handoff` |

Two rules keep this from becoming a checklist:

- **Never gate a problem-solving primitive by route.** `agf-debug-systematic` and the TDD gate are useful at any route — a Direct "fix this null check, it's already reproduced" task should still use systematic debugging if that's the actual primitive needed. Gate them by their own trigger (a bug exists; a test harness exists), not by route name.
- **Do gate orchestration primitives by real package count, not by route.** `agf-dispatch-package`/`agf-exec-package` require at least two genuinely independent, non-overlapping workstreams (see that skill's own dispatch gate). An Orchestrated-scope task with only one viable executor after exploration stays single-executor — Orchestrated justifies central planning and Level 3 review, not delegation for its own sake.

## Parallelism gate

Do not parallelize merely because the route is Orchestrated. Parallel work is justified only when package boundaries are explicit, write ownership does not overlap, interfaces are stable enough, and expected saved work exceeds coordination/context-transfer cost.
