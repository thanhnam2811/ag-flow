---
name: systematic-debugging
description: Debug coding failures from reproducible evidence, hypotheses, and targeted experiments instead of speculative edits. Use for bugs, failing tests, regressions, flaky behavior, and unclear runtime errors.
---

# Systematic Debugging

Prefer evidence over edit-and-pray loops.

## Workflow

1. **Reproduce** — establish the smallest reliable failing case or gather the strongest available evidence.
2. **Localize** — identify the failing boundary, relevant state, and recent or likely change surface.
3. **Form hypotheses** — keep a short ranked set; each hypothesis must predict an observable result.
4. **Test cheaply** — inspect, instrument, or run targeted commands that discriminate among hypotheses.
5. **Fix the cause** — make the smallest coherent change that addresses the supported root cause.
6. **Verify** — reproduce the original path, then run relevant regression checks.

## Rules

- Do not stack multiple speculative fixes before observing results.
- Distinguish cause, symptom, and secondary failure.
- Preserve useful failing evidence until the fix is confirmed.
- Expand scope only when evidence crosses a subsystem boundary.
- If the bug is broad or context-heavy, use `codebase-exploration` before editing.
- If the fix becomes multi-step or cross-system, hand off to `implementation-planning` and let `adaptive-routing` re-evaluate execution depth.

## Flaky failures

For flaky behavior, collect enough repeated evidence to identify correlation or nondeterminism. Do not claim a flaky issue is fixed from one passing run.

## Output

Summarize root cause, change, verification evidence, and any remaining uncertainty. Omit the chronological investigation log unless the user asks for it.
