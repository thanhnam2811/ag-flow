# ag-flow

Adaptive, agent-agnostic workflow skills for coding agents.

`ag-flow` combines bounded-context orchestration, progressive skill loading, execution-based verification, and automatic task routing without tying the workflow to one model or runtime.

## Design principles

- Minimum necessary context
- Minimum necessary delegation
- Maximum verification confidence
- Route per task, not per session
- Prefer semantic roles over runtime-specific tool names
- Degrade gracefully when subagents or parallelism are unavailable
- Preserve project-native instructions such as `AGENTS.md` and `CLAUDE.md`

## Install

Install all skills with the Skills CLI:

```bash
npx skills add thanhnam2811/ag-flow --skill '*'
```

Or install only the skills you want:

```bash
npx skills add thanhnam2811/ag-flow --skill adaptive-routing --skill verification
```

Target supported agents through the CLI, for example Claude Code and Codex:

```bash
npx skills add thanhnam2811/ag-flow --agent claude-code --agent codex --skill '*'
```

## Core skills

| Skill | Purpose |
| --- | --- |
| `adaptive-routing` | Classify each task and select the cheapest reliable execution path |
| `codebase-exploration` | Discover only the repository context needed for the task |
| `implementation-planning` | Turn findings into an executable, dependency-aware plan |
| `work-package-dispatch` | Split complex work into bounded, non-overlapping packages |
| `work-package-execution` | Execute one package with strict ownership and concise reporting |
| `verification` | Verify claims through execution with risk-aware depth |
| `systematic-debugging` | Debug from evidence and hypotheses instead of speculative edits |
| `session-handoff` | Persist only the minimum state needed to resume work safely |

## Runtime model

The skills use semantic roles instead of hard-coded agent APIs:

- **Orchestrator** — owns global decisions and integration
- **Explorer** — performs read-only context discovery
- **Executor** — implements a bounded work package
- **Reviewer** — independently verifies risky or complex changes

If a runtime supports subagents, these roles may be delegated. If it does not, the same boundaries should be executed sequentially by the main agent.

## Routing model

The public workflow does not require users to choose Light / Medium / Heavy modes. Internally, `adaptive-routing` selects among:

1. **Direct** — local, low-risk work; main agent executes directly.
2. **Guided** — multi-file or uncertain work; explore, plan, execute, verify.
3. **Orchestrated** — cross-system, high-risk, or truly parallel work; bounded packages, delegated execution where useful, independent verification.

Explicit user instructions always override automatic routing.

## Repository layout

```text
skills/
  adaptive-routing/
  codebase-exploration/
  implementation-planning/
  work-package-dispatch/
  work-package-execution/
  verification/
  systematic-debugging/
  session-handoff/
references/
  routing-matrix.md
  work-package-contract.md
  verification-levels.md
  capability-fallbacks.md
tests/
  routing-cases.md
  adversarial-cases.md
```

## Status

Initial core workflow. Domain-specific skills can be layered on top without changing the orchestration model.
