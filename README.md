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

```bash
npx skills add thanhnam2811/ag-flow --skill '*'
```

Claude Code + Codex:

```bash
npx skills add thanhnam2811/ag-flow \
  --agent claude-code \
  --agent codex \
  --skill '*'
```

Global install:

```bash
npx skills add thanhnam2811/ag-flow \
  --agent claude-code \
  --agent codex \
  --skill '*' \
  --global
```

## Core skills

| Skill | Responsibility |
| --- | --- |
| [`adaptive-routing`](skills/adaptive-routing/) | Select the cheapest reliable execution path per task |
| [`codebase-exploration`](skills/codebase-exploration/) | Discover only repository context relevant to the task |
| [`implementation-planning`](skills/implementation-planning/) | Turn findings into a dependency-aware plan |
| [`work-package-dispatch`](skills/work-package-dispatch/) | Split complex work into bounded non-overlapping packages |
| [`work-package-execution`](skills/work-package-execution/) | Execute one package with strict ownership and concise reporting |
| [`verification`](skills/verification/) | Verify claims through execution with risk-aware depth |
| [`systematic-debugging`](skills/systematic-debugging/) | Debug from evidence and hypotheses instead of speculative edits |
| [`session-handoff`](skills/session-handoff/) | Persist only the minimum state needed to resume safely |

## Runtime model

Core skills use semantic roles, not hard-coded agent APIs:

| Role | Responsibility |
| --- | --- |
| **Orchestrator** | Owns global decisions, boundaries, and integration |
| **Explorer** | Performs read-only context discovery |
| **Executor** | Implements one bounded work package |
| **Reviewer** | Independently verifies risky or complex changes |

When a runtime supports subagents, these roles can be delegated. Otherwise the same boundaries execute sequentially in the main agent.

## Routing model

- **Direct** — local, low-risk, clearly bounded work.
- **Guided** — multi-file, uncertain, or risk-sensitive work that benefits from exploration and planning.
- **Orchestrated** — cross-system, high-risk, or genuinely parallel work with clean ownership boundaries.

See [`references/routing-matrix.md`](references/routing-matrix.md).

## Canonical examples

Three end-to-end examples document the route boundaries and expected verification behavior:

- [`examples/01-direct-route/`](examples/01-direct-route/) — local pagination validation; no delegation.
- [`examples/02-guided-route/`](examples/02-guided-route/) — subsystem cache refactor; explore and plan, but execute sequentially.
- [`examples/03-orchestrated-route/`](examples/03-orchestrated-route/) — auth token migration with explicit non-overlapping work packages and Level 3 review.

These examples are intentionally about **why a route is justified**, not just what steps an agent performs.

## Reference contracts

- [`routing-matrix.md`](references/routing-matrix.md) — route selection and escalation rules
- [`work-package-contract.md`](references/work-package-contract.md) — bounded delegation contract
- [`work-package.schema.json`](references/schemas/work-package.schema.json) — machine-readable Work Package contract
- [`work-package.example.yaml`](references/examples/work-package.example.yaml) — canonical schema-validated example
- [`verification-levels.md`](references/verification-levels.md) — risk-aware verification depth
- [`capability-fallbacks.md`](references/capability-fallbacks.md) — graceful degradation across runtimes

## Structured behavioral fixtures

The original human-readable test corpus is preserved in Markdown, while machine-readable fixtures are available for future eval tooling:

- [`tests/fixtures/routing-cases.yaml`](tests/fixtures/routing-cases.yaml) — 25 routing cases
- [`tests/fixtures/adversarial-cases.yaml`](tests/fixtures/adversarial-cases.yaml) — 12 adversarial cases

Fixture fields include `id`, `prompt`, `repo_state_mock`, `expected_route`, `risk_factors`, and `forbidden_actions`; adversarial cases can also define `expected_behaviors`.

The validator checks fixture version, required fields, route enums, list types, and globally unique case IDs. This makes the corpus machine-readable without committing to an eval runtime yet.

## Validation

The repository validates its own contracts on every push to `main` and every pull request. Checks include:

- Agent Skill YAML frontmatter
- relative Markdown links
- Work Package JSON Schema validity
- canonical Work Package example
- structured routing/adversarial fixture shape

Run locally:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
```

The validation layer intentionally stays small: one Python script plus `PyYAML` and `jsonschema`, with no project-specific CLI.

## Design principles

- Route per task, not per session.
- Load only context required for the current responsibility.
- Delegate only when context isolation, specialization, parallelism, or independent verification provides real value.
- Keep work-package ownership explicit and non-overlapping.
- Prefer execution-based verification over inspection-only confidence.
- Preserve project-native instructions such as `AGENTS.md` and `CLAUDE.md`.
- Keep core skills runtime-agnostic; isolate capability-specific fallbacks.
- Report deltas, evidence, and unresolved risks instead of chronological agent logs.

## Repository layout

```text
ag-flow/
├── skills/
├── references/
│   ├── examples/
│   └── schemas/
├── examples/
│   ├── 01-direct-route/
│   ├── 02-guided-route/
│   └── 03-orchestrated-route/
├── tests/
│   ├── fixtures/
│   ├── routing-cases.md
│   └── adversarial-cases.md
├── scripts/
│   └── validate.py
├── .github/workflows/ci.yml
├── requirements-dev.txt
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
└── LICENSE
```

## Contributing

Start with [`CONTRIBUTING.md`](CONTRIBUTING.md). Prefer concrete routing examples or measurable workflow improvements over additional ceremony.

For sensitive issues involving destructive agent behavior, credential exposure, unsafe command execution, or ownership bypasses, follow [`SECURITY.md`](SECURITY.md).

## License

ag-flow is released under the [MIT License](LICENSE).

## Status

`ag-flow` is currently **pre-1.0**. The next milestone is empirical evaluation of the structured fixtures across real coding-agent runtimes; new workflow skills should be added only when evidence shows a repeated gap.
