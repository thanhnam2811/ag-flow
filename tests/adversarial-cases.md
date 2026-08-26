# Adversarial Cases

These cases guard against orchestration failure modes that waste tokens or reduce correctness.

## 1. Multi-file does not mean multi-agent

**Prompt:** Rename an internal DTO used in 18 files.

Expected behavior:

- classify as broad/mechanical but not automatically Orchestrated
- inspect ownership and change pattern
- execute sequentially if delegation adds little value
- verify references/type checks

Failure: spawning several executors whose write surfaces overlap.

## 2. One-file can still be high risk

**Prompt:** Change the authorization check in one middleware file.

Expected behavior:

- elevate risk despite local scope
- inspect auth invariants/callers/tests
- require stronger verification, potentially independent review

Failure: choosing shallow verification because only one file changed.

## 3. Fake parallelism

**Prompt:** Refactor a shared interface, then update all implementations.

Expected behavior:

- stabilize/assign the shared interface first
- only parallelize consumers after the interface is fixed

Failure: multiple executors independently editing the shared contract.

## 4. Context flooding

**Prompt:** Add a new endpoint in a large monorepo.

Expected behavior:

- explorer returns relevant service/package, conventions, interface, and test entry points
- executor receives bounded context

Failure: forwarding full chat history or repository-wide dumps to each worker.

## 5. Reviewer contaminated by implementation narrative

**Prompt:** Implement and independently review a security-sensitive change.

Expected behavior:

- reviewer gets task contract, relevant diff/context, invariants, and verification hooks
- reviewer forms its own assessment

Failure: reviewer receives the implementer's full reasoning and merely confirms it.

## 6. Sticky route

Task A is a large cross-system migration. Task B is a README typo.

Expected behavior: Task B routes independently to Direct.

Failure: preserving Orchestrated mode for the session.

## 7. Infinite repair loop

An executor fails the same test repeatedly.

Expected behavior:

- one focused repair with smallest failing evidence
- if still blocked, repackage/replace or return to orchestrator

Failure: repeated blind retries with growing context.

## 8. Static inspection presented as execution

Runtime cannot run tests.

Expected behavior: report static review and explicitly state executable verification was unavailable.

Failure: claim tests/behavior are verified.

## 9. Existing project instructions

Repository already contains `AGENTS.md`, `CLAUDE.md`, contribution rules, or task-state conventions.

Expected behavior: respect existing instructions and use existing state/documentation structure.

Failure: create competing framework files or overwrite project conventions.

## 10. User forbids delegation

**Prompt:** Fix this without subagents.

Expected behavior: preserve exploration/planning/verification semantics sequentially in the main agent.

Failure: delegate because automatic routing classified the task as Orchestrated.

## 11. User asks for parallelism where unsafe

**Prompt:** Use five agents in parallel to change this shared schema and all callers.

Expected behavior: honor the goal of speed but explain/avoid overlapping ownership; sequence the shared contract before parallel consumers where needed.

Failure: blindly create overlapping packages.

## 12. Apparent complex task collapses after discovery

**Prompt:** Fix login across frontend and backend.

Discovery shows a single malformed frontend request parameter.

Expected behavior: downgrade to a local/direct fix and targeted verification.

Failure: continue with the originally assumed orchestration plan.

## 13. Trivial task, skill budget

**Prompt:** Rename a local variable in one function for clarity.

Expected behavior: route Direct, run only `agf-route-adaptive` + `agf-verify-confidence` Level 1.

Failure: loading `agf-spec-clarify`, `agf-plan-impl`, or `agf-dispatch-package` for a change this small.

## 14. Read-only discovery does not need clarification

**Prompt:** Find out which module owns retry logic for outbound HTTP calls; do not change anything.

Expected behavior: use `agf-explore-code` alone — there is no requirement decision pending, only an ownership question the repository can answer.

Failure: invoking `agf-spec-clarify` for a question the codebase already answers.

## 15. Requirement ambiguity is not fixed by reading more code

**Prompt:** Add support for exporting reports, but it is unclear which formats should be supported.

Expected behavior: invoke `agf-spec-clarify` — no amount of repository exploration tells you which export formats the user wants.

Failure: guessing a format silently, or treating `agf-explore-code` as sufficient because the codebase has no export feature to inspect.

## 16. High risk does not imply dispatch

**Prompt:** Rewrite the token-expiry check in the auth middleware; the bug is already reproduced in one file.

Expected behavior: stay single-executor, raise verification to Level 3 for the security-sensitive change.

Failure: spawning multiple executors or dispatching packages because the change is high-risk.

## 17. No-subagent runtime does not change the route

**Prompt:** Split this module into three packages with stable interfaces; do it yourself, no subagents.

Expected behavior: route stays Orchestrated with `needs.delegation: true`; execute the same packages sequentially in the main agent while preserving ownership boundaries.

Failure: downgrading the route to Guided/Direct because the runtime (or the user) forbids delegation.

## 18. Routing uncertainty gets at most one question

**Prompt:** Improve the checkout flow.

Expected behavior: attempt cheap inspection of the checkout module first; if scope is still materially ambiguous, ask exactly one routing question with a recommended default.

Failure: asking an open-ended "what's the scope?" question without inspecting first, or asking more than one routing question.
