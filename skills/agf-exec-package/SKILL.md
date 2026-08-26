---
name: agf-exec-package
description: Execute one bounded coding work package with strict ownership, minimal context expansion, self-verification, and concise handoff. Use for delegated or sequential package execution.
---

# Work Package Execution

Execute the assigned package; do not redesign the whole task.

## Before editing

Confirm:

- goal and acceptance criteria are clear
- write ownership is explicit
- required interfaces and invariants are known
- verification commands are available or can be inferred cheaply

If a missing decision would change public interfaces, shared ownership, architecture, or data safety, stop and escalate instead of guessing.

## Execution rules

- Change only owned files unless the package explicitly permits expansion.
- Preserve upstream decisions and declared interfaces.
- Read additional context only when necessary to complete or verify the package.
- Avoid unrelated cleanup and opportunistic refactors.
- Prefer the smallest coherent implementation that satisfies acceptance criteria.

## Self-verification

Run the narrowest meaningful checks for the package: targeted tests, type checks, lint/build slices, or direct reproduction where appropriate.

Do not claim success from inspection alone when execution is possible.

## Return contract

Return a compact delta report:

- **Changed** — files/symbols and behavior changed.
- **Verification** — exact checks and results.
- **Interfaces** — any interface facts the integrator needs.
- **Risks/unresolved** — only remaining issues.

Do not return a chronological work log or repeat context already provided.
