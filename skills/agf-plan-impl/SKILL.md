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

## Decide whether to delegate

A multi-step plan does not automatically justify multiple agents. Delegate only when work packages can be isolated with explicit ownership and the coordination cost is lower than sequential execution.

For complex parallel work, hand the validated plan to `agf-dispatch-package`.
