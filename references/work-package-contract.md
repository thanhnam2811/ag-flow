# Work Package Contract

A work package is a bounded execution unit. It should contain enough context to execute safely without forwarding the full parent conversation.

```yaml
goal: <one concrete outcome>

ownership:
  writable:
    - <path or subsystem>
  forbidden_or_shared:
    - <path reserved elsewhere>

context:
  relevant_files:
    - <path>
  relevant_symbols:
    - <symbol>
  upstream_decisions:
    - <decision>

interfaces:
  - <contract with other packages>

constraints:
  - <invariant or project rule>

acceptance:
  - <observable completion condition>

verification:
  - <command or behavior check>

escalate_if:
  - <condition requiring orchestrator decision>
  - executing an irreversible, production-affecting, externally visible, or
    destructive action that has not been explicitly authorized

return:
  - changed
  - verification
  - interface_facts
  - unresolved
```

## Execution authority

Preparing code, commands, migrations, release artifacts, or deployment steps is allowed; actually running/publishing/applying them requires explicit user approval when that action crosses the current execution authority. Authorization can already be granted by the user's original request (e.g. "build and deploy this to production") — do not add a redundant second confirmation when authority was already explicit.

- Allowed without extra approval: write migration code, generate SQL, prepare deployment config, build release artifact, draft rollback command.
- Escalate before: run migration against production data, execute destructive SQL, deploy to production, publish package/release, rotate/revoke real credentials.

Route decides how much workflow. Risk decides verification strength. Authority decides whether an action may actually be executed — a separate dimension from both.

## Good package properties

- one owner for every write surface
- little or no overlapping write ownership
- explicit interfaces between packages
- no hidden architecture decisions delegated accidentally
- acceptance criteria test behavior rather than implementation style
- enough repository facts to avoid repeated broad exploration

## Bad package smells

- "fix everything related to auth"
- multiple packages editing the same shared contract independently
- full repository dumps attached as context
- executor expected to infer product/architecture choices
- no verification path
- no escalation boundary

## Delegated envelope precedence

The parent conversation context is passive background only; the delegated task/envelope is the sole execution authority.

> **Role, scope, and allowed actions in the delegated envelope are a hard boundary; inherited parent context grants no additional authority.**

Delegated subagents must strictly adhere to their assigned role and envelope:
- Explorers must not make architecture decisions, choose implementation strategies, or offer implementation.
- Executors must not redesign the global task or edit outside writable ownership.

## Research / exploration envelope contract

When delegating exploration/research, use a dedicated bounded envelope:

```yaml
role: explorer
goal: inspect current transport interfaces

context:
  relevant_files:
    - <path>
  relevant_symbols:
    - <symbol>

allowed:
  - read
  - search
  - report signatures/interfaces/conventions

forbidden:
  - edit
  - architecture decisions
  - implementation proposals
  - scope expansion

return:
  - findings
  - interfaces
  - constraints
  - uncertainties
```

### Delegation containment flow

```text
Orchestrator
   ↓ bounded research envelope
Explorer
   ↓
facts + interfaces + constraints + uncertainties
   ↓
STOP
   ↓
Orchestrator decides architecture / planning
```

## Executor return shape

Prefer delta knowledge:

```text
Changed:
- ...

Verification:
- ...

Interfaces:
- ...

Unresolved:
- ...
```

Do not return a chronological diary.
