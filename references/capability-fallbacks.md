# Capability Fallbacks

`ag-flow` is runtime-agnostic. Skills describe semantic roles; each coding agent maps those roles to capabilities it actually has.

## Semantic roles

- **Orchestrator** — owns task routing, architecture, package boundaries, integration, and final claims.
- **Explorer** — read-only repository/context discovery.
- **Executor** — implements one bounded package.
- **Reviewer** — independently verifies risky or broad work.

## Capability mapping

### Runtime supports subagents and parallelism

Use delegated roles when the routing and parallelism gates justify the overhead. Keep context bounded per role.

### Runtime supports subagents but not parallelism

Delegate isolated exploration/review when useful. Execute dependent work packages sequentially.

### Runtime has no subagents

The main agent executes the same role transitions sequentially:

1. exploration pass
2. planning/orchestration pass
3. bounded package execution passes
4. independent second-pass verification

Preserve package boundaries even when one agent performs every role. If `agf-route-adaptive` set `needs.delegation: true` but the runtime has no subagents, do not reinterpret that as `false` — the packages and their ownership boundaries from `agf-dispatch-package` still apply, only the execution mechanism changes from parallel/isolated to sequential in the main agent.

### Runtime lacks a dedicated planning/todo tool

Maintain the plan in working context or the repository's existing task/documentation convention. Do not create framework-specific state files unless persistence is genuinely needed.

### Runtime cannot run commands

Use static inspection only as a fallback and explicitly report that executable verification was unavailable. Do not describe static confidence as runtime verification.

## Model tiering across runtimes

When the runtime supports specifying models or subagent profiles, map semantic roles to cost and reasoning tiers while allowing risk-based escalation:

| Semantic Role | Default Tier | Purpose & Constraints | Example Models |
| --- | --- | --- | --- |
| **Orchestrator** | High / Inherit | Global architecture, decomposition, planning, integration | Default session model, Pro / Opus / GPT-4o |
| **Explorer** | Cheap / Fast | Bounded read-only discovery, symbol searches, interface extraction | Flash-Lite, Flash, Haiku, GPT-4o-mini |
| **Executor** | Cheap / Fast | Bounded implementation with explicit contracts and deterministic self-verification; escalate when risk/complexity remains high | Flash-Lite, Flash, Haiku, GPT-4o-mini |
| **Reviewer** | Balanced / Mid-tier | Nuanced evaluation of spec fidelity, regression risk, and invariants within a relevance-bounded perimeter | Flash, Sonnet, GPT-4o |

### Why cheap tier by default for code execution?

- **Speed and efficiency:** Many bounded coding packages do not require expensive frontier models.
- **Reduced ambiguity:** Minimal coherent scope, explicit writable targets, unambiguous contracts, and deterministic verification reduce unsupported assumptions and hallucination risk.
- **Evidence still wins:** Cheap-tier execution is an optimization, not a correctness guarantee. Verification remains mandatory.

Escalate an executor from `cheap` to `balanced` when a bounded package is still cognitively or operationally risky: security-critical logic, concurrency/distributed state, tricky migrations, unfamiliar or underspecified APIs, or repeated executor/verification failure.

### Why balanced tier with bounded perimeter for review?

- **Nuanced reasoning:** Catching subtle spec divergences or regression edge cases often benefits from balanced reasoning.
- **Anti-sprawl constraint ("khoanh vùng"):** Bound review by relevance to the affected behavior. Permit inspection of directly relevant callers, callees, interfaces, contracts, and tests, while forbidding unrelated architectural critique, style bikeshedding, and scope expansion.

## Portability rules

Skills must not require runtime-specific tool names, model names, or proprietary agent types. Runtime adapters may optimize execution, but the core behavioral contract must remain understandable without them.

Prefer capability statements such as "delegate to a read-only explorer if supported" over commands such as "call spawn_agent(type=explorer)".
