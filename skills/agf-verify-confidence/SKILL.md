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

If the runtime supports subagents, use a fresh reviewer subagent with a **balanced / mid-tier model** (e.g. `flash`, `sonnet`, `gpt-4o`). A balanced tier provides sufficient reasoning depth for edge-case and contract analysis without incurring the heavy token cost and latency of frontier models. Supply only the task contract, relevant diff/context, and verification entry points. Otherwise perform a second-pass review separated from implementation reasoning. Executor-reported verification is input to this review, not a substitute for it — re-run or independently inspect the evidence rather than accepting the executor's claim.

### Bounded review perimeter (Anti-sprawl)

To prevent the reviewer from wandering into unrelated code or generating sprawling commentary:

- **Pass only the perimeter** — supply strictly the task contract, the exact changed diff, relevant interfaces, and verification commands. Do not forward the entire codebase or full orchestrator conversation history.
- **Bound the evaluation** — assess only:
  1. Spec fidelity against explicit acceptance criteria.
  2. Regression risk and invariant preservation in the touched subsystem.
  3. Consistency between reported verification results and the actual diff.
- **Enforce negative boundaries** — explicitly forbid the reviewer from:
  - inspecting or critiquing untouched files
  - debating subjective stylistic preferences or formatting (style bikeshedding)
  - proposing unsolicited architectural redesigns or future scope expansion
  - re-implementing the solution unless requested to provide a minimal patch

## Semantic verifier gate

Use an independent LLM verifier only when executable evidence cannot fully establish a material acceptance criterion, or when independent semantic review materially increases confidence. Never use LLM judgment to replace an available deterministic check.

Decompose semantic review into concrete criteria derived from the task contract instead of asking one broad "is this correct?" question. Typical criteria include:

- spec fidelity and missing/extra behavior
- scope and ownership adherence
- interface and invariant consistency that is not fully executable
- unnecessary complexity or unsupported design assumptions
- consistency between reported evidence and the actual diff/context

Keep evidence strengths ordered: deterministic executable evidence outranks LLM judgment, which outranks unsupported static confidence. A failing test, build, type check, schema validator, or prover is not overridden by an LLM saying the change looks correct. If executable checks pass but the verifier finds a plausible spec mismatch, investigate whether the tests or proof target are incomplete instead of dismissing either signal.

Do not invent numerical precision. Unless the runtime exposes a real probabilistic verifier signal, report semantic confidence qualitatively (for example high/medium/low/unknown) with the evidence or concern that supports it.

Repeat semantic evaluation only when the judgment is materially uncertain or high-stakes and the extra cost is justified. Do not turn routine Level 1/2 verification into repeated LLM voting.

## Reviewer contract

Verify through two lenses — internal reasoning, not a required output format:

- **Spec fidelity** — did we build what was requested? Acceptance criteria, missing/extra behavior.
- **Engineering confidence** — invariants, interface compatibility, error/edge paths, integration across packages, unnecessary complexity, executable evidence.

When the semantic verifier gate fires, decompose these lenses into the smallest material criteria that cannot already be settled by executable evidence. A clean implementation of the wrong requirement should fail spec fidelity even when engineering confidence is high.

Stay within the bounded review perimeter: do not re-implement the feature or comment outside the touched boundary unless a focused repair is required.

## Failure loop

When verification fails:

1. isolate the failing package or assumption
2. return the smallest actionable failure context
3. attempt one focused repair
4. re-run affected verification
5. replace/repackage or escalate to the orchestrator if the same executor remains blocked

Avoid unbounded retry loops.

## Completion rule

Report what was actually verified. Distinguish executable evidence from semantic verifier judgment, and distinguish passed checks, skipped checks, unavailable checks, and residual risk. Verifier strength bounds what may be claimed.
