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

Match model tiers to the cognitive requirements and risk of each semantic role:

- **Code Executor** — default to **cheap / fast tier** for bounded, unambiguous implementation with deterministic verification. Escalate to **balanced** when the package is security-critical, concurrency/state-heavy, migration-sensitive, dependent on unfamiliar or underspecified APIs, or repeatedly fails execution/verification.
- **Reviewer** — use **balanced / mid tier** for independent evaluation of spec fidelity and edge cases.
- **Explorer** — use **cheap / fast tier** for read-only search, inspection, and signature extraction.
- **Orchestrator** — use the session's default/high model to own architecture, boundary setting, and final integration.

Model tier is an optimization hint, not a correctness guarantee. Verification evidence remains authoritative.

## Atomic scoping and task clarity (Risk reduction & speed)

Bounded explicit packages reduce ambiguity and hallucination risk, especially on cheaper model tiers:

1. **Smallest coherent decision boundary** — carve packages into independently verifiable single-responsibility units. File count is illustrative, not a target; a coherent interface + implementation + tests slice may span several tightly coupled files.
2. **Explicit, unambiguous contracts** — specify writable targets, relevant symbols/interfaces, expected behavior, and forbidden areas. Do not force the executor to guess architectural decisions.
3. **Deterministic verification** — supply exact executable commands where possible so the executor can verify its own output.
4. **Immediate escalation over guessing** — if a missing requirement or contract would materially change the implementation, halt and return to the orchestrator instead of inventing assumptions.

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

When dispatching an independent reviewer subagent, bound review by relevance rather than by Git diff alone:

```yaml
role: reviewer
model_tier: balanced
goal: verify auth middleware fix against acceptance criteria and regression risks
target_diff: [src/auth/middleware.ts, tests/auth/middleware.test.ts]
allowed: [verify spec fidelity, inspect directly relevant callers/callees/contracts/tests, check regression risks in affected area, inspect verification evidence]
forbidden: [critique unrelated untouched code, subjective style bikeshedding, unsolicited architectural refactoring, re-implementing]
return: [spec_fidelity, engineering_confidence, findings, residual_risk]
```

### Delegation containment flow

```text
Orchestrator (High / Inherit)
   │
   ├── bounded research envelope (Cheap tier) ──► Explorer
   │                                                 │ facts & interfaces only
   │                                                 ▼ STOP
   ├── bounded package (Cheap default; escalate by risk) ─► Executor
   │                                                 │ coherent scope, code + self-verify
   │                                                 ▼ STOP
   └── relevance-bounded review envelope (Balanced tier) ─► Reviewer
                                                     │ spec fidelity & regressions only
                                                     ▼ STOP
Orchestrator integrates and verifies claims
```

## Runtime portability

If subagents exist, dispatch packages to suitable executor roles. If parallelism is unavailable, execute the same packages sequentially while preserving ownership and package boundaries.

Use `agf-exec-package` as the executor contract.
