# Canonical Example: Orchestrated Route

## Scenario

Migrate authentication tokens from a legacy identifier to a new token subject format. The data/schema work and API middleware work can be separated after the new contract is fixed.

## Routing decision

```yaml
scope: cross-system
uncertainty: medium
risk: high
parallelizable: true_after_contract_stabilization
route: orchestrated
```

The orchestrator owns the token-subject contract and integration boundary. Delegation starts only after that contract is explicit.

## Work Package A — Data/schema

```yaml
goal: Prepare the persistence layer for the new token subject format.
ownership:
  writable:
    - db/migrations/**
    - src/data/token-subject.ts
  forbidden_or_shared:
    - src/api/auth-middleware.ts
context:
  relevant_files:
    - src/data/token-subject.ts
  relevant_symbols:
    - TokenSubject
  upstream_decisions:
    - New token subjects are stable opaque strings.
interfaces:
  - API middleware consumes TokenSubject as an opaque string.
constraints:
  - Existing records must remain readable during migration.
acceptance:
  - Migration preserves old records and writes the new format.
verification:
  - Run migration tests and data-layer tests.
escalate_if:
  - Existing data cannot be migrated without a lossy transform.
return:
  - changed
  - verification
  - interface_facts
  - unresolved
```

## Work Package B — API middleware

```yaml
goal: Update authentication middleware to consume the new token subject contract.
ownership:
  writable:
    - src/api/auth-middleware.ts
    - tests/auth-middleware.test.ts
  forbidden_or_shared:
    - db/migrations/**
    - src/data/token-subject.ts
context:
  relevant_files:
    - src/api/auth-middleware.ts
  relevant_symbols:
    - authenticateRequest
  upstream_decisions:
    - New token subjects are stable opaque strings.
interfaces:
  - Middleware receives TokenSubject from the persistence/auth boundary.
constraints:
  - Authorization semantics must not change.
acceptance:
  - New subjects authenticate successfully and invalid subjects fail closed.
verification:
  - Run auth middleware tests and focused integration tests.
escalate_if:
  - Authorization behavior must change to support the new format.
return:
  - changed
  - verification
  - interface_facts
  - unresolved
```

## Integration and verification

Expected verification depth: **Level 3** because authentication and migration behavior are both high-risk.

The independent reviewer receives the task contract, relevant diff, invariants, and verification evidence — not the implementers' full reasoning narratives.

## Why this is Orchestrated

There are two useful non-overlapping write surfaces after the shared contract is stabilized. Delegation creates real parallel value, while explicit ownership prevents conflicting edits. The high-risk auth/data boundary also justifies independent verification.
