---
name: agf-route-adaptive
description: Automatically classify a coding task by scope, uncertainty, risk, and parallelizability, then choose the cheapest reliable execution path and which gated skills apply. Use for non-trivial coding work when the user did not explicitly choose an execution strategy.
---

# Adaptive Routing

Choose execution depth per task. Do not make route selection part of the user's required vocabulary.

**Route controls execution depth. Gates control skill activation. Capability controls execution mechanism.** Keep these three separate: a route is not a fixed skill list, a missing runtime capability changes *how* a gate is fulfilled (see `references/capability-fallbacks.md`) but never which route was chosen.

## First classify

Assess only what is needed to route:

- **Scope:** local, subsystem, cross-system.
- **Uncertainty:** low, medium, high.
- **Risk:** low, medium, high.
- **Parallelizability:** none, limited, strong.

Treat security/auth, destructive data changes, migrations, public API contracts, concurrency, deployment, and irreversible operations as elevated risk.

Keep these dimensions separate. Risk primarily raises verification depth and review requirements; it does not by itself justify orchestration. Read-only work can still require Guided execution when repository ownership, provenance, or dependencies are uncertain.

## Three kinds of "not sure"

Do not treat every kind of uncertainty the same way — each has a cheaper, more specific fix than asking the user everything up front:

| Type | Question it answers | Resolve with |
| --- | --- | --- |
| **Routing uncertainty** | Which execution depth fits this task? | Cheap inspection, then at most one routing question (below) |
| **Requirement uncertainty** | What exactly should the resulting behavior be? | `agf-spec-clarify` |
| **Implementation uncertainty** | We know what to build, not yet where/how the repo does it | `agf-explore-code` |

Do not let `agf-spec-clarify` and `agf-explore-code` cover for each other. A missing requirement is not resolved by reading more code, and an unknown file/symbol is not resolved by asking the user.

## Resolve routing uncertainty cheaply

When the route itself is unclear, work through this order — do not jump straight to asking:

1. Can the route be resolved from the prompt alone? → route.
2. If not, does one bounded, cheap inspection resolve it (one file read, one symbol search, one directory listing)? → inspect, then route.
3. If scope/risk stays materially ambiguous **and** different answers would select materially different execution paths → ask exactly one routing question with a recommended default, e.g. *"This touches auth, so I'd route it Guided with Level 2 verification — say so if you want it treated as a purely local change."* Do not ask an open-ended "what's the scope of this?" when a cheap read already answers it.
4. Otherwise, choose the cheapest reliable route.

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

- Apply `agf-explore-code` if context is not already sufficient, including read-only provenance or ownership investigation.
- Apply `agf-plan-impl` when ordering, interfaces, or acceptance criteria matter.
- Main agent executes unless delegation has a clear benefit.
- Apply `agf-verify-confidence` before claiming completion.
- Prefer stronger verification over a heavier route when the work remains one coherent workstream but carries elevated risk.

### Orchestrated

Use when work is cross-system or contains multiple genuinely independent workstreams whose separation creates material execution or context benefit.

High risk alone is not enough. A single billing, auth, migration, or other business-critical workstream may remain Guided with Level 2/3 verification and independent review.

- Explore before partitioning.
- Plan interfaces and dependencies centrally.
- Apply `agf-dispatch-package` only when package boundaries are clean.
- Executors receive bounded context, not whole-session history.
- Integrate centrally.
- Apply independent verification for high-risk or broad changes.

## Emit a compact execution contract

After classifying, settle the route and which gates apply as a short internal contract — a reasoning aid, not a schema to persist or pass between agents:

```yaml
route: guided
verification: 2

needs:
  clarification: false   # agf-spec-clarify
  exploration: true      # agf-explore-code
  planning: false        # agf-plan-impl
  tdd_gate: true          # behavior-change gate in agf-exec-package / agf-verify-confidence
  delegation: false       # agf-dispatch-package + agf-exec-package
  handoff: false          # agf-session-handoff
```

The route sets verification depth and the general ceiling of effort. Each `needs` flag is decided by that gate's own trigger condition — documented in its own skill — not by the route name alone. A Direct task can still need `tdd_gate: true` if it changes behavior and a test harness already exists. An Orchestrated task can still have `delegation: false` if exploration shows only one real executor remains. See `references/routing-matrix.md` for the core-vs-conditional table per route.

## Escalate and downgrade dynamically

Routing is per task, not sticky across the session.

Escalate when discovery reveals broader scope, hidden dependencies, or useful independent workstreams. Raise verification independently when discovery reveals risk. Downgrade when apparent complexity collapses to a local change.

Explicit user instructions override automatic routing unless they conflict with safety requirements. Treat execution constraints precisely: "no subagents" or "do it yourself" disables delegation, but does not force Direct if exploration or planning is still needed. A user who explicitly requests a specific execution path may override the automatic route when that path remains safe and sufficient.

## Delegation gate

Delegate only when at least one is true:

- Context isolation will materially reduce main-agent load.
- Workstreams can progress independently with explicit ownership.
- Independent review materially improves confidence.
- Specialized investigation is cheaper than loading the same context into the orchestrator.

Independent review is a verification role, not automatically another implementation workstream.

If delegation overhead is likely greater than the work itself, execute directly or keep the main agent as the sole executor.

## Output discipline

Do not narrate internal route labels or the `needs` contract unless useful to the user — e.g. to explain why a skill was or wasn't used. Report decisions, changes, verification, and unresolved risks instead.
