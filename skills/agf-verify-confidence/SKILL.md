---
name: agf-verify-confidence
description: Verify coding changes through execution with depth proportional to scope and risk. Use before claiming completion, especially for multi-file, high-risk, cross-system, or delegated work.
---

# Verification

Confidence must come from evidence, preferably execution.

## Before any completion claim

1. Identify which executable check actually proves the claim.
2. Run it fresh — do not reuse a prior run's output or accept a subagent's self-report as-is.
3. Inspect the output and exit status yourself.
4. Claim only what that evidence supports.

## Verification levels

### Level 1 — self-check

Always perform when code changed:

- inspect the final diff or changed behavior
- check acceptance criteria and obvious regressions
- run the narrowest relevant executable check when possible

### Level 2 — targeted automated verification

Use for normal multi-file work:

- targeted tests
- relevant type checks
- lint/build slice
- migration/schema validation where applicable
- direct reproduction of the original failure or requested behavior
- if the behavior-change test gate applied, confirm the test actually failed before the fix and passes after — not just that it currently passes

### Level 3 — independent review

Use when any of these apply:

- auth/security-sensitive behavior
- migrations or destructive data operations
- public API/contract changes
- concurrency/state consistency
- broad refactors or cross-system changes
- orchestrated multi-package implementation
- user explicitly requested independent review

If the runtime supports subagents, use a fresh reviewer with only the task contract, relevant diff/context, and verification entry points. Otherwise perform a second-pass review separated from implementation reasoning. Executor-reported verification is input to this review, not a substitute for it — re-run or independently inspect the evidence rather than accepting the executor's claim.

## Reviewer contract

Verify:

- acceptance criteria
- interface compatibility
- invariants
- error/edge paths
- tests and executable evidence
- integration across packages

Do not re-implement the feature unless a repair is required.

## Failure loop

When verification fails:

1. isolate the failing package or assumption
2. return the smallest actionable failure context
3. attempt one focused repair
4. re-run affected verification
5. replace/repackage or escalate to the orchestrator if the same executor remains blocked

Avoid unbounded retry loops.

## Completion rule

Report what was actually verified. Distinguish passed checks, skipped checks, unavailable checks, and residual risk.
