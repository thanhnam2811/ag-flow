# Canonical Example: Direct Route

## Scenario

A pagination endpoint accepts negative `pageSize` values. The endpoint, validation location, and focused unit tests are already known.

## Routing decision

```yaml
scope: local
uncertainty: low
risk: low
parallelizable: false
route: direct
```

No explorer or executor delegation is justified. The main agent can make the bounded change more cheaply than transferring context to another agent.

## Execution

1. Read the endpoint and its focused tests.
2. Add validation rejecting negative `pageSize` values.
3. Add or update one focused regression test.
4. Inspect the diff for unrelated changes.
5. Run the targeted test.

## Verification

Expected verification depth: **Level 1 + targeted Level 2** when executable tests are available.

```text
Changed:
- endpoint validation rejects pageSize < 0
- regression test covers the negative boundary

Verification:
- targeted pagination test passed

Delegation:
- none
```

## Why this stays Direct

The task is local, ownership is known, the behavior change is small, and delegation would cost more context than it saves. Multi-agent execution would be over-orchestration.
