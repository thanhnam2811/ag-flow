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
