---
name: agf-plan-impl
description: Convert repository findings and a coding request into an executable plan with dependencies, interfaces, acceptance criteria, and verification. Use when implementation spans multiple meaningful steps or architecture decisions.
---

# Implementation Planning

Plan only to the depth needed to execute safely.

## Plan contract

For each meaningful step capture:

- outcome
- owned files or subsystem
- dependencies on earlier steps
- interfaces/contracts that must remain stable
- invariants and constraints
- acceptance criteria
- verification method

## Rules

- Base plans on repository evidence, not generic architecture patterns.
- Separate required work from optional cleanup.
- Prefer dependency order over arbitrary file order.
- Identify shared files and integration boundaries before parallelizing.
- Make hidden assumptions explicit when they can change implementation.
- Keep plans compact enough to remain useful during execution.

## Simplicity gate

Before adding complexity, check in order:

1. Can this requirement be omitted because it isn't actually needed?
2. Does the repository, stdlib, or platform already provide it?
3. Can an existing abstraction be extended instead of adding a new one?
4. Is a new abstraction/config/dependency justified by more than one real use case now?
5. Can the same behavior ship with a smaller diff?

Simplicity is a constraint after correctness, acceptance criteria, compatibility, and safety — never cut necessary robustness just to shrink the diff.

## Decide whether to delegate

A multi-step plan does not automatically justify multiple agents. Delegate only when work packages can be isolated with explicit ownership and the coordination cost is lower than sequential execution.

For complex parallel work, hand the validated plan to `agf-dispatch-package`.
