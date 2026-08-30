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
- **Model tier** (optional) — recommended cost tier for this package (`cheap`, `balanced`).

## Model tiering for delegated roles

Match model tiers to the cognitive requirements of each semantic role:

- **Code Executor** — use **cheap / fast tier** (e.g. `flash_lite`, `flash`, `haiku`, `gpt-4o-mini`). Implementing code against a bounded specification does not require expensive frontier models.
- **Reviewer** — use **balanced / mid tier** (e.g. `flash`, `sonnet`, `gpt-4o`). Independent review requires nuanced reasoning to evaluate spec fidelity and edge cases, but does not require expensive orchestration models.
- **Explorer** — use **cheap / fast tier** (read-only search, inspection, and signature extraction).
- **Orchestrator** — uses the session's default/high model to own architecture, boundary setting, and final integration.

## Atomic scoping and task clarity (Anti-hallucination & speed)

Cheap models execute fastest and with zero hallucinations when the task is atomic and explicit:

1. **Smallest coherent scope** — carve packages into single-responsibility units (1-2 tightly coupled files, a specific function, or an isolated test slice). Never give an executor an open-ended multi-subsystem assignment.
2. **Explicit, unambiguous contracts** — specify exact writable target files, exact symbol names, expected method signatures, and forbidden areas. Do not force the executor to guess architectural decisions.
3. **Deterministic verification** — supply exact, executable commands (e.g. targeted unit test, lint command) so the executor can verify its own output without subjective speculation.
4. **Immediate escalation over guessing** — if any requirement or contract is missing, the executor must halt and return to the orchestrator instead of hallucinating code.

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

When delegating, the orchestrator must make the envelope explicit.

#### Explorer envelope (read-only discovery)

```yaml
role: explorer
model_tier: cheap
goal: inspect current transport interfaces
allowed: [read, search, report signatures]
forbidden: [edit, architecture decisions, implementation proposals, scope expansion]
return: [findings, interfaces, constraints, uncertainties]
```

#### Reviewer envelope (bounded review perimeter)

When dispatching an independent reviewer subagent, strictly bound the review perimeter to avoid sprawling commentary or style bikeshedding:

```yaml
role: reviewer
model_tier: balanced
goal: verify auth middleware fix against acceptance criteria and regression risks
target_diff: [src/auth/middleware.ts, tests/auth/middleware.test.ts]
allowed: [verify spec fidelity, check regression risks in touched area, inspect verification evidence]
forbidden: [review untouched files, subjective style bikeshedding, unsolicited architectural refactoring, re-implementing]
return: [spec_fidelity, engineering_confidence, findings, residual_risk]
```

### Delegation containment flow

```text
Orchestrator (High / Inherit)
   │
   ├── bounded research envelope (Cheap tier) ──► Explorer
   │                                                 │ facts & interfaces only
   │                                                 ▼ STOP
   ├── bounded atomic package (Cheap tier) ─────► Executor
   │                                                 │ minimal scope, code + self-verify
   │                                                 ▼ STOP
   └── bounded review envelope (Balanced tier) ─► Reviewer
                                                     │ spec fidelity & regressions only
                                                     ▼ STOP
Orchestrator integrates and verifies claims
```

## Runtime portability

If subagents exist, dispatch packages to suitable executor roles. If parallelism is unavailable, execute the same packages sequentially while preserving ownership and package boundaries.

Use `agf-exec-package` as the executor contract.
