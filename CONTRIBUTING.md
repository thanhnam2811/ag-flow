# Contributing to ag-flow

Thanks for helping improve ag-flow.

## What makes a good contribution

Prefer changes that make the workflow more reliable, portable, measurable, or token-efficient without adding unnecessary ceremony.

Good contributions include:

- routing cases that expose over-escalation or under-escalation
- runtime-portability improvements
- clearer work-package or verification contracts
- adversarial tests for delegation, ownership, and false-success claims
- focused workflow skills that remain agent-agnostic

Avoid runtime-specific assumptions in core skills unless they are isolated as documented fallbacks.

## Development workflow

1. Create a focused branch.
2. Keep each change scoped to one workflow concern.
3. Update or add cases under `tests/` when behavior changes.
4. Preserve project-native instructions such as `AGENTS.md` and `CLAUDE.md`.
5. Verify examples and referenced skill names before opening a pull request.

## Skill guidelines

Each skill should:

- live in its own directory under `skills/`
- have a `SKILL.md` with concise frontmatter and portable instructions
- describe semantic behavior rather than hard-code a specific agent API
- load only the context needed for its responsibility
- define clear inputs, outputs, and stopping conditions
- prefer execution-based verification over unsupported claims

## Pull requests

A pull request should explain:

- the behavior being changed
- why the change is needed
- how it affects routing, context usage, delegation, or verification
- what tests or examples were added or updated

Small, reviewable pull requests are preferred.

## Reporting bugs and proposing features

Use the repository issue templates and include a concrete prompt or scenario whenever possible. Reproducible routing examples are especially useful.
