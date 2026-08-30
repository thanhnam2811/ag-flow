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

When the runtime supports specifying models or subagent profiles, map semantic roles to cost and reasoning tiers:

| Semantic Role | Model Tier | Purpose & Constraints | Example Models |
| --- | --- | --- | --- |
| **Orchestrator** | High / Inherit | Global architecture, decomposition, planning, integration | Default session model, Pro / Opus / GPT-4o |
| **Explorer** | Cheap / Fast | Bounded read-only discovery, symbol searches, interface extraction | Flash-Lite, Flash, Haiku, GPT-4o-mini |
| **Executor** | Cheap / Fast | Rapid code implementation of atomic, unambiguous packages; deterministic self-verification | Flash-Lite, Flash, Haiku, GPT-4o-mini |
| **Reviewer** | Balanced / Mid-tier | Nuanced evaluation of spec fidelity, regression risk, and invariants within bounded perimeter | Flash, Sonnet, GPT-4o |

### Why cheap tier for code execution?

- **Speed and efficiency:** Bounded coding packages do not require expensive frontier models.
- **Anti-hallucination guarantee:** Hallucination occurs when cheap models are handed ambiguous, sprawling tasks or forced to make architectural decisions. When the orchestrator provides **minimal atomic scope**, **explicit writable targets**, **unambiguous contracts**, and **deterministic verification commands**, cheap models execute near-instantly with zero hallucination.

### Why balanced tier with bounded perimeter for review?

- **Nuanced reasoning:** Catching subtle spec divergences or regression edge cases requires balanced reasoning that smaller/cheaper models often miss.
- **Anti-sprawl constraint ("khoanh vùng"):** Even capable reviewer models degrade if allowed to wander. Restricting reviewer input strictly to the assigned diff, contract, and verification hooks prevents stylistic nitpicking, subjective bikeshedding, and out-of-scope architectural sprawl.

## Portability rules

Skills must not require runtime-specific tool names, model names, or proprietary agent types. Runtime adapters may optimize execution, but the core behavioral contract must remain understandable without them.

Prefer capability statements such as "delegate to a read-only explorer if supported" over commands such as "call spawn_agent(type=explorer)".
