# Routing Matrix

Use this as guidance, not a rigid scoring system. Choose the cheapest path that can reliably complete and verify the task.

| Signal | Direct | Guided | Orchestrated |
| --- | --- | --- | --- |
| Scope | local | subsystem / multi-file | cross-system / broad |
| Repository uncertainty | low | medium/high | medium/high with multiple boundaries |
| Risk | low | low/medium | high, or broad integration risk |
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

## Parallelism gate

Do not parallelize merely because the route is Orchestrated. Parallel work is justified only when package boundaries are explicit, write ownership does not overlap, interfaces are stable enough, and expected saved work exceeds coordination/context-transfer cost.
