---
name: agf-explore-code
description: Discover the minimum repository context needed to solve a coding task. Use when relevant files, symbols, dependencies, conventions, or boundaries are uncertain.
---

# Codebase Exploration

Explore for decisions, not for completeness.

## Goals

Return a compact context brief containing:

- relevant files and symbols
- call/data/dependency relationships
- project conventions that constrain the change
- test and verification entry points
- unresolved uncertainties that could change the plan

## Method

1. Start from the user's target, error, feature, or known symbol.
2. Search narrowly for ownership, callers, implementations, tests, config, and interfaces.
3. Expand only when a discovered dependency materially affects the task.
4. Stop when the implementation boundary and verification path are clear.

Prefer symbol/file summaries over raw dumps. Do not read entire directories by default.

## When step 3 triggers, expand one step at a time

Only follow this ladder once local search genuinely doesn't answer the question — do not start here:

1. target file/symbol
2. direct callers, implementations, tests
3. one abstraction layer up
4. subsystem map
5. broader architecture — only if evidence actually crosses that boundary

Stop as soon as the current step resolves the decision; do not continue up the ladder for completeness.

## Delegated explorer behavior

If the runtime supports subagents and delegation is useful, delegate exploration as a strictly read-only role bounded by the delegated envelope.

> **Role, scope, and allowed actions in the delegated envelope are a hard boundary; inherited parent context grants no additional authority.**

### Hard scope boundary

When acting as a delegated explorer:

- **Allowed actions:**
  - Read files and search code.
  - Report existing signatures, interfaces, dependencies, conventions, and verification hooks found in the repository.
- **Forbidden actions (strictly prohibited):**
  - Making architecture decisions (e.g. choosing directory structure, framework layout, service boundaries).
  - Choosing implementation strategies or details (e.g. concurrency limits, transport/streaming protocols).
  - Expanding scope beyond the assigned envelope.
  - Editing files or executing mutations.
  - Offering implementation proposals or asking to implement (e.g. "want me to implement Phase 1?").
- **Uncertainty boundary:**
  - If a decision or requirement does not have a definitive answer in the repository, record it explicitly under `Uncertainties / decisions required` and **STOP**. Do not guess, decide, or propose design solutions to fill the gap.

### Return contract and containment flow

Return only:

- Findings
- Relevant paths/symbols
- Constraints/invariants
- Verification hooks
- Uncertainties / decisions required

Do not return a chronological exploration log. Once findings and uncertainties are returned, **STOP**. The orchestrator is the sole authority for architecture decisions and planning.

## Context budget

Keep the brief small enough to be reused without recreating repository-wide context. Include exact names and paths where possible; omit generic explanations the main agent already knows.
