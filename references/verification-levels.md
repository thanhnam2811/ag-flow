# Verification Levels

Verification depth should scale with risk and scope, not agent count.

## Level 1 — self-check

Minimum for any code change:

- inspect final diff/behavior
- check acceptance criteria
- run the narrowest relevant executable check when possible

## Level 2 — targeted automation

Use for normal multi-file work:

- focused tests
- relevant type checks
- lint/build slice
- direct reproduction of requested behavior or original failure
- schema/migration validation where relevant

## Level 3 — independent verification

Use for high-risk or broad changes:

- auth/security-sensitive behavior
- migrations/destructive data work
- public interfaces
- concurrency/state consistency
- cross-system changes
- orchestrated multi-package implementations

The independent reviewer should receive the task contract, relevant diff/context, and verification entry points—not the implementer's full chain of reasoning. When delegated to a subagent, use a **balanced / mid-tier model** and enforce a **bounded review perimeter**: evaluate spec fidelity against acceptance criteria, invariant preservation, and regression risks in the affected area. The reviewer may inspect directly relevant untouched callers, callees, interfaces, contracts, and tests when needed to establish those claims, but must not expand into unrelated code, subjective style bikeshedding, or unsolicited redesigns.

## Evidence reporting

Always separate:

- passed checks
- failed checks
- skipped/unavailable checks
- residual risk

Never convert "looks correct" into "verified" when executable evidence was available but not run.
