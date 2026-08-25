---
name: adaptive-routing
description: Automatically classify a coding task by scope, uncertainty, risk, and parallelizability, then choose the cheapest reliable execution path. Use for non-trivial coding work when the user did not explicitly choose an execution strategy.
---

# Adaptive Routing

Choose execution depth per task. Do not make route selection part of the user's required vocabulary.

## First classify

Assess only what is needed to route:

- **Scope:** local, subsystem, cross-system.
- **Uncertainty:** low, medium, high.
- **Risk:** low, medium, high.
- **Parallelizability:** none, limited, strong.

Treat security/auth, destructive data changes, migrations, public API contracts, concurrency, deployment, and irreversible operations as elevated risk.

## Choose the cheapest reliable path

### Direct

Use when the task is local, well understood, low risk, and can be verified cheaply.

- Read only relevant files.
- Load only relevant skills.
- Implement directly.
- Run targeted verification.
- Do not delegate merely because delegation exists.

### Guided

Use when the task spans multiple files, repository context is uncertain, or a short plan materially reduces mistakes.

- Apply `codebase-exploration` if context is not already sufficient.
- Apply `implementation-planning` when ordering, interfaces, or acceptance criteria matter.
- Main agent executes unless delegation has a clear benefit.
- Apply `verification` before claiming completion.

### Orchestrated

Use when work is cross-system, high risk, or contains multiple genuinely independent workstreams.

- Explore before partitioning.
- Plan interfaces and dependencies centrally.
- Apply `work-package-dispatch` only when package boundaries are clean.
- Executors receive bounded context, not whole-session history.
- Integrate centrally.
- Apply independent verification for high-risk or broad changes.

## Escalate and downgrade dynamically

Routing is per task, not sticky across the session.

Escalate when discovery reveals broader scope, hidden dependencies, risk, or useful parallel work. Downgrade when apparent complexity collapses to a local change.

Explicit user instructions override automatic routing unless they conflict with safety requirements.

## Delegation gate

Delegate only when at least one is true:

- Context isolation will materially reduce main-agent load.
- Workstreams can progress independently with explicit ownership.
- Independent review materially improves confidence.
- Specialized investigation is cheaper than loading the same context into the orchestrator.

If delegation overhead is likely greater than the work itself, execute directly.

## Output discipline

Do not narrate internal route labels unless useful to the user. Report decisions, changes, verification, and unresolved risks instead.
