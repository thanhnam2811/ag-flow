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

## Delegated explorer behavior

If the runtime supports subagents and delegation is useful, delegate exploration as a read-only role. The explorer must not edit code or make architecture decisions on behalf of the orchestrator.

Return only:

- Findings
- Relevant paths/symbols
- Constraints/invariants
- Verification hooks
- Uncertainties

Do not return a chronological exploration log.

## Context budget

Keep the brief small enough to be reused without recreating repository-wide context. Include exact names and paths where possible; omit generic explanations the main agent already knows.
