---
name: agf-spec-clarify
description: Resolve requirement ambiguity that would materially change implementation or acceptance criteria and cannot be cheaply inferred from repository evidence. Use only for requirement uncertainty, not routing or implementation uncertainty.
---

# Spec Clarification

Ask only what the repository cannot answer, and only when the answer would change what gets built.

## Gate

Invoke this skill only when both are true:

- A missing requirement or acceptance criterion would materially change the implementation or what counts as done.
- The answer cannot be cheaply inferred from repository evidence (existing code, tests, config, conventions, prior decisions).

If repository evidence can answer it, use `agf-explore-code` instead of asking — do not ask the user something the codebase already tells you.

If the gap would not change the implementation or acceptance criteria, do not ask at all. Proceed with the most reasonable default and state the assumption in the final report instead of blocking on it.

## Method

1. **Explore before asking.** Check the repository for the answer first — existing patterns, similar features, tests, docs, prior decisions. Skip any question that exploration resolves.
2. **Rank by dependency.** Order remaining questions so answers that constrain other decisions come first.
3. **One question per turn.** Never bundle multiple questions into one message.
4. **Always propose a default.** State a recommended answer and the reason in one sentence, so the user can confirm instead of composing an answer from scratch.
5. **Resolve one decision before opening the next.** Do not jump between unrelated open questions.
6. **Stop as soon as the remaining ambiguity no longer changes implementation or acceptance criteria.** Do not keep probing for completeness once the work is unblocked.

## Output

End with a compact decision brief, not a transcript:

- **Locked decisions** — what was resolved and why.
- **Assumptions** — low-impact gaps that were defaulted instead of asked, stated explicitly.
- **Still open** — anything `agf-plan-impl` or the executor must not guess on.

Hand the brief to whatever comes next in the chosen route — `agf-plan-impl`, or straight to execution when a separate planning pass isn't warranted. Do not replay the question-and-answer exchange itself.
