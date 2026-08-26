---
name: agf-session-handoff
description: Persist the minimum durable state needed to resume an unfinished coding task without replaying the full conversation. Use when work spans sessions, context is becoming large, or another agent must continue later.
---

# Session Handoff

Persist decisions and state, not transcript history.

## Include only

- current goal and completion state
- decisions already made and why they constrain future work
- files/symbols currently relevant
- completed changes and verification evidence
- next concrete steps in dependency order
- blockers, risks, and unresolved questions
- commands needed to resume verification

## Exclude

- chronological chat summaries
- generic repository explanations
- abandoned hypotheses unless they prevent repeated mistakes
- raw tool output that can be reproduced cheaply
- content already captured in an existing plan/spec/ADR/issue/diff — reference its path or URL instead of copying it
- filler, repetition, and narrative framing — compress prose, not information; keep exact commands, paths, symbols, APIs, errors, constraints, and unresolved risks intact

## Never persist secrets

Never write secrets, tokens, credentials, or other sensitive values into a handoff artifact. Reference where they are configured (an env var name, a secrets-manager key) instead of the value itself.

## Durable vs transient knowledge

Promote stable architecture decisions, conventions, and recurring gotchas into the project's existing durable documentation when appropriate. Keep task-specific progress in a transient handoff artifact.

Do not create a new documentation framework when the repository already has one.

## Resume behavior

On resume, treat the handoff as a compact index. Revalidate facts that may have changed since it was written, then continue from the next concrete step rather than re-exploring the entire repository.
