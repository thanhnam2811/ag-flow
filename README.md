# ag-flow

**Adaptive, agent-agnostic workflow skills for coding agents.**

[![Validate](https://github.com/thanhnam2811/ag-flow/actions/workflows/ci.yml/badge.svg)](https://github.com/thanhnam2811/ag-flow/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-111827)](https://skills.sh/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-supported-7C3AED)](https://docs.anthropic.com/en/docs/claude-code)
[![Codex](https://img.shields.io/badge/Codex-supported-111827)](https://openai.com/codex/)

`ag-flow` gives coding agents a portable execution workflow built around bounded context, adaptive routing, progressive delegation, and execution-based verification. It is designed to work across runtimes instead of encoding one model's tool API.

> **Minimum necessary context. Minimum necessary delegation. Maximum verification confidence.**

## Why ag-flow?

Coding-agent workflows often fail in one of two ways: they stay too lightweight for complex work, or they over-orchestrate simple tasks and waste context, tokens, and time.

`ag-flow` routes each task independently and escalates only when the work justifies it.

```text
User request
    │
    ▼
Adaptive routing
    │
    ├── Direct ───────────────► execute + targeted verification
    │
    ├── Guided ───────────────► explore → plan → execute → verify
    │
    └── Orchestrated ─────────► explore → plan → bounded work packages
                                      │
                                      ├── executor(s)
                                      └── independent verification
```

No manual Light / Medium / Heavy mode is required. Explicit user instructions always win.

## Install

Install the complete workflow with the Skills CLI:

```bash
npx skills add thanhnam2811/ag-flow --skill '*'
```

Install for Claude Code and Codex explicitly:

```bash
npx skills add thanhnam2811/ag-flow \
  --agent claude-code \
  --agent codex \
  --skill '*'
```

Install globally:

```bash
npx skills add thanhnam2811/ag-flow \
  --agent claude-code \
  --agent codex \
  --skill '*' \
  --global
```

Or install only selected skills:

```bash
npx skills add thanhnam2811/ag-flow \
  --skill adaptive-routing \
  --skill verification
```

## Core skills

| Skill | Responsibility |
| --- | --- |
| [`adaptive-routing`](skills/adaptive-routing/) | Classify each task and select the cheapest reliable execution path |
| [`codebase-exploration`](skills/codebase-exploration/) | Discover only repository context relevant to the task |
| [`implementation-planning`](skills/implementation-planning/) | Turn findings into an executable, dependency-aware plan |
| [`work-package-dispatch`](skills/work-package-dispatch/) | Split complex work into bounded, non-overlapping packages |
| [`work-package-execution`](skills/work-package-execution/) | Execute one package with strict ownership and concise reporting |
| [`verification`](skills/verification/) | Verify claims through execution with risk-aware depth |
| [`systematic-debugging`](skills/systematic-debugging/) | Debug from evidence and hypotheses instead of speculative edits |
| [`session-handoff`](skills/session-handoff/) | Persist only the minimum state needed to resume safely |

## Runtime model

Core skills use **semantic roles**, not hard-coded agent APIs:

| Role | Responsibility |
| --- | --- |
| **Orchestrator** | Owns global decisions, boundaries, and integration |
| **Explorer** | Performs read-only context discovery |
| **Executor** | Implements one bounded work package |
| **Reviewer** | Independently verifies risky or complex changes |

When a runtime supports subagents, these roles can be delegated. When it does not, the same boundaries are executed sequentially by the main agent. This lets the workflow degrade gracefully without changing its core behavior.

## Routing model

### Direct

Use for local, low-risk, clearly bounded work. The main agent acts directly and performs targeted verification.

### Guided

Use when the task spans multiple files, contains meaningful uncertainty, or benefits from explicit planning. Explore only what is needed, plan, execute, and verify.

### Orchestrated

Use for cross-system work, high-risk changes, or workstreams that are genuinely parallelizable. The orchestrator creates bounded work packages with explicit ownership and verifies integration independently.

See [`references/routing-matrix.md`](references/routing-matrix.md) for the routing contract.

## Design principles

- Route per task, not per session.
- Load only context required for the current responsibility.
- Delegate only when context isolation, specialization, parallelism, or independent verification provides real value.
- Keep work-package ownership explicit and non-overlapping.
- Prefer execution-based verification over inspection-only confidence.
- Preserve project-native instructions such as `AGENTS.md` and `CLAUDE.md`.
- Keep core skills runtime-agnostic; isolate capability-specific fallbacks.
- Report deltas, evidence, and unresolved risks instead of chronological agent logs.

## Reference contracts

- [`routing-matrix.md`](references/routing-matrix.md) — route selection and escalation rules
- [`work-package-contract.md`](references/work-package-contract.md) — bounded delegation contract
- [`work-package.schema.json`](references/schemas/work-package.schema.json) — machine-readable Work Package contract
- [`work-package.example.yaml`](references/examples/work-package.example.yaml) — canonical schema-validated example
- [`verification-levels.md`](references/verification-levels.md) — risk-aware verification depth
- [`capability-fallbacks.md`](references/capability-fallbacks.md) — graceful degradation across runtimes

## Validation

The repository validates its own contracts on every push to `main` and every pull request. The validator checks Agent Skill frontmatter, relative Markdown links, the JSON Schema itself, and the canonical Work Package example.

Run the same checks locally:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
```

This keeps the validation layer intentionally small: one Python script plus `PyYAML` and `jsonschema`, without introducing a project-specific CLI.

## Tests

The repository includes prompt-level workflow cases rather than pretending markdown skills have traditional unit tests:

- [`tests/routing-cases.md`](tests/routing-cases.md) checks expected route behavior.
- [`tests/adversarial-cases.md`](tests/adversarial-cases.md) targets over-routing, ownership conflicts, false verification, and other failure modes.

Contributions that change routing or orchestration behavior should update these cases.

## Repository layout

```text
ag-flow/
├── skills/
│   ├── adaptive-routing/
│   ├── codebase-exploration/
│   ├── implementation-planning/
│   ├── work-package-dispatch/
│   ├── work-package-execution/
│   ├── verification/
│   ├── systematic-debugging/
│   └── session-handoff/
├── references/
│   ├── examples/
│   └── schemas/
├── scripts/
│   └── validate.py
├── tests/
├── .github/workflows/ci.yml
├── requirements-dev.txt
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
└── LICENSE
```

## Contributing

Contributions are welcome. Start with [`CONTRIBUTING.md`](CONTRIBUTING.md), and prefer concrete routing examples or measurable workflow improvements over additional ceremony.

For sensitive issues involving destructive agent behavior, credential exposure, unsafe command execution, or ownership bypasses, follow [`SECURITY.md`](SECURITY.md).

## License

ag-flow is released under the [MIT License](LICENSE).

## Status

`ag-flow` is currently **pre-1.0**. The core orchestration model is intentionally small; domain-specific skills can be layered on top without changing the execution architecture.
