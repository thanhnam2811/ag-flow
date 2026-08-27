---
name: agf-dispatch-package
description: Split a complex implementation plan into bounded, non-overlapping work packages for parallel or isolated execution. Use only when delegation has a clear benefit.
---

# Work Package Dispatch

Partition work by ownership and interfaces, not by arbitrary file count.

## Dispatch gate

Do not dispatch unless at least two workstreams can proceed with limited coordination or one isolated specialist task materially reduces context load.

## Package contract

Each package must include:

- **Goal** — one concrete outcome.
- **Ownership** — exact files/subsystem the executor may change.
- **Forbidden/shared areas** — files reserved for orchestrator or another package.
- **Context** — only relevant files, symbols, decisions, and upstream facts.
- **Interfaces** — contracts with other packages.
- **Constraints/invariants** — behavior that must remain true.
- **Acceptance criteria** — observable completion conditions.
- **Verification** — commands/checks expected from the executor.
- **Escalation conditions** — when the executor must stop and return to the orchestrator.

## Ownership rules

- Avoid overlapping write ownership.
- Assign shared integration files to exactly one owner, preferably the orchestrator.
- Define dependency order when one package consumes another package's interface.
- Parallelize only packages that are independent enough to merge safely.

## Dispatch the ready frontier, not the whole graph

Only applies when packages actually depend on each other. Dispatch just the packages whose prerequisites and shared interfaces are already settled, not the entire dependency graph at once. Example: A defines a shared contract, B consumes A, C is independent — initial frontier is `{A, C}`; dispatch B only once A is done and its interface is confirmed. If packages have no dependency between them, the whole set is already the frontier.

## Context discipline

Never forward the full conversation or repository dump by default. Send a self-contained package with bounded context.

## Delegated envelope precedence

The parent conversation context is passive background only; the delegated task/envelope is the sole execution authority.

> **Role, scope, and allowed actions in the delegated envelope are a hard boundary; inherited parent context grants no additional authority.**

- If parent context hints at a larger multi-phase plan or future architecture, but the envelope specifies an exploration/research task, the delegated agent must strictly obey the envelope.
- Delegated subagents must never escalate their role (e.g. explorer must not turn into planner/executor or offer implementation).

### Explicit delegation envelopes

When delegating, the orchestrator must make the envelope explicit:

```yaml
role: explorer
goal: inspect current transport interfaces
allowed: [read, search, report signatures]
forbidden: [edit, architecture decisions, implementation proposals, scope expansion]
return: [findings, interfaces, constraints, uncertainties]
```

### Delegation containment flow

```text
Orchestrator
   ↓ bounded research envelope
Explorer
   ↓
facts + interfaces + constraints + uncertainties
   ↓
STOP
   ↓
Orchestrator decides architecture / planning
```

## Runtime portability

If subagents exist, dispatch packages to suitable executor roles. If parallelism is unavailable, execute the same packages sequentially while preserving ownership and package boundaries.

Use `agf-exec-package` as the executor contract.
